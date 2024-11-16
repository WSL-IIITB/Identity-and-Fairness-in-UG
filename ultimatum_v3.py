import numpy as np
# from softmax import *
import matplotlib.pyplot as plt
from dynamic_trans_agent import DynamicTransAgent
import random
import copy
class ultimatum_v3(object):
    def __init__(self,resource_val=1, proposer = DynamicTransAgent(), arbiter= DynamicTransAgent()):
        self.resource_val = resource_val
        self.proposer = proposer
        self.arbiter = arbiter
        propIdentity = {'arbiter':round(random.uniform(0,2),1)}
        arbIdentity = {'proposer':round(random.uniform(0,2),1)}
        random.seed = 32
        self.proposer.identity = propIdentity
        self.arbiter.identity = arbIdentity
        # self.proposer.setIdentity(propIdentity)
        # self.arbiter.setIdentity(arbIdentity)
    
    def find_key(self, input_dict, value):
        return {k for k, v in input_dict.items() if v == value}
    
    def agent_decision(self):
        split_factor = np.arange(0,1.01,0.01)
        utility = {}
        for i in split_factor:
            my_split = i*self.resource_val
            other_split = self.resource_val*(1-i)
            utility[i] = self.proposer.basic_utility_computation(my_split, other_split, 'arbiter')
        return utility

    def proposer_decision(self):
        split_factor = np.arange(0,1.05,0.05)
        satis_score = {}
        utility = {}
        for i in split_factor:
            my_split = i*self.resource_val
            other_split = self.resource_val*(1-i)
            utility[i] = self.proposer.utility_computation(my_split, other_split,'arbiter')
            # satis_score[i] = self.proposer.satisfaction_score(my_split, other_split)
        # print("stais_score ", satis_score)

        # utility_vals = list(utility.values())
        # maxUtility = max(utility_vals)

        # print("utility ", utility)
        # print("max ", maxUtility)

        # split = list(self.find_key(utility, maxUtility))[0]
        # print(self.proposer.get_attrs())

        # decision, decisionUtil = self.proposer.decision(utility)
        # return decision, decisionUtil

        return utility
        # return split
        
        # return decision
    
    def arbiter_decision(self, proposed_split):
        my_split = proposed_split
        other_split = self.resource_val - proposed_split
        utility = self.arbiter.utility_computation(my_split, other_split, 'proposer')
        minAccept, utilAccept = self.arbiter.minAccept('proposer')
        rejectUtil = self.arbiter.utility_computation(0,0,'proposer')
        if utility>=utilAccept:
            decision = 1
            finalUtil = utility
        else:
            # arbUtil = self.arbiter.utility_computation(0,0,'proposer')
            # print("Losing Out ", recvUtil, arbUtil, recvUtil-arbUtil)
            decision = 0
            finalUtil = rejectUtil
        return decision, finalUtil, utilAccept, minAccept
    
    def agent_fair_score(self, split, agent_type = 'proposer'):
        if agent_type=='proposer':
            return self.proposer.fair_normalized(split)
        else:
            return self.arbiter.fair_normalized(split)

    def find_accept(self, split_util):
        utility = list(split_util.values())
        # print(utility)
        return max(utility)
        # if max(utility) >= 0:
        #     return max(utility)
        # else:
        #     y = 0
        #     x_key = utility.index(max(utility))
        #     for i in range(x_key,len(utility)):
        #         if utility[i+1] - utility[i] < 0.04:
        #             return utility[i]

    def arbiter_mao(self):
        split_util = {}
        for split in np.arange(0,1.1,0.1):
            split_util[split] = self.arbiter_decision(split)
        splits = list(split_util.keys())
        utility = list(split_util.values())
        ylist = [j>0 for j in utility]
        # decSplit, decUtil = self.arbiter.decision(split_util)
        accept = self.find_accept(split_util)
        accept_split = list(self.find_key(split_util, accept))[0]
        return accept_split, accept
        # return decSplit, decUtil
        
    
    def game(self):
        proposer_split, propUtil = self.proposer_decision()
        # print(proposer_split)
        arbiter_split = self.resource_val - proposer_split
        recvUtil = copy.deepcopy(self.arbiter.utility_computation(arbiter_split, proposer_split, 'proposer'))
        decision, finalUtil, utilAccept, minAccept = self.arbiter_decision(arbiter_split)
        # print("min accept ", minimum_accept, " arbiter_split ", arbiter_split, " losing out", recvUtil-arbUtil)
        return proposer_split, arbiter_split, decision