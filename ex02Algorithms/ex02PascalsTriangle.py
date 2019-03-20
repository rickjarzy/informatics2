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



def binomial_koefficient(n,k):

    """Function that calculates the binomial coefficient """

    if n-k <= 0:
        return 1
    else:
        return factoriel(n) // (factoriel(k) * factoriel(n-k))      # return the calculated coefficient


def pascalsTriangle(n):
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

def pascals_triangle(n):
    """
    recurse function of pascal triangle found on stackoverflow,
    https://stackoverflow.com/questions/10628788/python-recursive-pascal-triangle
    """
    if n == 0:
        return []

    elif n == 1:
        return [[1]]

    else:
        new_row = [1]
        print("new row: ", new_row)
        result = pascals_triangle(n-1)
        print("result: ", result)
        last_row = result[-1]
        print("last row: ", last_row)

        for i in range(len(last_row)-1):
            new_row.append(last_row[i] + last_row[i+1])

        new_row += [1]
        result.append(new_row)

    return result

if __name__ == "__main__":

    n = 6

    #print("\n")
    #print(pascals_triangle(n))
    #print("\n")

    # create pascals triangle
    pascal_triangle = pascalsTriangle(n)

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