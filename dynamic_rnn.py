#!/usr/bin/env python3
import numpy as np
import tensorflow as tf
import csv

# Notes
# Goal is to build a pipeline from data to RNN
# use csv...want to use np.asarray(row), but this adds dimensionality, even if only 1, so we need to address that in the gen_batch
# version2...works for multi dimensional x input but y input needs to be read in as ints

# Global config variables
num_steps = 10 # number of truncated backprop steps ('n' in the discussion above)
batch_size = 100
num_classes = 3
state_size = 15
learning_rate = 0.1

x_dim = 7
y_dim = 1

x_data_file = open('/Users/jhs/tensorflow_python_3/RNN/x_data.csv', "r")
x_data_reader = csv.reader(x_data_file)

y_data_file = open('/Users/jhs/tensorflow_python_3/RNN/y_data.csv', "r") 
y_data_reader = csv.reader(y_data_file) 

raw_x = []
for row in x_data_reader:
    raw_x.append(np.asarray(row))
raw_x = np.array(raw_x)

raw_y = []
for row in y_data_reader:
    raw_y.append(int(row[0]))
    #raw_y.append(np.asarray(row))
raw_y = np.array(raw_y)


# adapted from https://github.com/tensorflow/tensorflow/blob/master/tensorflow/models/rnn/ptb/reader.py
def gen_batch(raw_data, batch_size, num_steps, x_dim, y_dim):
    raw_x, raw_y = raw_data       
    data_length = len(raw_x)    

    # partition raw data into batches and stack them vertically in a data matrix
    batch_partition_length = data_length // batch_size
    data_x = np.zeros([batch_size, batch_partition_length, x_dim], dtype=np.float32)
    data_y = np.zeros([batch_size, batch_partition_length], dtype=np.int32)
    #data_y = np.zeros([batch_size, batch_partition_length, y_dim], dtype=np.int32)
    for i in range(batch_size):
        data_x[i] = raw_x[batch_partition_length * i:batch_partition_length * (i + 1)]
        data_y[i] = raw_y[batch_partition_length * i:batch_partition_length * (i + 1)]
    # further divide batch partitions into num_steps for truncated backprop
    epoch_size = batch_partition_length // num_steps

    for i in range(epoch_size):
        x = data_x[:, i * num_steps:(i + 1) * num_steps]
        y = data_y[:, i * num_steps:(i + 1) * num_steps]
        yield (x, y)

def gen_epochs(n, num_steps):
    for i in range(n):
        yield gen_batch([raw_x, raw_y], batch_size, num_steps, x_dim, y_dim)

#Model
"""
Placeholders
"""

x = tf.placeholder(tf.float32, [batch_size, num_steps, x_dim], name='input_placeholder')
y = tf.placeholder(tf.int32, [batch_size, num_steps], name='labels_placeholder')
init_state = tf.zeros([batch_size, state_size])

"""
RNN Inputs
"""

rnn_inputs = x

"""
RNN
"""
cell = tf.contrib.rnn.BasicRNNCell(state_size)
rnn_outputs, final_state = tf.nn.dynamic_rnn(cell, rnn_inputs, initial_state=init_state)

"""
Predictions, loss, training step
"""
with tf.variable_scope('softmax'):
    W = tf.get_variable('W', [state_size, num_classes])
    b = tf.get_variable('b', [num_classes], initializer=tf.constant_initializer(0.0))
logits = tf.reshape(
            tf.matmul(tf.reshape(rnn_outputs, [-1, state_size]), W) + b,
            [batch_size, num_steps, num_classes])
predictions = tf.nn.softmax(logits)

losses = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
total_loss = tf.reduce_mean(losses)
train_step = tf.train.AdagradOptimizer(learning_rate).minimize(total_loss)

"""
Train the network
"""

def train_network(num_epochs, num_steps, state_size=state_size, verbose=True):
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        training_losses = []
        for idx, epoch in enumerate(gen_epochs(num_epochs, num_steps)):
            training_loss = 0
            training_state = np.zeros((batch_size, state_size))
            if verbose:
                print("\nEPOCH", idx)
            for step, (X, Y) in enumerate(epoch):
                tr_losses, training_loss_, training_state, _ = \
                    sess.run([losses,
                              total_loss,
                              final_state,
                              train_step],
                                  feed_dict={x:X, y:Y, init_state:training_state})
                training_loss += training_loss_
                if step % 100 == 0 and step > 0:
                    if verbose:
                        print("Average loss at step", step,
                              "for last 100 steps:", training_loss/100)
                    training_losses.append(training_loss/100)
                    training_loss = 0

    return training_losses
training_losses = train_network(90,num_steps)

