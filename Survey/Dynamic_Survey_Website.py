#!/usr/bin/env python
"""
Author: Weiqin Wang
Active Learning using simple Uncertainty Sampling, part of script developed during NSF REU CAAR 2019 DICKERSON GROUP  
"""
import numpy as np
import pandas as pd
from modAL.models import ActiveLearner
from modAL.uncertainty import entropy_sampling
from sklearn.linear_model import LogisticRegression
import numpy_indexed as npi
from Binary_D_Features import *
from RF_Feature_Plot import * 


def Dynamic_survey(training,labels):
    """
    Functin to survey, question asking from Binary_D_Features 
    Function return the Dataframe of the questions and surveyed results
    """

    #global sampling pool 
    X_pool = question_generator()

    #print the starting prompt 
    print(outstr)


    #cold start, just dummy variable for the baseline 
    training = [256,1023]
    labels=[1,0]

    #convert decial to binary 
    training = [ np.matrix(list(list('{0:010b}'.format(i)))).astype(int) for i in training]

    labels = np.array(labels)
    training_data = np.concatenate( training, axis=0 )

    #learner of active learning
    learner = ActiveLearner(
        estimator=LogisticRegression(C=1e5, solver='lbfgs'),
        X_training=training_data, y_training=np.array(labels).astype(int)
    )


    #saves the directresult 
    returnhold = [] 

    for q in range(30):

        #teach entropy based active learning 
        learner.teach(training_data,np.array(labels).astype(int))

        #find query idx and instance 
        query_idx, query_inst = learner.query(X_pool)  

        #remove the sampled data from data pool     
        #X_pool= X_pool[np.setdiff1d(np.arange(X_pool.shape[0]),query_idx)]

        returnhold.append(query_inst) 

        #convert the feature vectors to matrix, eg [1 1] -> [1 0 ]; [0 1]
        query_inst = multi_2_one(query_inst)



        #find the questions and get resposne 
        Dynamic_question = tuple([inv_features[str(i)] for i in query_inst])
        y_new = askQuestion(Dynamic_question)
        returnhold[-1] = np.append(returnhold[-1], int(y_new))

        #add to the trainning data
        training_data=np.append(training_data,X_pool[query_idx],axis =0 )



        #add labels to it
        labels = np.append(labels,int(y_new))

        #Add transitivity
        if y_new == "1":
            que,ans = T_Yes(Dynamic_question)
            que = npi.difference(que, training_data)
            ans = np.ones((1,que.shape[0]))
            training_data=np.append(training_data,que,axis =0 )
            labels = np.append(labels,ans)

        if y_new == "0":
            que,ans = T_No(Dynamic_question)
            que = npi.difference(que, training_data)
            ans = np.zeros((1,que.shape[0]))
            training_data=np.append(training_data,que,axis =0 )
            labels = np.append(labels,ans)

        #remove inferible questions 
        X_pool = npi.difference(X_pool, training_data)
        if X_pool.shape[0] == 0:
            print("You answered %d question, we are done"% q)
            break 

    panda_df = pd.DataFrame(data =returnhold,  columns = columns) 
    RF_plot(training_data, labels)
    return panda_df


results = Dynamic_survey([],[])
#Save to CSV
results.to_csv("Survey_Results.csv", index = False)
