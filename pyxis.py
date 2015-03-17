# The main handler
import cv2
import numpy as np
import preprocessing
import feature_extraction
import charmap
import tester

def see(feature_type):
	BLOCK_RESTRICTIONS = [5, 9, 80, 80] # WIDTH, HEIGHT, (MIN, MAX)
	vc = cv2.VideoCapture(1)

	i = 0
	while True:
		ret, frame = vc.read()
		kernel = np.ones((2, 2), np.uint8)
		frame = preprocessing.find_board(frame) # Optional (for board)

		frame = frame[10 : 400, 10: 300] # Optional cropping

		frame_original = frame.copy()

		# img = cv2.morphologyEx(preprocessing.adaptive_threshold(frame), cv2.MORPH_OPEN, kernel)
		img = preprocessing.adaptive_threshold(frame)
		blocks = preprocessing.find_bounding_blocks(frame, img, BLOCK_RESTRICTIONS)

		print len(blocks)
		cv2.imshow("tester", frame)
		key = cv2.waitKey(20)
		i += 1
		if i == 5:
			break

	blocks_images = preprocessing.crop_blocks(frame_original, blocks)
	tokens = map(preprocessing.resize_to_token, blocks_images)

	tokens_and_pos = zip(tokens, blocks)
	tokens_and_pos = preprocessing.filter_position(tokens_and_pos)
	tokens_and_pos = preprocessing.reject_sub_tokens(tokens_and_pos)

	tokens = [tok[0] for tok in tokens_and_pos]
	pos = [tok[1] for tok in tokens_and_pos]

	if (feature_type == "pixels"):
		print "Running on all pixels"
		feature_vectors = map(feature_extraction.simple_pixels_vector, tokens)
	elif (feature_type == "line"):
		print "Running on line average"
		feature_vectors = map(feature_extraction.line_average_vector, tokens)
	else:
		print "Running on hog"
		feature_vectors = map(feature_extraction.hog_vector, tokens)

	characters = []

	s = cv2.SVM()
	if (feature_type == "pixels"):
		s.load("dat/svm_pixels.dat")
	elif (feature_type == "line"):
		s.load("dat/svm_line.dat")
	else:
		s.load("dat/svm_hog.dat")

	for x in range(len(feature_vectors)):
		res = s.predict(np.float32(feature_vectors[x]))
		character = charmap.chars[res]
		position_of_character = [pos[x][0], pos[x][1]]
		# print charmap.chars[res] + " at (" + str(position_of_character[0]) + ", " + str(position_of_character[1]) + ")"

		characters.append([character, position_of_character])

	word = return_string(characters)
	print len(word)
	print word
	return word

def return_string(characters):
	sorted_characters = sorted(characters, key = lambda d: d[1])
	word = ""
	for x in sorted_characters:
		word += x[0]

	return word