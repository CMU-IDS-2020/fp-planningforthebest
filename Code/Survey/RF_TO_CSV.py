import pandas as pd
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

'''
Author Weiqin Wang
date 07/13/2019  part of script developed during NSF REU CAAR 2019 DICKERSON GROUP
'''
features = {
"0":"Paralysis ", # partial body paralysis
"1":"Voice ",
"2":"Feeding_Tube " ,
"3": "Vision ",
"4": "Cognitive " ,
"5": "Perception " ,
"6": "Dressing " ,
"7":"Incontinence " ,
"8": "Emotions ",
"9" : "Sex " ,
}
header = [  "Paralysis ", 
			"Voice ",
			"Feeding_Tube " ,
			 "Vision ",
			"Cognitive " ,
			"Perception " ,
			"Dressing " ,
			"Incontinence " ,
			"Emotions ",
			 "Sex " ]
#feature importance plot 

def RF_Features_Importance(X,Y,outputfile="RF.csv"):
	forest = RandomForestClassifier(n_estimators= 300)
	forest.fit(X, Y)
	importances = np.matrix(forest.feature_importances_).tolist()[0]
	df = pd.DataFrame(list(zip(header,importances)),
             
                  columns = ["Features","Importance"]) 

	df.to_csv(outputfile,index=False)
'''
def RF_Features_Importance(X,Y,outputfile="RF.csv"):
	model = LogisticRegression(C=1e5, solver='lbfgs').fit(X, Y)


	r = permutation_importance(model, X, Y, n_repeats=30 ,random_state=0)
	print(r)

	df = pd.DataFrame(list(zip(header,importances)),
             
                  columns = ["Features","Importance"]) 

	df.to_csv(outputfile,index=False)
'''
#Testing 
"""
total = pd.read_csv("Survey_Results.csv")
X = total.iloc[:,:10]
Y = total.iloc[:,10]
RF_Features_Importance(X,Y)
"""
