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
        L = [int(X[2*i+1]) + int((int(X[2*i]) - int(X[2*i+1]))//2) for i in range(n)]
        H = [int(X[2*i]) - int(X[2*i+1]) for i in range(n)]

        return np.concatenate((L, H))

    def s_transform_inverse(self, Y):
        # Asegurarse de que la longitud de Y es par
        assert len(Y) % 2 == 0, "La longitud de Y debe ser par"

        n = len(Y) // 2
        L = Y[:n]
        H = Y[n:]
        X_prime = np.zeros_like(Y)

        for i in range(n):
            X_prime[2*i] = int(H[i]) + int(L[i]) - int(int(H[i]) // 2)
            X_prime[2*i+1] = int(L[i]) - int(int(H[i]) // 2)

        return X_prime


    def handle_transform_forward(self):
        img_aux = np.copy(self.image[0])
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
        mat_aux = np.copy(image)
        transformed_mat = np.zeros((len_original_img,len_original_img), dtype=np.int16)
        # Filas
        for i, fila in enumerate(mat_aux):
            aux = self.s_tranform_forward(fila)
            transformed_mat[i] = aux

        # Columnas
        transformed_mat_T = np.transpose(transformed_mat)
        final_mat = np.zeros((len_original_img,len_original_img), dtype=np.int16)
        for i, columna in enumerate(transformed_mat_T):
            aux = self.s_tranform_forward(columna)
            final_mat[i] = aux

        # Transponer de nuevo para obtener la matriz final
#        final_mat = np.transpose(transformed_mat_T)
#        final_mat = transformed_mat
        return final_mat

    def handle_transform_inverse(self):
        original_img = np.copy(self.image)

        for i in range((self.levels-1), -1, -1):
            length = int(len(self.image) // pow(2, i))

            mat_aux = np.copy(original_img[:length, :length])
            aux = np.copy(self.handle_transform_inverse_rec(mat_aux))
            original_img[:length, :length] = np.copy(aux)

        original_img_3d = np.expand_dims(original_img, axis=0)

        return original_img_3d

    def handle_transform_inverse_rec(self, image):
        len_original_img = len(image)
        mat_aux = np.copy(image)
        transformed_mat = np.empty((len_original_img,len_original_img), dtype=np.int16)
        # Filas
        for i, fila in enumerate(mat_aux):
            aux = self.s_transform_inverse(fila)
            transformed_mat[i] = aux

        # Columnas
        transformed_mat_T = np.transpose(transformed_mat)
        final_mat = np.empty((len_original_img, len_original_img), dtype=np.int16)
        for i, columna in enumerate(transformed_mat_T):
            aux = self.s_transform_inverse(columna)
            final_mat[i] = np.copy(aux)

        # Transponer de nuevo para obtener la matriz final
#        final_mat = np.transpose(transformed_mat_T)
#        final_mat = transformed_mat
        return final_mat

#%%
