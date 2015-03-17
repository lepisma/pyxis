import cv2
import numpy as np
# from matplotlib import pyplot as plt
import cv

# # Constants
SZ = 20
affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR

def find_board(img):
	# Finds and crops the whiteboard
	# The steps planned are :
		# Matching corner using templates
		# Cropping the image
		# Transforming the skewed image
	img2 = img.copy()
	corner_template = [cv2.imread('templates/upper_left.JPG'), cv2.imread('templates/upper_right.JPG'), cv2.imread('templates/lower_left.JPG'), cv2.imread('templates/lower_right.JPG')] 

	img = img2.copy()
	method = eval('cv2.TM_CCOEFF_NORMED')

	points = []

	# Apply template Matching
	for template in corner_template:
		w, h, d = template.shape
		res = cv2.matchTemplate(img,template,method)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	
		top_left = max_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)
		points.append((top_left[0] + (w / 2), top_left[1] + (h / 2)))
		# cv2.rectangle(img,top_left, bottom_right, 255, 2)

	# print points
	top_width = points[1][0] - points[0][0]
	bottom_width = points[3][0] - points[2][0]
	left_height = points[2][1] - points[0][1]
	right_height = points[3][1] - points[1][1]

	# Finding dimensions of whiteboard

	if left_height > right_height:
		height = left_height
	else:
		height = right_height

	if top_width > bottom_width:
		width = top_width
	else:
		width = bottom_width

	points_before = np.float32([[points[0][0], points[0][1]], [points[1][0], points[1][1]], [points[2][0], points[2][1]], [points[3][0], points[3][1]]])
	points_after = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

	# Perspective transformation

	trans = cv2.getPerspectiveTransform(points_before, points_after)
	board = cv2.warpPerspective(img, trans, (width, height))

	# plt.subplot(121),plt.imshow(res,cmap = 'gray')
	# plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
	# plt.subplot(122),plt.imshow(board,cmap = 'gray')
	# plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
	# plt.suptitle('Match')

	# plt.show()

	return board

def check_difference(img1, img2):
	# Checks if the images have difference in textual contents

	img2 = (255 - img2)
	result = cv2.bitwise_and(img1, img2)
	mean_shade = int(np.sum(result) / (result.shape[0] * result.shape[1]))
	if mean_shade > MAX_VAL or mean_shade < MIN_VAL:
		return 0
	else:
		return 1

def adaptive_threshold(img):
	# Returns thresholded image
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	 
	ret, th1 = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
	th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
	th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
	th4 = cv2.adaptiveThreshold(img, 255, 1, 1, 11, 2)

	return th3

def human(img, cascade_fn = "haarXML/haarcascade_upperbody.xml", scale_factor = 1.3, min_neighbors = 4, min_size = (20, 20), flags = cv.CV_HAAR_SCALE_IMAGE):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.equalizeHist(img)
	cascade = cv2.CascadeClassifier(cascade_fn)
	rects = cascade.detectMultiScale(img, scaleFactor = scale_factor, minNeighbors = min_neighbors, minSize = min_size, flags = flags)

	if len(rects) == 0:
		body = []
	rects[:, 2:] += rects[:, :2]
	body = rects

	if len(body) <= 0:
		return 0
	else:
		return 1

def find_bounding_blocks(original_image, thresh_image, BLOCK_RESTRICTIONS):
	# Returns identified character blocks from image
	contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	blocks = []

	for cnt in contours:
		if cv2.contourArea(cnt) > (BLOCK_RESTRICTIONS[0] * BLOCK_RESTRICTIONS[1]):
			[x, y, w, h] = cv2.boundingRect(cnt)

			if h > BLOCK_RESTRICTIONS[1] and h < BLOCK_RESTRICTIONS[3]:
				if w > BLOCK_RESTRICTIONS[0] and w < BLOCK_RESTRICTIONS[2]:
					roi = thresh_image[x:x+w, y:y+h]
					if len(roi) == 0:
						continue
					cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 1)
					blocks.append([x, y, w, h])
					# break

	return blocks

def crop_blocks(original_image, blocks):
	thresh = adaptive_threshold(original_image)
	cropped = []
	for coords in blocks:
		[x, y, w, h] = coords
		cropped.append(thresh[y:y + h, x:x + w])
	return cropped

def resize_to_token(box):
	# Resizes the contour blocks to 100x100 size token after deskewing

	# m = cv2.moments(box)
	# if abs(m['mu02']) < 1e-2:
	# 	return box.copy()
	# skew = m['mu11']/m['mu02']
	# M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
	# box = cv2.warpAffine(box,M,(SZ, SZ),flags=affine_flags)
	token = cv2.resize(box, (100, 100))
	return token

def reject_sub_tokens(token_plus_pos):
	new_tokens = []
	length = len(token_plus_pos)

	no = 0

	for i in range(length):
		for j in range(i + 1, length):
			to_filter = token_plus_pos[i][1]
			compares_to = token_plus_pos[j][1]

			if (to_filter[0] > compares_to[0]) and (to_filter[0] < (compares_to[0] + compares_to[2])):
				if (to_filter[1] > compares_to[1]) and (to_filter[1] < (compares_to[1] + compares_to[3])):
					if (to_filter[2] < compares_to[2]) and (to_filter[3] < compares_to[3]):
						break
			else:
				no += 1
		if (no == (length - i - 1)):
			new_tokens.append(token_plus_pos[i])
		no = 0
	return new_tokens

def filter_position(tokens_and_pos):
	new_tk = []

	for x in tokens_and_pos:
		if x[1][1] < 60: # Optional (temporary board cropping)
			new_tk.append(x)

	return new_tk