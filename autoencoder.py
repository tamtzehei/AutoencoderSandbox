import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.layers import fully_connected

# Import dataset
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# Specify some parameters
num_inputs = 784
num_hid1 = 392
num_hid2 = 196
num_hid3 = num_hid1
num_output = num_inputs
lr = 0.01
actf = tf.nn.relu

X = tf.placeholder(tf.float32, shape = [None, num_inputs])
initializer = tf.variance_scaling_initializer()

w1 = tf.Variable(initializer([num_inputs, num_hid1]), dtype = tf.float32)
w2 = tf.Variable(initializer([num_hid1, num_hid2]), dtype = tf.float32)
w3 = tf.Variable(initializer([num_hid2, num_hid3]), dtype = tf.float32)
w4 = tf.Variable(initializer([num_hid3, num_output]), dtype = tf.float32)

b1 = tf.Variable(tf.zeros(num_hid1))
b2 = tf.Variable(tf.zeros(num_hid2))
b3 = tf.Variable(tf.zeros(num_hid3))
b4 = tf.Variable(tf.zeros(num_output))

hid_layer1 = actf(tf.matmul(X, w1) + b1)
hid_layer2 = actf(tf.matmul(hid_layer1, w2) + b2)
hid_layer3 = actf(tf.matmul(hid_layer2, w3) + b3)
output_layer = actf(tf.matmul(hid_layer3, w4) + b4)

loss = tf.reduce_mean(tf.square(output_layer - X))

optimizer = tf.train.AdamOptimizer(lr)
train = optimizer.minimize(loss)

saver = tf.train.Saver()

init = tf.global_variables_initializer()

num_epoch = 5
batch_size = 150
num_test_images = 10

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(num_epoch):
        num_batches = mnist.train.num_examples//batch_size
        print(num_batches)
        for iteration in range(num_batches):
            X_batch, y_batch = mnist.train.next_batch(batch_size)
            sess.run(train, feed_dict = {X:X_batch})
            #save_path = saver.save(sess, "~/Projects/AutoencoderTutorial/model{03d}.ckpt")
            
            #print("Saved at {}".format(save_path))
            
        train_loss = loss.eval(feed_dict = {X:X_batch})
        print("epoch {} loss {}".format(epoch, train_loss))
        
    results = output_layer.eval(session = sess, feed_dict = {X:mnist.test.images[:num_test_images]})

    f,a = plt.subplots(2, 10, figsize = (20, 4))
    for i in range(num_test_images):
        a[0][i].imshow(np.reshape(mnist.test.images[i], (28, 28)))
        a[1][i].imshow(np.reshape(results[i], (28, 28)))
        
    a.show()


