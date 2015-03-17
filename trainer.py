import cv2
import numpy as np
import preprocessing
import charmap
import feature_extraction

#-------------------------------Training data creation

def createTrainingData(): # Currently only for two classes
	trainingData = []
	targetData = []

	token_files_array = []

	for x in range(26):
		name_string = "dat/tokens/" + str(charmap.chars[x]) + "_tokens.npy"
		token_array = np.load(name_string)
		token_array = [tok[0] for tok in token_array]
		token_files_array.append(token_array)

	number_of_classes = len(token_files_array)

	for x in range(number_of_classes):
		number_of_tokens = len(token_files_array[x])

		feature_vectors = map(feature_extraction.hog_vector, token_files_array[x])
		# feature_vectors = map(feature_extraction.line_average_vector, token_files_array[x])
		# feature_vectors = map(feature_extraction.simple_pixels_vector, token_files_array[x])

		trainingData.append(feature_vectors)
		char_class = float(x)
		targetData.append([char_class for i in range(number_of_tokens)])

	trainingData = np.array(trainingData).reshape(-1)
	tmp_trainingData = []
	for x in range(len(trainingData)):
		tmp_trainingData += trainingData[x]
	trainingData = np.float32(np.array(tmp_trainingData))

	targetData = np.array(targetData).reshape(-1)
	tmp_targetData = []
	for x in range(len(targetData)):
		tmp_targetData += targetData[x]
	targetData = np.float32(np.array(tmp_targetData))

	svm_params = dict(kernel_type = cv2.SVM_LINEAR, svm_type = cv2.SVM_C_SVC, C = 2.67, gamma = 5.383)

	trainer = cv2.SVM()
	trainer.train(trainingData, targetData, params = svm_params)
	trainer.save("dat/svm_hog.dat")

createTrainingData()