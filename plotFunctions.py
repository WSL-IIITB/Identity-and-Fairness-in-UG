from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from ultimatum_v2 import ultimatum_v2
from transcendent_fair_agent import trans_agent

def matrix(agent_parameter='gamma', value=1):
    para_prop = 1*list(np.arange(0,1.1,0.1))
    para_arb = 1*list(np.arange(0,1.1,0.1))
    matrix = np.zeros((11,11))
    for i in range(0,len(para_prop)):
        for j in range(0,len(para_arb)):
            game = ultimatum_v2(1, agent={'proposer':{agent_parameter:para_prop[i]}, 'arbiter':{agent_parameter:para_arb[j]}})
            game_result = game.game()
            if game_result[2]!=0:
                matrix[i][j] = game_result[value]
            else:
                matrix[i][j] = -1
    return matrix

def matrix_agent(para1 = 'gamma', para2 = 'fair_thresh', value=1):
    parameter1 = 1*list(np.arange(0,1.1,0.1))
    parameter2 = 1*list(np.arange(0,1.1,0.1))
    matrix = np.zeros((11,11))
    for i in range(0,len(parameter1)):
        for j in range(0,len(parameter2)):
            game = ultimatum_v2(1, proposer=trans_agent({para1:parameter1[i],para2:parameter2[j]}))
            game_result = game.proposer_decision()
            matrix[i][j] = 2*game_result - 1 
            # fairscore_agent = game.agent_fair_score(game_result[0])
            # if game_result[2]!=0:
            #     matrix[i][j] = game_result[0] - game_result[1]
            # else:
            #     matrix[i][j] = -2
    return matrix

def matrix_arbiter(para1 = 'gamma', para2 = 'fair_thresh', value=1):
    parameter1 = 1*list(np.arange(0,1.1,0.1))
    parameter2 = 1*list(np.arange(0,1.1,0.1))
    matrix = np.zeros((11,11))
    for i in range(0,len(parameter1)):
        for j in range(0,len(parameter2)):
            game = ultimatum_v2(1, arbiter=trans_agent({para1:parameter1[i],para2:parameter2[j]}))
            game_result = game.arbiter_mao()
            # fairscore_agent = game_result[1]
            matrix[i][j] = 2*game_result - 1
            # if game_result[2]!= 0:
            #     matrix[i][j] = 2*game_result - 1
            # else:
            #     matrix[i][j] = -2
    return matrix

def matrix_plot(matrix, parameter = 'gamma'):
    fig, ax = plt.subplots()
    cmap = ListedColormap(["tomato", "lightgreen", "limegreen","green"])
    cax = ax.matshow(matrix.T, cmap=cmap)
    fig.colorbar(cax)
    for i in range(11):
        for j in range(11):
            c = round(matrix[i,j],1)
            ax.text(i, j, str(c), va='center', ha='center')
    ax.set_xlabel(parameter + " Proposer")
    ax.set_ylabel(parameter + " Arbiter")

def matrix_plot_agent(matrix, para1 = 'gamma', para2 = 'fair_thresh', agent_type = 'proposer'):
    fig, ax = plt.subplots()
    cmap = ListedColormap(["tomato", "lightgreen", "limegreen",'mediumseagreen','forestgreen', "green"])
    cax = ax.matshow(matrix.T, cmap='Reds_r')
    fig.colorbar(cax)
    for i in range(11):
        for j in range(11):
            c = round(matrix[i,j],1)
            ax.text(i, j, str(c), va='center', ha='center')
    ax.set_xlabel(para1 + " " + agent_type)
    ax.set_ylabel(para2 + " " + agent_type)

def matrix_plot_arbiter(matrix, para1 = 'gamma', para2 = 'fair_thresh', agent_type = 'proposer'):
    fig, ax = plt.subplots()
    cmap = ListedColormap(["lightgreen", "limegreen","forestgreen","green"])
    cax = ax.matshow(matrix.T, cmap='Reds_r')
    fig.colorbar(cax)
    for i in range(11):
        for j in range(11):
            c = round(matrix[i,j],1)
            ax.text(i, j, str(c), va='center', ha='center')
    ax.set_xlabel(para1 + " " + agent_type)
    ax.set_ylabel(para2 + " " + agent_type)