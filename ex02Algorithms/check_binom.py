from scipy import special
# https://www.maplesoft.com/applications/view.aspx?sid=3617&view=html


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



if __name__ == "__main__":

    n = 6
    pascal_triangle = pascalsTriangle(6)
    fib_sum = 0
    for line in pascal_triangle:
        print(line)
        num_elements = len(line)

        print("len elements: ", len(line))

        if num_elements % 2 == 0:
            print("gerade zahl")
            iter_list = list(range(num_elements-1,0,-2)).append(0)
            print("iter list: ", iter_list)
        else:
            print("ungerade zahl")
            iter_list = list(range(num_elements-1,0,-2))
            print("iter list: ", iter_list)

        for i in iter_list:

            print(i)











