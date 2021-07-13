import os, cv2, potrace
import numpy as np

# DIRS and CONFIG
BASE_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
BW_DIR = os.path.join(OUTPUT_DIR, 'bw')
SVG_DIR = os.path.join(OUTPUT_DIR, 'svg')

# Load image and get it on B/W
filename = 'firma.jpg'

image = cv2.imread(filename, 2)
ret, bw = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# Write bw image to disk
# cv2.imwrite(os.path.join(BW_DIR, filename), bw)

# Write bw image data (numpy matrix) to disk
# np.savetxt('data_bw.txt', bw)

# Transform data in numpy array to match potrace
bw[bw > 0] = 1

# Write bw "binary" image data (numpy matrix) to disk
# np.savetxt('data_bw_norm.txt', bw)

idx_one = bw == 1
idx_zero = bw == 0

bw[idx_one] = 0
bw[idx_zero] = 1

# Write bw "inverted binary" image data (numpy matrix) to disk
# np.savetxt('data_bw_norm_inv.txt', bw)

# Generate bitmap with "inverted binary" data
bmp = potrace.Bitmap(bw)
# Generate path tracing bitmap
path = bmp.trace()

# Iterate over path curves and data
for curve in path:
    print("start_point =", curve.start_point)
    for segment in curve:
        print(segment)
        end_point_x, end_point_y = segment.end_point
        if segment.is_corner:
            c_x, c_y = segment.c
        else:
            c1_x, c1_y = segment.c1
            c2_x, c2_y = segment.c2

# TODO: Method to write path data to disk