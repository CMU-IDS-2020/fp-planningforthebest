import pandas as pd
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier
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

	forest = ExtraTreesClassifier(n_estimators=30,
	                              random_state=42)

	forest.fit(X, Y)
	importances = np.matrix(forest.feature_importances_).tolist()[0]

	df = pd.DataFrame(list(zip(header,importances)),
             
                  columns = ["Features","Importance"]) 

	df.to_csv(outputfile,index=False)

#Testing 
"""
total = pd.read_csv("Survey_Results.csv")
X = total.iloc[:,:10]
Y = total.iloc[:,10]
RF_Features_Importance(X,Y)
"""
