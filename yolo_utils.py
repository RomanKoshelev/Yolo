import tensorflow as tf


def cell_locate(size, bbox, S):

    """ 
    locate the center of ground truth in which grid cell

    """
    x = tf.cast(tf.slice(bbox, [0,0], [-1,1]), tf.float32)
    y = tf.cast(tf.slice(bbox, [0,1], [-1,1]), tf.float32)
    w = tf.cast(tf.slice(bbox, [0,2], [-1,1]), tf.float32)
    h = tf.cast(tf.slice(bbox, [0,3], [-1,1]), tf.float32)


    height, width = size

    cell_w = width / S
    cell_h = height / S

    center_y = tf.add(y, tf.mul(h, 0.5))
    center_x = tf.add(x, tf.mul(w, 0.5))

    cell_coord_x = tf.cast(tf.div(center_x, cell_w), tf.int32)
    cell_coord_y = tf.cast(tf.div(center_y, cell_h), tf.int32)

    cell_num = tf.add(tf.mul(cell_coord_y, S), cell_coord_x)

    return cell_num
        
        



def convert_to_one(bbox, width, height, S):

    x, y, w, h = bbox

    x = tf.cast(x, tf.float32)
    y = tf.cast(y, tf.float32)
    w = tf.cast(w, tf.float32)
    h = tf.cast(h, tf.float32)

    global_center_x = tf.mul(tf.add(tf.mul(x, 2), w), 0.5)
    global_center_y = tf.mul(tf.add(tf.mul(y, 2), h), 0.5)

    w = tf.div(w, width)
    h = tf.div(h, height)

    cell_w = tf.cast(tf.div(tf.cast(width, tf.int32), S), tf.float32)
    cell_h = tf.cast(tf.div(tf.cast(height, tf.int32), S), tf.float32)


    cell_coord_x = tf.cast(tf.cast(tf.div(global_center_x, cell_w), tf.int32), tf.float32)
    cell_coord_y = tf.cast(tf.cast(tf.div(global_center_y, cell_h), tf.int32), tf.float32)

    offset_x = tf.div(tf.sub(global_center_x, tf.mul(cell_coord_x, cell_w)), cell_w)
    offset_y = tf.div(tf.sub(global_center_y, tf.mul(cell_coord_y, cell_h)), cell_h)


    assert offset_x.dtype == tf.float32 and \
            offset_y.dtype == tf.float32 and \
            w.dtype == tf.float32 and \
            h.dtype == tf.float32

    bbox = [offset_x, offset_y, w, h]

    return bbox

def convert_to_reality(bbox, width, height, S):

    relative_center_x, relative_center_y, global_w, global_h = bbox

    #relative_center_x = tf.clip_by_value(relative_center_x, 0, 1)
    #relative_center_y = tf.clip_by_value(relative_center_y, 0, 1)

    w = tf.cast(tf.mul(global_w, width), tf.int32)
    h = tf.cast(tf.mul(global_h, height), tf.int32)

    cell_w = width / S
    cell_h = height / S

    index = tf.reshape(tf.range(S * S),[-1,1])

    cell_coord_y = tf.div(index, S)
    cell_coord_x = tf.mod(index, S)

    real_x_left_up = tf.sub(tf.add(tf.reshape(tf.mul(cell_coord_x, cell_w), [-1]), tf.cast(tf.mul(relative_center_x, cell_w), tf.int32)), tf.cast(tf.mul(tf.cast(w, tf.float32), 0.5), tf.int32))
    real_y_left_up = tf.sub(tf.add(tf.reshape(tf.mul(cell_coord_y, cell_h), [-1]), tf.cast(tf.mul(relative_center_y, cell_h), tf.int32)), tf.cast(tf.mul(tf.cast(h, tf.float32), 0.5), tf.int32))


    real_x_left_up = tf.nn.relu(real_x_left_up)
    real_y_left_up = tf.nn.relu(real_y_left_up)
    
    assert real_x_left_up.dtype == tf.int32 and \
           real_y_left_up.dtype == tf.int32 and \
            w.dtype == tf.int32 and \
            h.dtype == tf.int32

    bbox = [real_x_left_up, real_y_left_up, w, h]

    return bbox