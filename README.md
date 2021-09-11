# Signature digitalizer script (version 3)
## Dependencies
+ Python 3.9
+ OpenCV
+ [Pypotrace (custom fork)](https://github.com/DarkBlood202/pypotrace-xml)

## Description
The script reads signature images and traces over them using potrace library. SVG files are generated under the "signatures" folder.

## Usage (as of version 3)
1. Place desired signature image inside root folder.
2. Execute in a terminal:
~~~
python digitalizer-v3.py -f <filename>
~~~

