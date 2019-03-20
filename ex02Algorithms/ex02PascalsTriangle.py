# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A
# literatur zu fibonacci und zusammenhang mit pascals dreieck https://www.maplesoft.com/applications/view.aspx?sid=3617&view=html

import numpy



def factoriel(n):
    """Function that calculates the factoriel of a number in a recursive function"""
    #print("- input: ", n)
    if n <= 1:
        return 1
    else:
        return n * factoriel(n-1)



def binomial_koefficient(n, k):

    """Function that calculates the binomial coefficient """

    if n-k <= 0:
        return 1
    else:
        return factoriel(n) // (factoriel(k) * factoriel(n-k))      # return the calculated coefficient


def pascals_triangle(n):
    """Calculates the Pascals Triangle - NOT RECURSIVE"""

    col_list = []

    for n in range(n+1):
        row_list = []
        for k in range(n+1):

            if n == 0 and k == 0:
                row_list.append(1)

            else:
                row_list.append(binomial_koefficient(n,k))

        col_list.append(row_list)

    return col_list

def pascals_triangle_rec(n):
    """
    recurse function of pascal triangle found on stackoverflow,
    https://stackoverflow.com/questions/10628788/python-recursive-pascal-triangle
    """
    #print("input n ", n)
    if n == 0:
        #print("geh da rein")
        return []

    elif n == 1:
        return [[1]]

    else:

        # create a new pascal row as a list and let it start with a 1
        new_pascal_row = [1]
        #print("new row: ", new_pascal_row)

        # call pascal triangle recursive and return the entire
        pascal_triangle_list = pascals_triangle_rec(n-1)
        #print("result: ", pascal_triangle_list)

        # take the last list in the lost of lists returned by the recursive function
        last_row = pascal_triangle_list[-1]
        #print("last row: ", last_row)

        # iter through the last list in the list of lists
        for i in range(len(last_row)-1):
            # sum the elements according the pascals triangle and append it to the last row
            #print("calc sum: ", last_row[i] + last_row[i+1])
            new_pascal_row.append(last_row[i] + last_row[i+1])

        # "close" the last row with a 1
        new_pascal_row += [1]

        # append the new row under the last row so it creates the pascal triangle
        pascal_triangle_list.append(new_pascal_row)

    return pascal_triangle_list

if __name__ == "__main__":

    n = 12

    #print("\n")
    #print(pascals_triangle(n))
    #print("\n")

    # create pascals triangle with the function that uses recursion
    #pascal_triangle = pascals_triangle_rec(n)

    # create pascals triangle with the function that uses NO recursion
    pascal_triangle = pascals_triangle(n)

    # initialize fibonacci sequence
    fibonacci_list = [0,1]

    # walk through sub_lists in pascals triangle return list
    for line in pascal_triangle:
        print(line)
        num_elements = len(line)

        #print("len elements: ", len(line))

        fib_sum = 0
        # calculate the fibinacci sequence with binomial koefficients
        for j in range(1 + int(numpy.trunc(num_elements-2 / 2))):

            if num_elements-2*j < 0:
                break
            else:
                #print("%d - " % j, num_elements - j, " ", num_elements - 2 * j)
                fib_sum += binomial_koefficient(num_elements - j, num_elements - 2 * j)
        #print("fib sum: ", fib_sum)
        fibonacci_list.append(fib_sum)

    print("fibonacci result: ", fibonacci_list)