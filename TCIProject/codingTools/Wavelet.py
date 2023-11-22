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
            L_data = int(input_array[2 * n + 1] + (int((input_array[2 * n] - input_array[2 * n + 1]) / 2)))
            L.append(L_data)
            H.append(int(input_array[2 * n] - input_array[2 * n + 1]))

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
            X_prime_data_1 = int(input_array[n + for_range] + input_array[n] - int(input_array[n + for_range] / 2))
            X_prime_data_2 = int(input_array[n] - int(input_array[n + for_range] / 2))
            X_prime.append(X_prime_data_1)
            X_prime.append(X_prime_data_2)

        # Convertir X' a un array de numpy
        X_prime = np.array(X_prime)

        # Devolver X'
        return X_prime

    def handle_transform_forward(self):
        img_aux = self.image[0]
        ret_img = np.zeros((len(img_aux),len(img_aux)), dtype=np.int16)
        for i in range(0, self.levels):
            aux = self.handle_transform_forward_rec(img_aux)
            ret_img[:len(aux), :len(aux)] = aux
            mitad = aux.shape[0] // 2
            img_aux = aux[:mitad, :mitad]

        # Bucle for de juntar todas las matrices
        return(ret_img)

    def handle_transform_forward_rec(self, image):
        len_original_img = len(image)
        transformed_mat = np.zeros((len_original_img,len_original_img), dtype=np.int16)
        # Filas
        for i, fila in enumerate(image):
            aux = self.s_tranform_forward(fila)
            transformed_mat[i] = aux

        print(f"Longitud forward: {len(transformed_mat)}")

        # Columnas
        transformed_mat_T = transformed_mat.T
        for i, columna in enumerate(transformed_mat_T):
            aux = self.s_tranform_forward(columna)
            transformed_mat_T[i] = aux

        # Transponer de nuevo para obtener la matriz final
        final_mat = transformed_mat_T.T
        final_mat = transformed_mat
        return final_mat

    def handle_transform_inverse(self):
        original_img = self.image

        for i in range((self.levels-1), -1, -1):
            length = int(len(self.image) / pow(2, i))

            mat_aux = np.zeros((length, length), dtype=np.int16)

            mat_aux[:length, :length] = original_img[:length, :length]
            aux = self.handle_transform_inverse_rec(mat_aux)
            original_img[:length, :length] = aux

        original_img_3d = np.expand_dims(original_img, axis=0)

        return original_img_3d

    # Caso 1 ( 1 level )
    # 512 -> length = 512,
    # Caso 2 ( 2 levels )
    # 512 -> length = 256 -> length = 512
    # Caso 4 ( 4 levels ) -> 3 - 2 - 1 - 0
    # 512 -> 64 ->

    def handle_transform_inverse_rec(self, image):
        len_original_img = len(image)
        transformed_mat = np.empty((len_original_img,len_original_img), dtype=np.int16)
        # Filas
        for i, fila in enumerate(image):
            aux = self.s_transform_inverse(fila)
            transformed_mat[i] = aux

        # Columnas
        transformed_mat_T = transformed_mat.T
        for i, columna in enumerate(transformed_mat_T):
            aux = self.s_transform_inverse(columna)
            transformed_mat_T[i] = aux

        # Transponer de nuevo para obtener la matriz final
        final_mat = transformed_mat_T.T
        final_mat = transformed_mat
        return final_mat

#%%
