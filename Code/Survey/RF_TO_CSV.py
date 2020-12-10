import pandas as pd
from sklearn.ensemble.forest import RandomForestClassifier
import numpy as np

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

