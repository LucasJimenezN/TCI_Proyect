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

    def s_tranform_forward(self, X):
        # Asegurarse de que la longitud de X es par
        assert len(X) % 2 == 0, "La longitud de X debe ser par"

        n = len(X) // 2
        L = [X[2*i+1] + int((X[2*i] - X[2*i+1])//2) for i in range(n)]
        H = [X[2*i] - X[2*i+1] for i in range(n)]

        return np.concatenate((L, H))

    def s_transform_inverse(self, Y):
        # Asegurarse de que la longitud de Y es par
        assert len(Y) % 2 == 0, "La longitud de Y debe ser par"

        n = len(Y) // 2
        L = Y[:n]
        H = Y[n:]
        X_prime = np.zeros_like(Y)

        for i in range(n):
            X_prime[2*i] = H[i] + L[i] - (H[i] // 2)
            X_prime[2*i+1] = L[i] - (H[i] // 2)

            # Si el valor es mayor que 255, restar 255
            if X_prime[2*i] > 255:
                X_prime[2*i] -= 256
            if X_prime[2*i+1] > 255:
                X_prime[2*i+1] -= 256

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
        return ret_img

    def handle_transform_forward_rec(self, image):
        len_original_img = len(image)
        transformed_mat = np.zeros((len_original_img,len_original_img), dtype=np.int16)
        # Filas
        for i, fila in enumerate(image):
            aux = self.s_tranform_forward(fila)
            transformed_mat[i] = aux

        # Columnas
        transformed_mat_T = np.transpose(transformed_mat)
        for i, columna in enumerate(transformed_mat_T):
            aux = self.s_tranform_forward(columna)
            transformed_mat_T[i] = aux

        # Transponer de nuevo para obtener la matriz final
        final_mat = np.transpose(transformed_mat_T)
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

    def handle_transform_inverse_rec(self, image):
        len_original_img = len(image)
        transformed_mat = np.empty((len_original_img,len_original_img), dtype=np.int16)
        # Filas
        for i, fila in enumerate(image):
            aux = self.s_transform_inverse(fila)
            transformed_mat[i] = aux

        # Columnas
        transformed_mat_T = np.transpose(transformed_mat)
        for i, columna in enumerate(transformed_mat_T):
            aux = self.s_transform_inverse(columna)
            transformed_mat_T[i] = aux

        # Transponer de nuevo para obtener la matriz final
        final_mat = np.transpose(transformed_mat_T)
        return final_mat

#%%
