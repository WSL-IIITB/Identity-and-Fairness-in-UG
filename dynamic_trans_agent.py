import numpy as np
# from softmax import *
import matplotlib.pyplot as plt
import random
class DynamicTransAgent(object):
    def __init__(self,attr={},identity={}):
        if 'gamma' in attr:
            self.gamma = attr['gamma']
        else:
            self.gamma = 0.35
        # if 'distance' in attr:
        #     self.distance = attr['distance']
        # else:
        #     self.distance = 1
        # if any(identity):
        self.identity = identity
        expec = {}
        for i in self.identity:
            distance = self.identity[i]
            expec[i] = -np.power(self.gamma,distance+1)/(distance+1)
        self.expectations = expec
            # self.expectation = 0
        # if 'fair_thresh' in attr:
        #     self.fair_thresh = attr['fair_thresh']
        # else:
        #     self.fair_thresh = 0.5
        fair_thresh = {}
        for i in self.identity:
            d = self.identity[i]
            fair_thresh[i] = 1-np.power(self.gamma,d)
            # print(i, self.fair_thresh[i])
        self.fair_thresh = fair_thresh
        # print("fair ", self.fair_thresh)
        self.attrs = {'gamma':self.gamma}
        
    def getAttrs(self):
        return self.attrs, self.identity
    
    def setExpectations(self):
        expec = {}
        for i in self.identity:
            distance = self.identity[i]
            # expec[i] = -np.power(self.gamma,distance)/(np.log(self.gamma))
            expec[i] = -self.gamma*distance
        self.expectations = expec
    
    def setFairThresh(self):
        fair_thresh = {}
        for i in self.identity:
            d = self.identity[i]
            fair_thresh[i] = round(1-np.power(self.gamma,d),2)
            # print(i, self.fair_thresh[i])
        self.fair_thresh = fair_thresh
    
    def setIdentity(self, identity):
        self.identity = identity
        self.setExpectations()
        # self.setFairThresh()
        return self.identity
    
    def getDistance(self, index):
        return self.identity[index]
    
    def sigmoid(self, x):
        if x>=0:
            return ((np.exp(30*x)/(2*(np.exp(30*x))+2)) - 0.25)
        if x<0:
            return (1*(np.exp(20*x)/((np.exp(20*x))+1)) - 0.5)
    
    def fair_sigmoid(self,x):
        if x>=0:
            return ((np.exp(12*x)/(1*(np.exp(12*x))+1)) - 0.50)
        if x<0:
            return (2*(np.exp(10*x)/((np.exp(10*x))+1)) - 1)

    def utility_computation(self, my_payoff, other_payoff, other_index):
        distance = self.identity[other_index]
        fair_my = self.fair_sigmoid(my_payoff-self.fair_thresh[other_index])
        fair_other = self.fair_sigmoid(other_payoff-(self.fair_thresh[other_index]))
        # print(fair_my, fair_other)
        return (fair_my + np.power(self.gamma, distance)*(fair_other))/(1+np.power(self.gamma, distance))
    
    def satisfaction_score(self, my_payoff, other_payoff, other_index):
        utility = self.utility_computation(my_payoff, other_payoff, other_index)
        satisfaction = utility - self.expectations[other_index]
        # print(other_index, utility, self.expectations[other_index])
        satis_score = self.fair_sigmoid(satisfaction)
        # satis_score = utility
        return satis_score
    
    def find_key(self, input_dict, value):
        return {k for k, v in input_dict.items() if v == value}

    def findMinAcceptable(self, splitDict):
        splits = list(splitDict.keys())
        utility = list(splitDict.values())
        y = -2
        x = -2
        for i in utility:
            if i>=0:
                y = i
                x = list(self.find_key(splitDict,y))[0]
                break
        if y == -2:
            y= max(utility)
            x = list(self.find_key(splitDict,y))[0]
        return y, x

    def minAccept(self, indexProp):
        split_util = {}
        for split in np.arange(0,1.1,0.1):
            my_split = split
            other_split = 1-split
            split_util[split] = self.utility_computation(my_split, other_split, indexProp)
        acceptUtility, acceptSplit = self.findMinAcceptable(split_util)

        return acceptSplit, acceptUtility

    def decision(self, splitDict): 
        splits = list(splitDict.keys())
        utility = list(splitDict.values())
        # if splitDict == {}:
        #     print("what the hell are you doing")
        choiceUtil = max(utility)
        choice = list(self.find_key(splitDict,choiceUtil))[0]
        # return [y], [x]     
        # util_list = list(choice_dict.values())
        # choice_list = list(choice_dict.keys())
        # prob = softmax(np.array(util_list))
        # print("dict ", choice_dict)
        # print("prob ", prob)

        # cumProb =[prob[0]]
        # for i in range(1,len(prob)):
        #     cumProb.append(prob[i] + cumProb[i-1])
        # random.seed = 33
        # choice = random.choices(choice_list, cum_weights=cumProb, k=1)[0]
        # choiceUtil = choice_dict[choice]

        # choiceUtil = util_list[prob.argmax()]
        # choice = choice_list[prob.argmax()]
        return choice, choiceUtil
    
    def fair_normalized(self, my_payoff):
        fair_my = self.fair_sigmoid(my_payoff-self.fair_thresh)
        return fair_m