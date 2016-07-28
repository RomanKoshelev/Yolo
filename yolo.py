from utils import IoU
from skimage import io
import tensorflow as tf
from imdb import load_imdb
import numpy as np


def conv2d(x, W, b, strides = 1):

    # input [ batch , height , width , channels ]
    # filters [ width , height , channels , output channels (number of filters)]
    #print x.get_shape()
    #print W.get_shape()
    x = tf.nn.conv2d(x, W, strides = [1, strides, strides, 1], padding = 'SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)

def maxpool2d(x, k = 2):
    return tf.nn.max_pool(x, ksize = [1, k, k, 1], strides = [1, k, k, 1], padding = 'SAME')

def conv_net(x, weights, biases, dropout):

    x = tf.reshape(x, shape = [-1, 448, 448, 3])

    # Convolution Layer

    print weights['conv21'].get_shape()
    print x.get_shape()
    print biases['conv21'].get_shape()
    conv1 = conv2d(x, weights['conv1'], biases['conv1'], strides = 2)
    conv1 = maxpool2d(conv1, k = 2)

    conv2 = conv2d(conv1, weights['conv2'], biases['conv2'])
    conv2 = maxpool2d(conv2, k = 2)

    conv3 = conv2d(conv2, weights['conv3'], biases['conv3'])
    conv4 = conv2d(conv3, weights['conv4'], biases['conv4'])
    conv5 = conv2d(conv4, weights['conv5'], biases['conv5'])
    conv6 = conv2d(conv5, weights['conv6'], biases['conv6'])
    conv6 = maxpool2d(conv6, k = 2)

    conv7 = conv2d(conv6, weights['conv7'], biases['conv7'])
    conv8 = conv2d(conv7, weights['conv8'], biases['conv8'])
    conv9 = conv2d(conv8, weights['conv9'], biases['conv9'])
    conv10 = conv2d(conv9, weights['conv10'], biases['conv10'])
    conv11 = conv2d(conv10, weights['conv11'], biases['conv11'])
    conv12 = conv2d(conv11, weights['conv12'], biases['conv12'])
    conv13 = conv2d(conv12, weights['conv13'], biases['conv13'])
    conv14 = conv2d(conv13, weights['conv14'], biases['conv14'])
    conv15 = conv2d(conv14, weights['conv15'], biases['conv15'])
    conv16 = conv2d(conv15, weights['conv16'], biases['conv16'])
    conv16 = maxpool2d(conv16, k = 2)

    conv17 = conv2d(conv16, weights['conv17'], biases['conv17'])
    conv18 = conv2d(conv17, weights['conv18'], biases['conv18'])
    conv19 = conv2d(conv18, weights['conv19'], biases['conv19'])
    conv20 = conv2d(conv19, weights['conv20'], biases['conv20'])
    conv21 = conv2d(conv20, weights['conv21'], biases['conv21'])
    conv22 = conv2d(conv21, weights['conv22'], biases['conv22'])

    conv23 = conv2d(conv22, weights['conv23'], biases['conv23'])
    conv24 = conv2d(conv23, weights['conv24'], biases['conv24'])

    # Fully connected layer
    # Reshape conv2 output to fit fully connected layer input
    fc1 = tf.reshape(conv24, [-1, weights['fc1'].get_shape().as_list()[0]])
    fc1 = tf.add(tf.matmul(fc1, weights['fc1']), biases['fc1'])
    fc1 = tf.nn.relu(fc1)
    # fc1 = tf.nn.dropout(fc1, dropout)

    fc2 = tf.add(tf.matmul(fc1, weights['fc2']), biases['fc2'])
    fc2 = tf.reshape(fc2, [-1, 49, 30])
    fc2 = tf.nn.relu(fc2)

    #fc1 = tf.reshape(conv2, [-1, weights['wd1'].get_shape().as_list()[0]])
    #fc1 = tf.add(tf.matmul(fc1, weights['wd1']), biases['bd1'])
    #fc1 = tf.nn.relu(fc1)

    # Apply dropout
    # fc1 = tf.nn.dropout(fc1, dropout)

    #out = tf.add(tf.matmul(fc1, weights['out']), biases['out'])

    return fc2

weights = {

    'conv1': tf.Variable(tf.random_normal([7, 7, 3, 64])),

    'conv2': tf.Variable(tf.random_normal([3, 3, 64, 192])),

    'conv3': tf.Variable(tf.random_normal([1, 1, 192, 128])),
    'conv4': tf.Variable(tf.random_normal([3, 3, 128, 256])),
    'conv5': tf.Variable(tf.random_normal([1, 1, 256, 256])),
    'conv6': tf.Variable(tf.random_normal([3, 3, 256, 512])),

    'conv7': tf.Variable(tf.random_normal([1, 1, 512, 256])),
    'conv8': tf.Variable(tf.random_normal([3, 3, 256, 512])),
    'conv9': tf.Variable(tf.random_normal([1, 1, 512, 256])),
    'conv10': tf.Variable(tf.random_normal([3, 3, 256, 512])),
    'conv11': tf.Variable(tf.random_normal([1, 1, 512, 256])),
    'conv12': tf.Variable(tf.random_normal([3, 3, 256, 512])),
    'conv13': tf.Variable(tf.random_normal([1, 1, 512, 256])),
    'conv14': tf.Variable(tf.random_normal([3, 3, 256, 512])),
    'conv15': tf.Variable(tf.random_normal([1, 1, 512, 512])),
    'conv16': tf.Variable(tf.random_normal([3, 3, 512, 1024])),

    'conv17': tf.Variable(tf.random_normal([1, 1, 1024, 512])),
    'conv18': tf.Variable(tf.random_normal([3, 3, 512, 1024])),
    'conv19': tf.Variable(tf.random_normal([1, 1, 1024, 512])),
    'conv20': tf.Variable(tf.random_normal([3, 3, 512, 1024])),
    'conv21': tf.Variable(tf.random_normal([3, 3, 1024, 1024])),
    'conv22': tf.Variable(tf.random_normal([3, 3, 1024, 1024])),
    'conv23': tf.Variable(tf.random_normal([3, 3, 1024, 1024])),
    'conv24': tf.Variable(tf.random_normal([3, 3, 1024, 1024])),

    'fc1':tf.Variable(tf.random_normal([7 * 7 * 1024, 4096])),
    'fc2':tf.Variable(tf.random_normal([4096, 7 * 7 * 30])),
    #'out':tf.Variable(tf.random_normal([]))
}

biases = {

    'conv1': tf.Variable(tf.random_normal(64)),

    'conv2': tf.Variable(tf.random_normal([192])),

    'conv3': tf.Variable(tf.random_normal([128])),
    'conv4': tf.Variable(tf.random_normal([256])),
    'conv5': tf.Variable(tf.random_normal([256])),
    'conv6': tf.Variable(tf.random_normal([512])),

    'conv7': tf.Variable(tf.random_normal([256])),
    'conv8': tf.Variable(tf.random_normal([512])),
    'conv9': tf.Variable(tf.random_normal([256])),
    'conv10': tf.Variable(tf.random_normal([512])),
    'conv11': tf.Variable(tf.random_normal([256])),
    'conv12': tf.Variable(tf.random_normal([512])),
    'conv13': tf.Variable(tf.random_normal([256])),
    'conv14': tf.Variable(tf.random_normal([512])),
    'conv15': tf.Variable(tf.random_normal([512])),
    'conv16': tf.Variable(tf.random_normal([1024])),

    'conv17': tf.Variable(tf.random_normal([512])),
    'conv18': tf.Variable(tf.random_normal([1024])),
    'conv19': tf.Variable(tf.random_normal([512])),
    'conv20': tf.Variable(tf.random_normal([1024])),
    'conv21': tf.Variable(tf.random_normal([1024])),
    'conv22': tf.Variable(tf.random_normal([1024])),
    'conv23': tf.Variable(tf.random_normal([1024])),
    'conv24': tf.Variable(tf.random_normal([1024])),

    'fc1':tf.Variable(tf.random_normal([4096])),
    'fc2':tf.Variable(tf.random_normal([7 * 7 * 30])),
    #'out':tf.Variable(tf.random_normal([])),
}





"""
x, y, w, h   ====>  between 0 , 1


"""
from tensorflow.examples.tutorials.mnist import input_data
#mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)


n_input = 448 * 448
n_classes = 2
x = tf.placeholder(tf.float32, [None, n_input]) # feed_dict (unknown batch , features)
y = tf.placeholder(tf.float32, [None, 5]) # feed_dict (unknown batch, prob for each classes)


B = 2

is_obj = None
not_obj = None

response_threshold = 0.5
def get_confidence(pred, y, B):
    
    confidence = None
    
    #print 'pred_shape : ', pred.get_shape()[1]
    shape = (-1,int(pred.get_shape()[1]),B) 
    #print shape
    for b in xrange(B):
        
        #print 'pred : ', pred[ : , : , b * 5 : b * 5 + 4].get_shape()
        
        if confidence == None:
            confidence = IoU(pred[ : , : , b * 5 : b * 5 + 4], y[ : , b * 5 : b * 5 + 4])
        else:
           # print confidence.dtype
            
            confidence = tf.concat(1,(confidence,IoU(pred[ : , : , b * 5 : b * 5 + 4], y[ : , b * 5 : b * 5 + 4])))
            print confidence.get_shape()
    

    """
    confidence shape = [batch, cell, B]

    """
    confidence = tf.reshape(confidence,shape)
    
    assert confidence.dtype == tf.float32

    return confidence

def is_responsible(confidence):

    """
    threshold = max of confidence

    so is_res will be a boolean vector, present wheather the cell is responsible for the object

    """

    max_iou = np.amax(confidence, axis = 2)
    
    is_res = (confidence >= max_iou)

    assert is_res.dtype == bool and confidence.dtype == float and is_res.shape == confidence.shape
    
    return is_res
    


def is_appear_in_cell(confidence):
    
    return np.sum(confidence, axis = 2) > 0
    
"""

training 

"""
print 'start training ... '
init = tf.initialize_all_variables()
lcoord = 5
lnoobj = .5

pred = conv_net(x, weights, biases, 1)
display_step = 20
confidence = get_confidence(pred, y, B)
is_res = is_responsible(confidence)
is_appear = is_appear_in_cell(confidence)
not_res = not is_res
images, objects = load_imdb('plate') 

loss = None

print 'dadawdawdwd'

for b in xrange(B):
    
    """
    B = [(SxS) x B]

    x, y => relative to cell
    w, h => relative to image
    
    pred = [batch, SxS, 5B+C]

    """
    dx = (pred[:,:,b*5+0] - y[:,0]) ** 2
    dy = (pred[:,:,b*5+1] - y[:,1]) ** 2
    dw = (pred[:,:,b*5+2]**0.5 - y[:,2]**0.5) ** 2
    dh = (pred[:,:,b*5+3]**0.5 - y[:,3]**0.5) ** 2
    dc = (pred[:,:,b*5+4] - y[:,4]) ** 2

    
    if loss == None:
        
        loss = lcoord * is_res[:,:,b] * (dx+dy) + \
                lcoord * is_res[:,:,b] * (dw+dh) + \
                is_res[:,:,b] * dc + \
                lnoobj * not_res[:,:,b] * dc
    else:

        loss += lcoord * is_res[:,:,b] * (dx+dy) + \
                lcoord * is_res[:,:,b] * (dw+dh) + \
                is_res[:,:,b] * dc + \
                lnoobj * not_res[:,:,b] * dc
    
    index = b + 1

loss += is_appear * sum((y[:,:,b:] - pred[:,:,b:]) ** 2)

assert len(y[:,:,b:]) == num_classes

loss = tf.reduce_mean(loss)


with tf.Session() as sess:
    
    sess.run(init)
    step = 1

    while step * batch_size < training_iters:

        batch_x = images[i * batch_size : (i+1) * batch_size]
        batch_y = objects[i * batch_size : (i+1) * batch_size]
        
        sess.run(optimizer, 
                feed_dict = {
                      x:batch_x,
                      y:batch_y})

        if step % display_step == 0:
            
            loss, acc = sess([cost, accuracy], 
                            feed_dict = { 
                                x:batch_x,
                                y:batch_y})

            print "Iter " , str(step*batch_size) + ", Minibatch Loss= " ,"{:.6f}".format(loss) , ", Training Accuracy= " ,"{:.5f}".format(acc)
            step += 1

    print "Optimization Finished!"