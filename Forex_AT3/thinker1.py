import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

class Brain1:
	def __init__(self, numOfWeights):
		self.memories = np.empty((0, numOfWeights+1))
		self.model = np.array([1.0] * numOfWeights)
		self.start = True
		self.xs = 0
		self.prediction = 0

	def step(self, xAr):
		# print("step")
		# print(xAr)

		if self.start == True:
			# xAr * self.model
			# self.model += xAr
			
			self.start = False

		else:
			self.memories = np.append(self.memories, [np.insert(self.xs, 0, xAr[0])], axis = 0)
			# if len(self.memories) > 50:
			# 	self.memories = np.delete(self.memories, 0, 0)

			# predictions = self.NNtrain([xAr])
			# print(predictions)

		self.xs = xAr



	def retMemVals(x, w):
		return np.where(np.logical_and(self.memories < x+w/2 and self.memories > x-w2), self.memories[:,0])

	def apriori(self):
		ys = self.memories[:,0]
		resAr = np.empty((0, len(self.memories[0])-1))

		resAr = []
		for i in range(1, len(self.memories[0])):
			xs = self.memories[:,i]
			temp = np.where(ys[xs>0]>0 ,1,0)
			if len(temp)>0:
				temp = (temp==1).sum() / len(temp)
			else:
				temp = 0
			resAr.append(temp)

		return resAr

	def NNtrain(self, new_X):
		X = self.memories[:,1:]
		y = np.where(self.memories[:,0]>0, 1,0)
		# X_train = X
		# y_train = y
		X_train, X_test, y_train, y_test = train_test_split(X, y)

		scaler = StandardScaler()
		scaler.fit(X_train)

		X_train = scaler.transform(X_train)
		X_test = scaler.transform(X_test)
		# new_X = scaler.transform(new_X)

		# print(X_train)
		# print()
		# print(y_train)

		# print()
		# print("X train length", len(X_train))
		# print("y train length", len(y_train))

		mlp = MLPClassifier(
			hidden_layer_sizes=(
				len(self.memories[0])-1,
				len(self.memories[0])-1,
				len(self.memories[0])-1,
				len(self.memories[0])-1,
				),
			max_iter=500)
		mlp.fit(X_train,y_train)

		predictions = mlp.predict(X_test)
		print()
		print(predictions)
		print(y_test)
		score = mlp.score(X_test, y_test)
		print(score)
		# predictions = mlp.predict(new_X)
		return predictions

		
