#Part of this script was developed during CAAR REU 2019.
#file to check the rationality 

import numpy as np
from itertools import combinations
from random import sample, shuffle
import pandas as pd
features = {
"One sided body paralysis " : np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0]), # partial body paralysis
"Impaired voice, unable to speak coherent words " : np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
"Impaired eating requiring use of a feeding tube " : np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
"Impaired vision " : np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
"Impaired cognitive ability such as severe memory loss, difficulty expressing yourself, difficulty reasoning " : np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
"Impaired perception and orientation to surroundings " : np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
"Impaired self-care ability, e.g. difficulty dressing yourself " : np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
"Incontinence " : np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
"Impaired control of emotions " : np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
"Impaired sexual ability " : np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
}
columns =[ 
                "One sided body paralysis ",
                "Impaired voice, unable to speak coherent words ",
                "Impaired eating requiring use of a feeding tube ",
                "Impaired vision ",
                "Impaired cognitive ability such as severe memory loss, difficulty expressing yourself, difficulty reasoning ",
                "Impaired perception and orientation to surroundings ",
                "Impaired self-care ability, e.g. difficulty dressing yourself " ,
                "Incontinence " ,
                "Impaired control of emotions ",
                "Impaired sexual ability ",
                "Labels" 
            ]
outstr = """ 
    
    Welcome!
    
    The 05839 Planningforthebest group will be using the data collected from this survey to test
    various assumptions about human preferences, and to test various inference methods.  
    
    For every question, suppose that you suffered a stroke.  You are currently unconscious and thus unable to communicate.  
    A doctor makes the assessment that if you were to regain consciousness, then with high probability you will suffer 
    from some disabilities or ailments specific to each question.  You are then asked whether or not you would want to 
    receive life-sustaining support in this scenario. 
    
    Please answer as accurately and honestly as possible.   

    """
h_class = {
    '0' : 'NO',
    '1' :'Yes'
}
inv_features = {str(v): k for k, v in features.items()}
all_q = list(combinations(features.keys(), 1))
for i in range(1,int(9)):
    all_q += list(combinations(features.keys(), i+1))



def question_generator():
    """
    generate question matrix 1023*10
    
    """

    X_pool = []

    for question in all_q:
        X_pool.append(sum(features[symptom] for symptom in question).tolist())
    X_pool = np.array(X_pool)

    return X_pool 

def askQuestion(nodes_list):
    """
    Displays a question and gathers a response
    :param nodes_list: a list of nodes to inquire about
    :return: the value (1 for yes, 0 for no)
    """

    out_str_begin = "Suppose that if you regained consciousness, you would have ALL below -  "
    out_str_end = " *Would you still want to receive life-sustaining care?"

    # Add nodes to ask about.
    for i in range(len(nodes_list)):
        out_str_begin = out_str_begin + "*" + nodes_list[i][0] + nodes_list[i][1:] + "; "


    
    out_str_begin = out_str_begin + out_str_end 


    

    return  out_str_begin



def multi_2_one(vector):
    """
    decmpose instance vector to matrix of one hot encoding
    """
    index = np.where(vector[0] == 1)
    nb_classes = 10
    targets = index[0].reshape(-1)
    one_hot_targets = np.eye(nb_classes)[targets]
    one_hot_targets  = one_hot_targets.astype(int)
    return one_hot_targets


def flatten_targets_to_string(matrix):
    return "".join([str(x) for x in np.sum(matrix, axis=0)])

def T_No(question):
    """
    Function to encode transitivty of No
    """
    global all_q
    responses =[]

    To_add = [q for q in all_q if set(question).issubset(q)]
    responses += [0] * len(To_add)

    #result of the array
    result = []
    for q in To_add:
        result.append(sum(features[symptom] for symptom in q).tolist())
    return np.array(result), np.array(responses)


def T_Yes(question): 
    """
    Function to encode transitivty of Yes
    """
    global all_q
    responses =[]

    To_add = [q for q in all_q if set(q).issubset(question)]
    responses += [1] * len(To_add)
    
    #result of the array
    result =[]
    for q in To_add:
        result.append(sum(features[symptom] for symptom in q).tolist())
    return np.array(result), np.array(responses)

"""
Model:  learner in the core script 
pool:  X_pool in the core script (need more dicsussion since X_pool automatically get rid of the transitivity)
"""
def eval(model,pool):
    if pool.shape[0] < 10:
        X_test = pool
    else:
        X_test = pool[np.random.choice(pool.shape[0], 10, replace=False)]

    df = pd.DataFrame(columns=["Question", "Probability","Labels"])

    q_hold = []
    for q in X_test:
        query_inst = multi_2_one(q.reshape((1,q.shape[0])))
        Dynamic_question = tuple([inv_features[str(i)] for i in query_inst])
        #askQuestion(Dynamic_question)
        q_hold.append(askQuestion(Dynamic_question))

    df["Question"] = q_hold

    probability = model.predict_proba(X_test)[:,1]
    df["Probability"] = probability

    labels = model.predict(X_test)
    df["Labels"] = labels
    rst = ""
    for index, row in df.iterrows():
        if row['Labels'] == 1:
            answer = "YES"
        else:
            answer = "NO"
        question = row['Question']
        question = question.replace('*', '')
        rst += question + " \tYOUR PREDICTED ANSWER: " + answer
        rst += "\n"
    return rst