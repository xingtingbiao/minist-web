#!/usr/bin/python3

import os
from mnist import input_data
import tensorflow as tf

from mnist.model import regression

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

# create a model
with tf.variable_scope('regression'):
    x = tf.placeholder(tf.float32, [None, 784])
    y, variables = regression(x)
    pass


# train
y_r = tf.placeholder('float', [None, 10])                                       # 真实值
cross_entropy = -tf.reduce_sum(y_r * tf.log(y))                                 # 预测值与真实值的交叉熵
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)    # 使用梯度下降优化器最小化交叉熵
correct_prediction = tf.equal(tf.argmax(y, 1), tf.arg_max(y_r, 1))              # 比较预测值和真实值是否一致
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))              # 统计预测正确的个数，取均值得到准确率

saver = tf.train.Saver(variables)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for _ in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)                        # 每次随机选取100个数据进行训练, 即所谓的"随机梯度下降(Stochastic Gradient Descent，SGD)"
        sess.run(train_step, feed_dict={x: batch_xs, y_r: batch_ys})            # 正式执行train_step，用feed_dict的数据取代placeholder
    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_r: mnist.test.labels}))
    path = saver.save(
        sess, os.path.join(os.path.dirname(__file__), 'data', 'regression.ckpt'),
        write_meta_graph=False, write_state=False
    )
    print('Saved:', path)
    pass

