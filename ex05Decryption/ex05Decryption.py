# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A
# main programm

import numpy
import matplotlib.pyplot as plt
import downloader

if __name__ == "__main__":

    matrix_file_name = "matrix.txt.gz"
    key_file_name = "key.txt"

    # download the key file
    downloader.download("ftp.tugraz.at", "/outgoing/ITSG/teaching/2019SS_Informatik2", "key.txt")

    #download the matrix file and decompress the matrix file
    matrix_txt_filename = downloader.decompress(matrix_file_name)

    #load matrix from txtfile
    matrix = numpy.loadtxt(matrix_txt_filename)
    key_vector = numpy.loadtxt(key_file_name)

    # decrypt information
    key_col_vector = key_vector[:, numpy.newaxis]   # create a column vector
    print("key_col_vector shape: ", key_col_vector.shape)

    matrix_B = key_col_vector * matrix              # multiply k with lines of B
    matrix_K = key_col_vector @ key_col_vector.T    # create a matrix kK.T
    matrix_I = numpy.eye(matrix_K.shape[0])         # create I Matrix
    matrix_L = matrix_I + matrix_K                  # add I with kk.T
    matrix_C = numpy.linalg.inv(matrix_L) @ matrix_B    # multiply L on the left side with matrix_B
    matrix_D = matrix_C.T                           # transpose matrix C
    matrix_E = matrix_D - matrix_L                  # subtract matrix_L from matrix_D


    #plot information
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.imshow(matrix_E, cmap='gray')
    ax.set_title("""#include <stdio.h> int main(){ printf("Hello World!"); return 0; }\nex05Decryption""") # ;)
    plt.show()

    print("Programm ENDE")