# Test de Independencia Condicional con Redes Generativas Adversarias

Esta es una implementación en python del algoritmo de propuesto en el paper paper ["Conditional Independence Testing with Generative Adversarial Networks"](https://arxiv.org/pdf/1907.04068.pdf), al cual se le incluyen ciertas modificaciones detalladas más adelante de manera de complementar el desempeño. El objetivo principal de los autores originales del paper es probar la independencia condicional entre un conjunto de variables X e Y, condicional a Z. Las pruebas serán realizadas sólo en conjuntos sintéticos, los mismos generados por los autores originales.

## Dependencias
python 3.7
pytorch 1.X

## Modificaciones al código de los autores originales
El archivo *GCIT.py* contiene una modificación en la última línea para poder obtener, además el *p-value* del test, las curvas de entrenamiento de las tres redes.

