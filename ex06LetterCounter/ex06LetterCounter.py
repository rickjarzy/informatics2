import argparse


def create_characte_dict(input_word, verbose=False):

    counted_chars_dict = {}
    # walk throu the string elements
    for character in input_word:

        # if the character has been allready stored increment it, else add a new key to the dict
        if character in counted_chars_dict:
            counted_chars_dict[character] += 1
        else:
            counted_chars_dict[character] = 1

    if verbose:
        print("Word: ", input_word)
        print("".join(sorted([character+str(counted_chars_dict[character])+" " for character in counted_chars_dict])))

    return counted_chars_dict


def count_chars(input_string_list, upper_case=False, verbose=False):
    print("input list\n", input_string_list)

    # if the casesensitive input parameter from the cmd is NOT set
    if upper_case is False:
        # join all input strings to one string and make em lower case
        input_string = "".join(input_string_list).lower()
    else:
        input_string = "".join(input_string_list)

    counted_chars_dict = create_characte_dict(input_string, verbose=verbose)

    # join all the single characters with their frequency , sort them and join a single string
    return_string = "".join(sorted([character+str(counted_chars_dict[character])+" " for character in counted_chars_dict]))

    print(return_string)

if __name__ == "__main__":

    parser = argparse.ArgumentParser("counts the occurrences of letters in words")
    parser.add_argument("word", type=str, nargs='*', help="input string which letters will be counted")
    parser.add_argument("-c", "--casesensitive", help="count lower and upper case letters individually", action="store_true")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")
    parser.add_argument("--min", type=int, help="minimum number of occurrences to be considered")

    args = parser.parse_args()

    count_chars(args.word, upper_case=args.casesensitive, verbose=args.verbosity)

    print("Programm ENDE")

