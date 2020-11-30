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
header = [  "Paralysis ", "Voice ",
"Feeding_Tube " ,
 "Vision ",
"Cognitive " ,
"Perception " ,
"Dressing " ,
"Incontinence " ,
"Emotions ",
 "Sex " ]
#feature importance plot 
def RF_plot(X,Y,outputfile="result.jpg"):

	forest = ExtraTreesClassifier(n_estimators=30,
	                              random_state=42)

	forest.fit(X, Y)
	importances = np.matrix(forest.feature_importances_)
	std = np.std([tree.feature_importances_ for tree in forest.estimators_],
	             axis=0)
	df = pd.DataFrame(data = importances,  
                  index = ["ROW1"],
                  columns = header) 

	df.to_csv("RF.csv",index=False)
'''
total = pd.read_csv("Survey_Results.csv")
X = total.iloc[:,:10]
Y= total.iloc[:,10]
RF_plot(X,Y)
'''