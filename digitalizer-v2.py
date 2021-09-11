# Signature digitalizer version 2
# ==================================================
# Generates binary images as mid-products.
# Requires potrace (binary) installed on the system.
#
# Usage: python digitalizer-v2.py -f <filename>

import subprocess, os, cv2, argparse
from wand.image import Image

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

# Write binary borders to file (pnm) #
cv2.imwrite(BW_OUTPUT_FILENAME, borders)
with Image(filename=BW_OUTPUT_FILENAME) as pnm_target:
    pnm_target.format = "pnm"
    pnm_target.save(filename=PNM_OUTPUT_FILENAME)

# Call potrace to make svg #
subprocess.Popen(
    f"potrace {PNM_OUTPUT_FILENAME} --svg -o {SVG_OUTPUT_FILENAME}", shell=True
).wait()
