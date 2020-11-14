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
#total = pd.read_csv("Survey_Results.csv")
#feature importance plot 
def RF_plot(X,Y):
	#X = np.array(total)[:,:10].astype('int')
	#Y = np.array(total)[:,10].astype('int')
	forest = ExtraTreesClassifier(n_estimators=30,
	                              random_state=42)

	forest.fit(X, Y)
	importances = forest.feature_importances_
	std = np.std([tree.feature_importances_ for tree in forest.estimators_],
	             axis=0)
	indices = np.argsort(importances)[::-1]

	# Print the feature ranking
	print("Relative Feature Ranking:")

	for f in range(X.shape[1]):
	    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

	# Plot the feature importances of the forest
	plt.figure(figsize=(100, 30), dpi=30)

	plt.title("Relative Feature Importances")
	plt.bar(range(X.shape[1]), importances[indices],
	       color="r", yerr=std[indices], align="center")
	result = [features[str(i)] for i in indices]
	plt.xticks(range(X.shape[1]), result, fontsize=14)
	plt.xlim([-1, X.shape[1]])
	plt.savefig('result.jpg')
	plt.show()