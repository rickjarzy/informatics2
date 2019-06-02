# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A


class InvalidGradeError(ValueError):
    """
    class that handles invalide grades with an error message
    """
    def __init__(self, arg):
        # public error message
        self.errorstring = arg


def calcGradeAverage(grade_dict):

    """
    sorts the grade_dict by its keys and prints the information in a fomrated way on the screen
    :param grade_dict: dict - keys: grades - values: frequency of a grade
    :return: None
    """

    sum_grade = 0
    sum_frequency = 0
    # sort the dict by its keys
    print(grade_dict.items())
    for grade, frequency in sorted(grade_dict.items()):
        print("Grade: ", grade, " : ", frequency)
        sum_grade += grade * frequency
        sum_frequency += frequency
    # calc the mean of the grade
    print("Average grade (out of %d): %2.1f" % (sum_frequency, sum_grade / sum_frequency))


def checkGrade(grade, grade_dict):
    """
    Converts a string, which represents a grade, into an integer and checks if the string is convertable, and stores the
    grade onto a dictionary that is handed in and back.
    :param grade:   string - the grade
    :param grade_dict: dict - keys: grades - values: frequency of a grade
    :return: dict - grade_dict
    """


    # check if inputstring element has a dot that could hint to a float number
    try:
        if "." in grade:                            # "." hints for a float number
            grade_key = int(round(float(grade)))
            print("- Warning: Rounding %s to %s" % (grade, grade_key))
        else:                                       # if no "." was found maybe its a integer
            grade_key = int(grade)

    # if the input string is not a number the Value Error is caught and a message is printed to the screen
    except ValueError:
        print("- Error: input %s is not a number" % grade)
        return grade_dict

    # check if the converted input_strings are in a meaningfully range from 1 to 5
    try:
        if 1 <= grade_key <= 5:
            if grade_key in grade_dict:
                grade_dict[grade_key] += 1

            else:
                grade_dict[grade_key] = 1

        else:     # if an input was smaller or larger than then the borders of the intervall a self defined Error is raised ...
            raise InvalidGradeError("- Error: Invalid grade %s - grade value must be between 1 and 5" % grade)

    except InvalidGradeError as grade_error:        # ... and caught. the Error message is saved to the screen
        print(grade_error.errorstring)
        return grade_dict

    return grade_dict

if __name__ == "__main__":

    # initial grade dict on which all the grades and their frequencies are stored
    grade_dict = {}
    try:
        while True:

                print("Please Enter a Grade: ")

                # convert input string to list with string elements
                input_str = input().split()

                print("Input : ", input_str)

                # check if exit ist in the input string list
                if "exit" in input_str:

                    # if only exit is handed
                    if len(input_str) == 1 and "exit" in input_str:

                        print("Input: exit\nExiting Program")
                        break
                    # if exit and some notes are handed - elimiate exit from the list - process the grade calc and stop the programm
                    else:

                        input_str.remove("exit")        # kickl out the exit from the list which will iter through
                        for grade in input_str:
                            grade_dict = checkGrade(grade, grade_dict)
                        calcGradeAverage(grade_dict)
                        print("Input: exit\nExiting Program")
                        break

                else:
                        for grade in input_str:
                            grade_dict = checkGrade(grade, grade_dict)
                        calcGradeAverage(grade_dict)

    except KeyboardInterrupt:
        print("Good Bye - Stopped Programm via STRG + C")

