import numpy as np

chars = np.load("charmap_data.npy")

def get_class(character):
	i = 0
	for x in chars:
		if character == x:
			return i
		i += 1

	return 'Error'