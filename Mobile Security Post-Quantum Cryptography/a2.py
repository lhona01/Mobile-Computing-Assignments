import numpy as np
import math

class A2:
    def __init__(self):
        pass

    # int [][], int [], int [], int ; return []
    def generate_public_key_vector(self, matrix_A, secret_key_s, error_vector_e, modulus_p):
        print("matrix_A:", matrix_A)
        print("secret_key_s:", secret_key_s)
        print("error_vector_e:", error_vector_e)
        print("modulus_p:", modulus_p)

        result = np.zeros(len(matrix_A))

        for i in range(0, len(matrix_A)):
            sum_row_x_s = 0 # sum(matrix_A[x][y] * secret_key_s[Y])

            for j in range(0, len(matrix_A[i])):
                sum_row_x_s += matrix_A[i][j] * secret_key_s[j]

            result[i] = (sum_row_x_s + error_vector_e[i]) % modulus_p
        return result
    
    # (int[][], int[]), int, , int
    def encrypt(self, public_key, rand_binary_vector, message, modulus):
        print("public_key:", public_key)
        print("rand_binary_vector:", rand_binary_vector)
        print("message:", message)
        print("modulus:", modulus)
        matrix_A = public_key[0]
        key_vector = public_key[1]
        sum_valid_rows_A = np.zeros(len(matrix_A[0]))
        sum_key_vector = 0

        for i in range(0, len(rand_binary_vector)):
            if (rand_binary_vector[i] == 1):
                # Sum up corresponding entries in b
                sum_key_vector += key_vector[i]

                for j in range(0, len(matrix_A[i])):
                    # sum up corresponding entries in A's rows
                    sum_valid_rows_A[j] += matrix_A[i][j]
        
        for i in range(0, len(sum_valid_rows_A)):
            sum_valid_rows_A[i] = sum_valid_rows_A[i] % modulus
        
        # encrypt message
        if message == 1:
            return (sum_valid_rows_A, (sum_key_vector + math.floor(modulus / 2)) % modulus)
        elif message == 0:
            return (sum_valid_rows_A, sum_key_vector % modulus)
    
    #def decrypt(private_key, ciphertext, modulus):

A = [[19, 8, 1, 14], [3, 11, 20, 23], [5, 5, 23, 9]]
s = [4, 1, 2, 3]
e = [-1, 1, 0]
p = 7

a2 = A2()
b = a2.generate_public_key_vector(A,s,e,p)

public_key = (A, b)

apple = a2.encrypt(public_key, [1, 1, 0], 1, 7)
