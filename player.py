from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
import numpy as np
import operator

MUT_POS = 0.1
MUT_RANGE = 10

class Player:
    def __init__(self):
        self.score = 0
        self.brain = Sequential()
        self.brain.add(Dense(12, input_dim=34, activation='relu'))
        self.brain.add(Dense(4))
        self.brain.add(Dense(6, activation="sigmoid"))
        self.brain.compile(optimizer="adam", loss="mse")
        
    def move(self, inputs):
        inputs = np.array(inputs)
        prediction = self.brain.predict(inputs.reshape(1,34))[0]
        output = []
        # move prediction
        move_pred = prediction[:3]
        output.append(np.argmax(move_pred)-1)
        # -1 move down, 0 stay, +1 move up

        # shoot prediction
        if prediction[3] < 0.5:
            output.append(0) # do not shoot
        else:
            output.append(1) # shoot

        output.append(prediction[4]) # dx bullet speed
        output.append(2*(prediction[5]-0.5)) # dy bullet speed
        return output

def breed(p_one, p_two):
    p_child = Player()
    p_one_weights = p_one.brain.get_weights()
    p_two_weights = p_two.brain.get_weights()
    
    child_weights = []
    for dad, mum in zip(p_one_weights, p_two_weights):
        curr_weights = []
        for dad_w, mum_w in zip(dad, mum):
            curr_w = 0
            if(not isinstance(dad_w, np.float32)):
                curr_w = []
                for dad_w_w, mum_w_w in zip(dad_w, mum_w):
                    cross_ratio = np.random.uniform()
                    curr_w.append(dad_w_w*cross_ratio + mum_w_w*(1-cross_ratio))
            else:
                cross_ratio = np.random.uniform()
                curr_w = dad_w*cross_ratio + mum_w*(1-cross_ratio)
            curr_weights.append(curr_w) 
        child_weights.append(curr_weights)
    
    p_child.brain.set_weights(child_weights)
    return p_child

def mutate(weight):
    if np.random.uniform() <= MUT_POS:
        mut_ratio = np.random.uniform(-MUT_RANGE, MUT_RANGE)
        weight += weight * mut_ratio
    return weight