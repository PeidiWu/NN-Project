#!/usr/bin/env python3

import csv
import numpy as np

x_file = open('/Users/jhs/tensorflow_python_3/RNN/x_data.csv', "w")
x_writer = csv.writer(x_file)

y_file = open('/Users/jhs/tensorflow_python_3/RNN/y_data.csv', "w") 
y_writer = csv.writer(y_file) 

# experiment #1
# y_t = x_t 

#for i in range(1000000):
#    my_list = np.random.randint(2, size=1)
#    x_writer.writerow(my_list)
#    y_writer.writerow(my_list)

# experiment #2
# rule: sum across the 3 dimensions of x_t
# proves we can handle dimensionality in the input, and NN works across dimensions
#for i in range(1000000):
#    my_list = np.random.randint(2, size=10)
#    x_writer.writerow(my_list)
#    num = 0
#    for _ in my_list:
#        num += _
#    if num < 5:
#        my_list = [0]
#    if num >= 5:
#        my_list = [1]
#    y_writer.writerow(my_list)
#    #y_writer.writerow(np.random.randint(2, size=1))

# experiment #3
# now we want to test rules across timesteps
# the average of t-4 and t-5 decides t
# next we will want to test at long time steps and measure against num_steps in model
# result: interesting!! this one takes longer to converge but it does ultimately converge
# on multiple trials, it does seem possible for this one to get hung up but only over one epoch
#temp_list = np.random.randint(2, size=5)    
#for i in range(1000000):
#    x = [np.random.randint(2)]
#    x_writer.writerow(x)
#    past_timesteps = temp_list[0] + temp_list[1]
#    if past_timesteps == 1:
#        y = [1]
#        y_writer.writerow(y)
#    elif past_timesteps == 0 or past_timesteps == 2:
#        y = [0]
#        y_writer.writerow(y)
#    else:
#        raise ValueError
#    temp_list[:-1] = temp_list[1:]
#    temp_list[-1] = x[0]

# experiment #4
# testing time and dimensionality
# like last one, but here we take two elements from 5 dimensional x at timesteps t-5 and t-4

#temp_list = []
#temp_list = np.random.randint(2, size=(5,5))    
#for i in range(1000000):
#    x = np.random.randint(2, size=5)
#    x_writer.writerow(x)
#    past_timesteps = temp_list[0][0] + temp_list[1][4]
#    if past_timesteps == 1:
#        y = [1]
#        y_writer.writerow(y)
#    elif past_timesteps == 0 or past_timesteps == 2:
#        y = [0]
#        y_writer.writerow(y)
#    else:
#        raise ValueError
#    temp_list[:-1] = temp_list[1:]
#    temp_list[-1] = x

#Results: wow, most times gets stuck at what appears to be a local min (.69), but sometimes gets it, results below
# possible factors: compute time, learning rate, num_steps
# tried it with num_steps = 5, never converged, maybe just got unlucky
# YES! changing learning rate from 0.1 to 0.2 got convergence every time, that was it
# retested with num_steps = 5, seems pretty clearly stuck 
# num_steps = 6 can get it, but not always, and can revert back between epochs
# keep in mind that's something that can happen between epochs, might need some saved model to revert to
# if we get a bad epoch
# num_steps = 10 seems to be about the sweetspot, if we go larger, then we'll need more data
# or perhaps, changing batch size will make up for it, let's test that
# with num_steps = 15 and a batch size of 100 instead of 200 works each time tested
# clearly starting to see we need a long enough num_steps to capture, but also need enough data, which you can eat up quick

# experiment #5
# chaning num_classes from 2 to 3
# great success, num_steps = 10, learning_rate = 0.2, batch_size = 100, state_size = 8 crushes this
# so next we change x dim to 7, with the intent to reduce state size below 7 to see if that screws it up
# worth noting that 7 works with state_size = 8
# this breaks it, get's stuck at .50, which is good, makes sense that we need more neurons the greater x dim
# next we increased x dim to 20, state size to 25, and sure enough it worked

#temp_list = []
#temp_list = np.random.randint(2, size=(5,20))    
#for i in range(1000000):
#    x = np.random.randint(2, size=20)
#    x_writer.writerow(x)
#    past_timesteps = temp_list[0][0] + temp_list[1][4]
#    if past_timesteps == 1:
#        y = [1]
#        y_writer.writerow(y)
#    elif past_timesteps == 0: 
#        y = [0]
#        y_writer.writerow(y)
#    elif past_timesteps == 2:
#        y = [2]
#        y_writer.writerow(y)
#    else:
#        raise ValueError
#    temp_list[:-1] = temp_list[1:]
#    temp_list[-1] = x

# experiment #6
# now let's see what happens when we move the inputs away from 0 to 2000-2020
# that broke it, which is good news, because it could explain why the model didn't do well with the lobster data
# let's try with fewer dimensions and see if that makes a difference (from 20 to 1)
# that didn't work 
# let's try with smaller numbers
# and that worked, so if x is 5dim with values of 0,1,2 it will work
# but it fails at x belongs to [0,8], suggesting we can't stray too far from inputs of 0, normalization and pre-
# processing is essential

#temp_list = []
#temp_list = np.random.randint(3, size=(5,5))    
#for i in range(1000000):
#    x = np.random.randint(3, size=5)
#    x_writer.writerow(x)
#    past_timesteps = temp_list[0][0] + temp_list[1][4]
#    if past_timesteps % 3 == 0:
#        y = [0]
#        y_writer.writerow(y)
#    elif past_timesteps % 3 == 1: 
#        y = [1]
#        y_writer.writerow(y)
#    elif past_timesteps % 3 == 2:
#        y = [2]
#        y_writer.writerow(y)
#    else:
#        raise ValueError
#    temp_list[:-1] = temp_list[1:]
#    temp_list[-1] = x
 
# experiment #7
# normalize with mean subraction and normalization
# had to change x type to float32 from int32

# data below seems like an edge case, it converges but high = 3 but not high = 4
###temp_list = []
###temp_list = np.random.randint(0, high=3, size=(5,7))    
###for i in range(1000000):
###    x = np.random.randint(0, high=3, size=7)
###    processed_x = x #- 2009.5  
###    #processed_x = processed_x / 5.77
###    #print(x)
###    #print(processed_x)
###    x_writer.writerow(processed_x)
###    past_timesteps = temp_list[0][0] + temp_list[1][4]
###    if past_timesteps % 3 == 0:
###        y = [0]
###        y_writer.writerow(y)
###    elif past_timesteps % 3 == 1: 
###        y = [1]
###        y_writer.writerow(y)
###    elif past_timesteps % 3 == 2:
###        y = [2]
###        y_writer.writerow(y)
###    else:
###        raise ValueError
###    temp_list[:-1] = temp_list[1:]
###    temp_list[-1] = x
 

# experiment #8
# a spread from 0 to 4 broke convergence, but the same size spread from -1 to 3 worked
# this suggests that mean centering has an effect 
# next we'll test bigger spreads around the mean
#temp_list = []
#temp_list = np.random.randint(-1, high=3, size=(5,7))    
#for i in range(1000000):
#    x = np.random.randint(-1, high=3, size=7)
#    processed_x = x #- 2009.5  
#    #processed_x = processed_x / 5.77
#    #print(x)
#    #print(processed_x)
#    x_writer.writerow(processed_x)
#    past_timesteps = temp_list[0][0] + temp_list[1][4]
#    if past_timesteps % 3 == 0:
#        y = [0]
#        y_writer.writerow(y)
#    elif past_timesteps % 3 == 1: 
#        y = [1]
#        y_writer.writerow(y)
#    elif past_timesteps % 3 == 2:
#        y = [2]
#        y_writer.writerow(y)
#    else:
#        raise ValueError
#    temp_list[:-1] = temp_list[1:]
#    temp_list[-1] = x

# experiment 9
# how far out can we go if we're mean centered?
# [-2, 2] doesn't work, tested with a variety of different hyperparameters
# does this mean the data has to be [-1, -1]
# that seems wrong to me


temp_list = []
temp_list = np.random.randint(-1, high=2, size=(5,7))    
for i in range(1000000):
    x = np.random.randint(-1, high=2, size=7)
    processed_x = x #- 2009.5  
    processed_x = processed_x 
    #print(x)
    #print(processed_x)
    x_writer.writerow(processed_x)
    past_timesteps = temp_list[0][0] + temp_list[1][4]
    if past_timesteps % 3 == 0:
        y = [0]
        y_writer.writerow(y)
    elif past_timesteps % 3 == 1: 
        y = [1]
        y_writer.writerow(y)
    elif past_timesteps % 3 == 2:
        y = [2]
        y_writer.writerow(y)
    else:
        raise ValueError
    temp_list[:-1] = temp_list[1:]
    temp_list[-1] = x




