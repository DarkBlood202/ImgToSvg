# Signature digitalizer version 3
# =========================================================
# Uses custom fork of pypotrace based on Gungora's (v.0.3).
# Generates svg file directly (no mid-product images).
#
# Usage: python digitalizer-v3.py -f <filename>

import os, cv2, argparse, potrace

# Getting args from CLI #
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "-f", "--file", help="Ruta a la imagen de la firma o sello", required=True
)

args = vars(arg_parser.parse_args())

# Extracting filename #
filename = args.get("file").rpartition(".")[0]
file_ext = args.get("file").rpartition(".")[2]

# Directory creation #
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SIG_DIR = os.path.join(BASE_DIR, "signatures")
FILE_DIR = os.path.join(SIG_DIR, filename)

# Output filenames #
BW_OUTPUT_FILENAME = os.path.join(FILE_DIR, f"{filename}_bw.{file_ext}")
PNM_OUTPUT_FILENAME = os.path.join(FILE_DIR, f"{filename}.pnm")
SVG_OUTPUT_FILENAME = os.path.join(FILE_DIR, f"{filename}.svg")

# signatures folder
try:
    os.mkdir(SIG_DIR)
    print(f'[INFO] Creating "signatures" directory.')
except FileExistsError:
    pass

# file subfolder
try:
    os.mkdir(FILE_DIR)
    print(f'[INFO] Files will be saved at "{filename}" sub-folder.')
except FileExistsError:
    pass

# Gray and Blur #
image = cv2.imread(args.get("file"))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Get binary borders #
borders = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 7
)

# Transform data to match potrace #
borders[borders > 0] = 1

idx_one = borders == 1
idx_zero = borders == 0

borders[idx_one] = 0
borders[idx_zero] = 1

# Generate potrace Bitmap, Path and XML #
bitmap = potrace.Bitmap(borders)
path = bitmap.trace()
xml = bitmap.to_xml()

# Write XML to SVG file #
with open(SVG_OUTPUT_FILENAME, "w") as svg:
    svg.write(xml)
