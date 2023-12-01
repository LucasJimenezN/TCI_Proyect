import sys
import os
import numpy as np
import math


class Prediction:

    def __init__(self, image):
        self.image = image[0]

    def predict_image(self):
        # Asumiendo que la imagen es una matriz 2D de numpy
        assert len(self.image.shape) == 2

        # Crear una copia de la imagen para almacenar la imagen residual
        residual = np.zeros_like(self.image)

        # Para cada pixel en la imagen (excepto la primera fila y la primera columna)
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                if i == 0 and j == 0:
                    prediction = 0

                else:
                    if i == 0:
                        # Cuando estamos en la primera fila solo podremos utilizar los pixeles de la izquierda
                        prediction = self.image[i, j - 1]

                    elif j == 0:
                        prediction = self.image[i - 1, j]

                    else:
                        # Predecir el valor del pixel actual basándose en los pixels vecinos
                        prediction = int((self.image[i - 1, j - 1] + self.image[i - 1, j] * 2 +
                                          self.image[i, j - 1] * 2) / 5)

                # Calcular el residual como la diferencia entre el valor real y la predicción
                residual[i, j] = self.image[i, j] - prediction

                '''if i > 1 and j > 1:
                    # Predecir el valor del pixel actual basándose en los pixels vecinos
                    prediction = ((self.image[i-2, j-2] + 2*self.image[i-2, j-1] + 3*self.image[i-2, j] +
                                  2*self.image[i-1, j-2] + 4*self.image[i-1, j-1] + 5*self.image[i-1, j] +
                                  3*self.image[i, j-2] + 5*self.image[i, j-1]) / 25)
                elif i > 0 and j > 0:
                    # Si estamos en la segunda fila o columna, usamos una fórmula de predicción más simple
                    prediction = ((self.image[i-1, j-1] + self.image[i-1, j] +
                                   self.image[i, j-1]) / 3)
                elif j > 0:
                    prediction = self.image[i, j-1]
                    
                elif i > 0:
                    prediction = self.image[i-1, j]
                    
                else:
                    # Para los primeros pixels usamos el valor original
                    prediction = self.image[i, j]

                residual[i, j] = self.image[i, j] - prediction'''

        return_img = np.expand_dims(residual, axis=0)

        return return_img


def invert_image(predicted):
    # Asumiendo que la imagen residual es una matriz 2D de numpy
    residual = predicted[0]
    assert len(residual.shape) == 2

    # El resto del código es el mismo que antes...
    original = np.zeros_like(residual)
    for i in range(residual.shape[0]):
        for j in range(residual.shape[1]):
            if i == 0 and j == 0:
                original[i, j] = residual[i, j]
            else:
                if i == 0:
                    prediction = original[i, j - 1]
                elif j == 0:
                    prediction = original[i - 1, j]
                else:
                    prediction = int((original[i - 1, j - 1] + original[i - 1, j] * 2 +
                                      original[i, j - 1] * 2) / 5)
                original[i, j] = residual[i, j] + prediction

    return_img = np.expand_dims(original, axis=0)

    return return_img
