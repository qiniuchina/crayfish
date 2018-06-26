#!/usr/bin/env python
# coding=utf-8
import tushare as ts
import tensorflow as tf
import numpy as np

if __name__ == '__main__':
    df = ts.get_k_data('sh000001')
    x_data = np.array(df[['open','high','low','volume','close']],np.float32)
    y_data = np.array(df['close'].shift(-1),np.float32)
    
    x = tf.placeholder(tf.float32, [1, 5])
    y_ = tf.placeholder(tf.float32, [1, 1])
    W = tf.Variable(tf.zeros([5,1]))
    #W = tf.Variable(tf.random_uniform([5, 1], -1.0, 1.0))
    b = tf.Variable(tf.zeros([1]))
    #b = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
    y = tf.matmul(x,W) + b
    cost = tf.reduce_mean(tf.square(y_-y))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cost)

    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)
    steps = len(y_data) - 1
    for i in range(steps):
        #m = random.randint(0,steps)
        xs = x_data[i].reshape(1,5)
        print("xs=",xs)
        ys = np.array([[y_data[i]]])
        print("ys=",ys)
        feed = { x: xs, y_: ys }
        print("cost: %f" % sess.run(cost, feed_dict=feed))
        print(i, sess.run(W).flatten(), sess.run(b).flatten())
        print("\n")