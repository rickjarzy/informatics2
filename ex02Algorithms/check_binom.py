from scipy import special


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
    """Calculates the Pascals Triangle"""

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


for line in pascalsTriangle(6):
    print(line)


