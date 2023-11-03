import sys
import os
import numpy
import math

import numpy as np


class Wavelet:
    current_level = 0

    def __init__(self, image, levels):
        self.image = image
        self.levels = levels

    def get_image(self):
        return self.image

    def get_levels(self):
        return self.levels

    def s_tranform_forward(self, input_array):
        # Asegurarse de que X es un array de numpy
        if not isinstance(input_array, np.ndarray):
            input_array = np.array(input_array)

        # Comprobar que la longitud de X es par
        if len(input_array) % 2 != 0:
            raise ValueError("La longitud de X debe ser par")

        # Inicializar L y H como listas vacías
        L = []
        H = []

        # Rango del bucle for
        for_range = int(len(input_array) / 2)

        # Calcular L y H usando un bucle for
        for n in range(0, for_range):
            L_data = input_array[2 * n + 1] + (int((input_array[2 * n] - input_array[2 * n + 1]) / 2))
            L.append(L_data)
            H.append(input_array[2 * n] - input_array[2 * n + 1])

        # Convertir L y H a arrays de numpy
        L = np.array(L)
        H = np.array(H)

        # Devolver un solo array con L y H concatenados
        return np.concatenate((L, H))

    def s_transform_inverse(self, input_array):
        # Asegurarse de que X es un array de numpy
        if not isinstance(input_array, np.ndarray):
            input_array = np.array(input_array)

        # Comprobar que la longitud de X es par
        if len(input_array) % 2 != 0:
            raise ValueError("La longitud de X debe ser par")

        # Inicializar X' como una lista vacía
        X_prime = []

        # Rango del bucle for
        for_range = int(len(input_array) / 2)

        # Calcular X' usando un bucle for
        for n in range(0, for_range):
            X_prime_data_1 = input_array[n + for_range] + input_array[n] - int(input_array[n + for_range] / 2)
            X_prime_data_2 = input_array[n] - int(input_array[n + for_range] / 2)
            X_prime.append(X_prime_data_1)
            X_prime.append(X_prime_data_2)

        # Convertir X' a un array de numpy
        X_prime = np.array(X_prime)

        # Devolver X'
        return X_prime

    def handle_transform_forward(self):
        for z in range(self.image_components):
            for y in range(self.image.shape(1)):
                print(f"Fila 1: {self.image[z][y]}")