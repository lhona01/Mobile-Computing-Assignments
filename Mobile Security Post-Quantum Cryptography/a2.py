import numpy as np
import math

# Encrypts/decrypts binary messages ex: 010011...... using Learnin with error (LWE) algorithm
class A2:
    def __init__(self):
        self.secret_key = None

    # int [][], int [], int [], int ; return []
    def generate_public_key_vector(self, matrix_A, secret_key_s, error_vector_e, modulus_p):
        self.secret_key = secret_key_s
        print("secret_key", secret_key_s)
        result = np.zeros(len(matrix_A))

        for i in range(0, len(matrix_A)):
            sum_row_x_s = 0 # sum(matrix_A[x][y] * secret_key_s[Y])

            for j in range(0, len(matrix_A[i])):
                sum_row_x_s += matrix_A[i][j] * secret_key_s[j]

            result[i] = (sum_row_x_s + error_vector_e[i]) % modulus_p
        return result
    
    # (int[][], int[]), int, , int
    def encrypt(self, public_key, rand_binary_vector, message, modulus):
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
        
        # encrypt binary
        if message == 1:
            return (sum_valid_rows_A, (sum_key_vector + math.floor(modulus / 2)) % modulus)
        elif message == 0:
            return (sum_valid_rows_A, sum_key_vector % modulus)
    
    # int[], int([], int) , int
    def decrypt(self, private_key, ciphertext, modulus):
        print("ciphertext:", ciphertext)
        print("modulus:", modulus)
        print("private_key", private_key)
        mod_div_2 = math.floor(modulus / 2)

        enc = (ciphertext[1] - (np.dot(ciphertext[0], self.secret_key) % modulus)) % modulus
        close_to_0 = enc
        close_to_mod_div_2 = abs(enc - mod_div_2)

        if close_to_0 < close_to_mod_div_2:
            return 0
        else:
            return 1


# Test Case
'''
A = [[19, 8, 1, 14], [3, 11, 20, 23], [5, 5, 23, 9]]
s = [4, 7, 16, 9, 13, 11, 1, 18, 5, 10]
e = [-1, 1, 0]
p = 7

a2 = A2()
b = a2.generate_public_key_vector(A,s,e,p)

public_key = (A, b)

#apple = a2.encrypt(public_key, [1, 1, 0], 1, 7)

print(a2.decrypt([4,7,16,9,13,11,1,18,5,10], ([ 9, 6, 3, 0, 7, 9, 10, 8, 4, 1], 12), 15))

#expected = 1, returned = 0
'''