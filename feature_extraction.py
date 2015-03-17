import cv2
import numpy as np

def line_average_vector(token):

	# Feature vector description
	#	-	starting 100 values = average of each column
	#	-	next 100 values = average of each row

	rows_n, columns_n = token.shape
	token = np.float32(token)

	column_average = token.sum(axis = 0) / rows_n
	row_average = token.sum(axis = 1) / columns_n

	vector = np.concatenate((column_average, row_average))
	norm_vector = vector/max(vector)

	return norm_vector

def simple_pixels_vector(token):

	# Feature vector description
	# 	- Returns all 10000 pixels
	return token.reshape(-1)


def hog_vector(token):

	# Feature vector description
	#	-	16 values per sub squares, total sub squares = 4
	#	-	total values = 64

	bin_n = 16
	
	gx = cv2.Sobel(token, cv2.CV_32F, 1, 0)
	gy = cv2.Sobel(token, cv2.CV_32F, 0, 1)
	mag, ang = cv2.cartToPolar(gx, gy)

	# quantizing binvalues in (0...16)
	bins = np.int32(bin_n*ang/(2*np.pi))

	# Divide to 4 sub-squares
	bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
	mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
	hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
	hist = np.hstack(hists)

	return hist