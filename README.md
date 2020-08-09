# Redes Generativas Adversarias en Test de Independencia Condicional

Esta es una implementación en python del algoritmo de propuesto en el paper paper ["Conditional Independence Testing with Generative Adversarial Networks"](https://arxiv.org/pdf/1907.04068.pdf), al cual se le incluyen ciertas modificaciones detalladas más adelante de manera de complementar el desempeño. El objetivo principal de los autores originales del paper es probar la independencia condicional entre un conjunto de variables X e Y, condicional a Z. Las pruebas serán realizadas sólo en conjuntos sintéticos, los mismos generados por los autores originales.

## Dependencias

- python 3.6.9
- pytorch 1.6.0+cu101
- numpy 1.18.5
- matplotlib 3.2.2

## Modificaciones al código de los autores originales

El archivo *GCIT.py* contiene una modificación en la última línea para poder obtener, además el *p-value* del test, las curvas de entrenamiento de las tres redes. También se modifica el mismo archivo para evitar detener el entrenamiento antes de las 1000 iteraciones.

## Implementación en Pytorch

La implementación en *Pytorch* se realizó acorde al algoritmo descrito en el material suplementario del paper. Se valida la implementación en la nueva librería comparando las curvas de entrenamiento de las redes para los conjuntos sintéticos Condicionalmente Independientes (CI), Independientes (I), No Independientes (NI).

## Mejoras

Se incorpora la regularización del modelo InfoGAN de este paper ["InfoGAN: Interpretable Representation Learning by Information Maximizing Generative Adversarial Nets"](https://arxiv.org/pdf/1606.03657) para preservar la información de la variable condicionante Z en la red generadora de la distribución X|Z. Esto finalmente corresponde a entrenar un estimador de información mutua entre las muestras generadas y la variable condicionante Z, para luego agregar un término extra en la función de costos de la red generadora de tal forma que se maximice este término.
