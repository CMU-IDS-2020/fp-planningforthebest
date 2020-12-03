import numpy as np
import pandas as pd
from modAL.models import ActiveLearner
from modAL.uncertainty import entropy_sampling
from sklearn.linear_model import LogisticRegression
import numpy_indexed as npi
from Survey.Binary_D_Features import *
from Survey.RF_Feature_Plot import *
from Survey.RF_TO_CSV import *
from db.Database import *

class Core():
    def __init__(self):
        self.X_pool = question_generator()

        #cold start, just dummy variable for the baseline 
        training = [256,1023]
        labels=[1,0]

        #convert decial to binary 
        training = [ np.matrix(list(list('{0:010b}'.format(i)))).astype(int) for i in training]

        self.labels = np.array(labels)
        self.training_data = np.concatenate( training, axis=0 )

        #learner of active learning
        self.learner = ActiveLearner(
            estimator=LogisticRegression(C=1e5, solver='lbfgs'),
            X_training=self.training_data, y_training=np.array(labels).astype(int)
        )

        self.values = dict()
        self.answers = list()
        

    def set_websocket(self, websocket):
        self.websocket = websocket

    def write_message(self, response):
        self.websocket.write_message(response)

    def handle_message(self, message):
        print(message)
        if message.split(",")[0] == 'submit':
            feedback = message[message.index(",")+1:]
            importances = RF_plot(self.training_data, self.labels)
            self.write_message("plot generated")

            #disabling db connection for local testing
            # db = Database()
            # db.insertFeatureImportance([self.values.get("user_name")]+list(importances))
            # db.insertFeedback([self.values.get("user_name"), feedback])
            # db.insertAnswers([self.values.get("user_name")]+self.answers)
            # db.closeConnection()

        else:
            self.learner.teach(self.training_data,np.array(self.labels).astype(int))

            #find query idx and instance
            query_idx, query_inst = self.learner.query(self.X_pool)

            #convert the feature vectors to matrix, eg [1 1] -> [1 0 ]; [0 1]
            query_inst = multi_2_one(query_inst)

            #find the questions and get resposne
            Dynamic_question = tuple([inv_features[str(i)] for i in query_inst])
            question_hold = askQuestion(Dynamic_question)
            #add to the trainning data
            self.training_data=np.append(self.training_data,self.X_pool[query_idx],axis =0 )

            answer, question_idx = message.split(',')

            if question_idx == "0":
                #the answer contains name
                self.values["user_name"] = answer

            if answer == "yes":
                y_new  = "1"
            else:
                y_new  = "0"
            self.labels = np.append(self.labels,int(y_new))

            if y_new == "1":
                que,ans = T_Yes(Dynamic_question)
                que = npi.difference(que, self.training_data)
                ans = np.ones((1,que.shape[0]))
                self.training_data=np.append(self.training_data,que,axis =0 )
                self.labels = np.append(self.labels,ans)

            if y_new == "0":
                que,ans = T_No(Dynamic_question)
                print(flatten_targets_to_string(query_inst))
                que = npi.difference(que, self.training_data)
                ans = np.zeros((1,que.shape[0]))
                self.training_data=np.append(self.training_data,que,axis =0 )
                self.labels = np.append(self.labels,ans)

            #Store question string and label
            self.answers.append(flatten_targets_to_string(query_inst)+y_new)

            #remove inferible questions
            self.X_pool = npi.difference(self.X_pool, self.training_data)

            print(self.training_data.shape)
            print(self.labels.shape)

            if int(question_idx) > 0:
                # RF_plot(self.training_data, self.labels, "training" + question_index + ".jpg")
                RF_Features_Importance(self.training_data, self.labels, "static/training" + question_idx + ".csv")

            #print("The answer of question " + str(question_id) + " is " + answer)

            self.write_message(str(question_hold))