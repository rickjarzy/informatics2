# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A

import argparse


def create_characte_dict(input_word, upper_case=False):
    """
    counts the single caracters in the handed word

    :param input_word: string -
    :param upper_case: bool - if flag is set, this
    :return:
    """

    # if the casesensitive input parameter from the cmd is NOT set
    if upper_case is False:
        # join all input strings to one string and make em lower case
        input_string = "".join(input_word).lower()
    else:
        input_string = "".join(input_word)


    counted_chars_dict = {}
    # walk throu the string elements
    for character in input_string:

        # if the character has been allready stored increment it, else add a new key to the dict
        if character in counted_chars_dict:
            counted_chars_dict[character] += 1
        else:
            counted_chars_dict[character] = 1

    return counted_chars_dict


def count_chars(input_string_list, upper_case=False, verbose=False, min=0):
    """
    returns the counted characters in a structured way on the screen. prints different detail levels if verbose is set

    :param input_string_list: list - list with the input text
    :param upper_case: Bool - if this flag is set the the Upper case letters will be counted seperatly
    :param verbose: bool - activates additional screen prints
    :param min: int - filters the screen print so only letters equal bigger the input will be streamed to the screen
    :return: no return value
    """

    if verbose:
        overall_collect_string = ""
        for input_string_element in input_string_list:

            # collect the single words in the input string list to process an overall character count at the end of the if statement
            overall_collect_string = overall_collect_string+input_string_element


            # count characters of a single word of input list
            counted_chars_dict = create_characte_dict(input_string_element, upper_case=upper_case)

            if verbose > 1:
                return_string = "".join(sorted(["%s = %s\n" % (key, str(character)) for key, character in counted_chars_dict.items() if character >= min]))
            else:
                # join all the single characters with their frequency , sort them and join a single string
                return_string = "".join(sorted([key+str(character)+" " for key, character in counted_chars_dict.items() if character >= min]))


            if len(return_string) > 0:
                print("Word: ", input_string_element)
                print(return_string)

        # count and show the entire character frequencies of the input word list
        overall_count_dict = create_characte_dict(overall_collect_string, upper_case=upper_case)
        if verbose > 1:
            overall_count_string = "".join(sorted(["%s = %s\n" % (key, str(character)) for key, character in counted_chars_dict.items() if character >= min]))
        else:
            overall_count_string = "".join(sorted([key + str(character) + " " for key, character in counted_chars_dict.items() if character >= min]))
        print("Overall count")
        print(overall_count_string)

    else:
        # create the character frequency with out additional screen info
        overall_count_dict = create_characte_dict(input_string_list, upper_case=upper_case)
        if verbose > 1:
            overall_count_string = "".join(sorted(["%s = %s\n" % (key, str(character)) for key, character in overall_count_dict.items() if character >= min]))
        else:
            overall_count_string = "".join(sorted([key + str(character) + " " for key, character in overall_count_dict.items() if character >= min]))
        print(overall_count_string)

if __name__ == "__main__":

    # Setting up the position and optional arguments
    parser = argparse.ArgumentParser("counts the occurrences of letters in words")
    parser.add_argument("word", type=str, nargs='*', help="input string which letters will be counted")
    parser.add_argument("-c", "--casesensitive", help="count lower and upper case letters individually", action="store_true")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")
    parser.add_argument("--min", type=int, help="minimum number of occurrences to be considered")

    args = parser.parse_args()
    # set the min filter value for the screen output
    if args.min:
        min_count = args.min
    else:
        min_count = 0

    # call function to count the letters
    count_chars(args.word, upper_case=args.casesensitive, verbose=args.verbosity, min=min_count)

    print("Programm ENDE")

