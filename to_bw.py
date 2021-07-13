import sys, cv2, os

# Get command-line arguments
try:
    filename = sys.argv[1]
    output = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <input filename> <output filename>")

# Read file and load to opencv
img = cv2.imread(filename, 2)
# Get BW based on color value
ret, bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
# Write BW image to disk
cv2.imwrite(output, bw)
