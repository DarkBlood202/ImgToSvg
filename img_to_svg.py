import sys, subprocess

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

# Calls to bw script
subprocess.Popen(f'python to_bw.py {filename} {bw_output_name}', shell=True).wait()
# Calls to ImageMagick convert function
subprocess.Popen(f'convert {bw_output_name} {pnm_output_name}', shell=True).wait()
# Calls to Potrace
subprocess.Popen(f'potrace {pnm_output_name} --svg -o {svg_output_name}', shell=True).wait()