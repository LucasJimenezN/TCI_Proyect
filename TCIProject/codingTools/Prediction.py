import sys
import os
import numpy as np
import math


class Prediction:

    def __init__(self, image):
        self.image = image[0]

    def predict_image_LOP(self):
        # Asumiendo que la imagen es una matriz 2D de numpy
        assert len(self.image.shape) == 2

        # Crear una copia de la imagen para almacenar la imagen residual
        residual = np.zeros_like(self.image)

        # Para cada pixel en la imagen (excepto la primera fila y la primera columna)
        for i in range(1, self.image.shape[0]):
            for j in range(1, self.image.shape[1]):
                # Predecir el valor del pixel actual basándose en los pixels vecinos
                prediction = self.image[i-1, j-1] + self.image[i-1, j] + self.image[i, j-1] - 2*self.image[i-1, j-1]
                # Calcular el residual como la diferencia entre el valor real y la predicción
                residual[i, j] = self.image[i, j] - prediction


        return_img = np.expand_dims(residual, axis=0)

        return return_img

    def inverse_image(self):
        # Asumiendo que el residual es una matriz 2D de numpy
        assert len(self.image.shape) == 2

        # Crear una copia del residual para almacenar la imagen reconstruida
        image = np.zeros_like(self.image)

        # Para cada pixel en el residual (excepto la primera fila y la primera columna)
        for i in range(1, self.image.shape[0]):
            for j in range(1, self.image.shape[1]):
                # Reconstruir el valor del pixel actual sumando la predicción y el residual
                prediction = image[i-1, j-1] + image[i-1, j] + image[i, j-1] - 2*image[i-1, j-1]
                image[i, j] = prediction + self.image[i, j]

        return_img = np.expand_dims(prediction, axis=0)

        return return_img
