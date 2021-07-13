# Vectorización de una imagen
## Proceso funcional actual en script (genera byproducts)
### Dependencias
+ Potrace
+ ImageMagick
+ Python 3.9

Ejecutar en una terminal:
~~~
python img_to_svg.py <filename>
~~~

## Proceso funcional actual (versión manual)
### Dependencias
+ Potrace
+ ImageMagick
+ Python 3.9

1. Ejecución de script **to_bw.py** para convertir imagen a su versión en blanco y negro (duotono).
2. Uso de ImageMagick para convertir imagen en blanco y negro a formato **PNM** y que pueda ser leída por Potrace.
    ~~~
    convert image.png image.pnm
    ~~~
3. Uso de Potrace para trazar sobre el mapa de bits y generar una imagen vectorial.
    ~~~
    potrace image.pnm --svg -o image.svg
    ~~~

## Proceso a través de un único script (no genera byproducts)
### Dependencias
+ Numpy
+ OpenCV
+ PyPotrace

Ejecutar en una terminal:
~~~
python img_to_path.py <filename>
~~~

1. Cargar imagen vía **OpenCV** y convertirla a su versión en blanco y negro (duotono).
2. Transformar los datos de la imagen en blanco y negro con **NumPy** en una matriz de 0 (blanco) y 1 (negro).
3. Generar un mapa de bits con **Potrace** a partir de la matriz.
4. Generar un trayecto a partir del mapa de bits.
5. Generar una imagen vectorial a partir de los datos del trayecto*.

*: Falta el método para escribir la data del trazado a un archivo de gráficos vectoriales (svg).