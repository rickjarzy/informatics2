import argparse


def create_characte_dict(input_word, upper_case=False):
    """

    :param input_word:
    :param upper_case:
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


def count_chars(input_string_list, upper_case=False, verbose=False):
    """

    :param input_string_list:
    :param upper_case:
    :param verbose:
    :return:
    """

    if verbose:
        overall_collect_string = ""
        for input_string_element in input_string_list:

            overall_collect_string = overall_collect_string+input_string_element

            print("Word: ", input_string_element)
            counted_chars_dict = create_characte_dict(input_string_element, upper_case=upper_case)

            # join all the single characters with their frequency , sort them and join a single string
            return_string = "".join(sorted([character+str(counted_chars_dict[character])+" " for character in counted_chars_dict]))
            print(return_string)

        overall_count_dict = create_characte_dict(overall_collect_string, upper_case=upper_case)
        overall_count_string = "".join(sorted([character+str(overall_count_dict[character])+" " for character in overall_count_dict]))
        print("Overall count\n", overall_count_string)

    else:
        overall_count_dict = create_characte_dict(input_string_list, upper_case=upper_case)
        overall_count_string = "".join(sorted([character + str(overall_count_dict[character]) + " " for character in overall_count_dict]))
        print(overall_count_string)

if __name__ == "__main__":

    parser = argparse.ArgumentParser("counts the occurrences of letters in words")
    parser.add_argument("word", type=str, nargs='*', help="input string which letters will be counted")
    parser.add_argument("-c", "--casesensitive", help="count lower and upper case letters individually", action="store_true")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")
    parser.add_argument("--min", type=int, help="minimum number of occurrences to be considered")

    args = parser.parse_args()

    count_chars(args.word, upper_case=args.casesensitive, verbose=args.verbosity)

    print("Programm ENDE")

