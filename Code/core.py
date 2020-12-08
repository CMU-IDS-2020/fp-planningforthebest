
import numpy as np
import pandas as pd
from modAL.models import ActiveLearner
from modAL.uncertainty import entropy_sampling
from sklearn.linear_model import LogisticRegression
import numpy_indexed as npi
from Survey.Binary_D_Features import *
from Survey.RF_TO_CSV import *
from db.Database import *
from sklearn.ensemble import RandomForestClassifier

class Core():
    def __init__(self):
        self.X_pool = question_generator()

        #cold start, just dummy variable for the baseline

        training = [0,1023]
        labels=[1,0]

        #convert decial to binary 
        training = [ np.matrix(list(list('{0:010b}'.format(i)))).astype(int) for i in training]

        self.labels = np.array(labels)
        self.training_data = np.concatenate( training, axis=0 )
        self.start_bool = False 
        self.start_hold = None 
        #learner of active learning
        self.learner = ActiveLearner(
            estimator=RandomForestClassifier(n_estimators= 300),#LogisticRegression(C=1e5, solver='lbfgs'), #LogisticRegression(),
            X_training=self.training_data, y_training=np.array(labels).astype(int)
        )

        self.values = dict()
        self.user_name = ""
        self.answers = list()
        self.input_hold = None
        self.Dynamic_question = None

    def set_websocket(self, websocket):
        self.websocket = websocket

    def write_message(self, response):
        self.websocket.write_message(response)

    def handle_message(self, message):

        #print(self.training_data)
        if message.split(",")[0] == 'submit':
            feedback = message[message.index(",")+1:]
            rst = eval(self.learner, self.X_pool)
            self.write_message(rst)


            #disabling db connection for local testing
            # importances = pd.read_csv("static/training20.csv")["Importance"].to_list()
            # try:
            #     db = Database()
            #     db.insertFeatureImportance([self.user_name]+list(importances))
            #     db.insertFeedback([self.user_name, feedback])
            #     db.insertAnswers([self.user_name]+self.answers)
            #     db.closeConnection()
            # except Exception as e: 
            #     print(e)

        elif message.split(",")[0] == 'evaluate':
            score = message.split(",")[1]
            # print(score)
            # try:
            #     db = Database()
            #     db.insertEval([self.user_name, score])
            #     db.closeConnection()
            # except Exception as e: 
            #     print(e)

        else:

            answer, question_idx = message.split(',')

            if question_idx == "0":
                #the answer contains name
                self.user_name = answer
                self.X_pool = question_generator()

                # cold start, just dummy variable for the baseline

                training = [0, 1023]
                labels = [1, 0]

                # convert decial to binary
                training = [np.matrix(list(list('{0:010b}'.format(i)))).astype(int) for i in training]

                self.labels = np.array(labels)
                self.training_data = np.concatenate(training, axis=0)
                self.start_bool = False
                self.start_hold = None
                # learner of active learning
                self.learner = ActiveLearner(
                    estimator=RandomForestClassifier(n_estimators=300),
                    # LogisticRegression(C=1e5, solver='lbfgs'), #LogisticRegression(),
                    X_training=self.training_data, y_training=np.array(labels).astype(int)
                )

                self.values = dict()
                self.answers = list()
                self.input_hold = None
                self.Dynamic_question = None

            else:
                #input_hold = self.X_pool[query_idx].reshape(self.training_data[0].shape)
                #print(input_hold)
                #print(self.X_pool[query_idx].reshape())
                self.training_data=np.append(self.training_data,self.input_hold,axis =0 )
                # print(self.training_data)
                
                if answer == "yes":
                    y_new  = "1"
                else:
                    y_new  = "0"

                self.labels = np.append(self.labels,int(y_new))

                if y_new == "1":
                    que,ans = T_Yes(self.Dynamic_question)
                    que = npi.difference(que, self.training_data)
                    ans = np.ones((1,que.shape[0]))
                    self.training_data=np.append(self.training_data,que,axis =0 )
                    self.labels = np.append(self.labels,ans)

                if y_new == "0":
                    que,ans = T_No(self.Dynamic_question)
                    que = npi.difference(que, self.training_data)
                    ans = np.zeros((1,que.shape[0]))
                    self.training_data=np.append(self.training_data,que,axis =0 )
                    self.labels = np.append(self.labels,ans)

                #Store question string and label
                
                self.answers.append(flatten_targets_to_string(self.query_inst)+y_new)
                
                #remove inferible questions
                self.X_pool = npi.difference(self.X_pool, self.training_data)

                #got the answer move to next question
                self.start_bool = False

                #print(self.training_data)
                #print(self.labels)
    



            if self.start_bool: 
                self.query_inst = self.start_hold
                self.start_bool = False
            else:
                self.learner.teach(self.training_data,np.array(self.labels).astype(int))

                #find query idx and instance
                query_idx, self.query_inst = self.learner.query(self.X_pool)

                self.start_bool = True
                self.start_hold = self.query_inst    

            self.input_hold = self.query_inst.reshape(self.training_data[0].shape)

            #convert the feature vectors to matrix, eg [1 1] -> [1 0 ]; [0 1]
            self.query_inst = multi_2_one(self.query_inst)

            #find the questions and get resposne
            self.Dynamic_question = tuple([inv_features[str(i)] for i in self.query_inst])
            question_hold = askQuestion(self.Dynamic_question)

            #add to the trainning data
            if int(question_idx) > 0:
                # RF_plot(self.training_data, self.labels, "training" + question_index + ".jpg")
                RF_Features_Importance(self.training_data, self.labels, "static/training" + question_idx + ".csv")

            self.write_message(str(question_hold))

