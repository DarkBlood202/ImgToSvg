import sys, subprocess, shutil, os, cv2
from wand.image import Image

def create_directories(raw_filename):
    try: 
        os.mkdir('signatures') 
    except: 
        pass 

    try: 
        os.mkdir(f'signatures\{raw_filename}') 
    except: 
        pass

def img_to_bw(filename, bw_output_name):

    # Read file and load to opencv
    img = cv2.imread(filename, 2)
    # Get BW based on color value
    ret, bw = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    # Write BW image to disk
    try:
        cv2.imwrite(bw_output_name, bw)
    except:
        raise Exception('Colocar imagen de la firma en la carpeta raiz del proyecto') 

def bw_to_pnm(filename_bw, pnm_output_name):

    with Image(filename=filename_bw) as img:
        img.format = 'pnm'
        img.save(filename=pnm_output_name)

def svg_to_jpg(svg_output_name, jpg_output_name):

    with Image(filename=svg_output_name) as img:
        img.format = 'jpg'
        img.save(filename=jpg_output_name)

# Getting command-line arguments
try:
    filename = sys.argv[1]
except:
    raise SystemExit(f"Usage: {sys.argv[0]} <filename>")

# Extracting filename data from argument
raw_filename = filename.rpartition(".")[0]
ext_filename = filename.rpartition(".")[2]

# Setting output names
bw_output_name = f'{raw_filename}_bw.{ext_filename}'
pnm_output_name = f'{raw_filename}.pnm'
svg_output_name = f'{raw_filename}.svg'
jpg_output_name = f'{raw_filename}_final.jpg'

output_filenames_list = [bw_output_name, pnm_output_name, svg_output_name,jpg_output_name]

# Calls to bw function
img_to_bw(filename, bw_output_name)

# Directories creation
create_directories(raw_filename)

# Convert from bw to pnm format
bw_to_pnm(bw_output_name, pnm_output_name)

# Convert from pnm to svg format
subprocess.Popen(f'potrace {pnm_output_name} --svg -o {svg_output_name}', shell=True).wait()

# Convert from svg to jpg format
svg_to_jpg(svg_output_name, jpg_output_name)

# Move all output files to a separate directory
for output_filename in output_filenames_list:
    target = f'signatures\{raw_filename}\{output_filename}'
    shutil.move(output_filename,target)
