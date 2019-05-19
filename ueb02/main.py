import argparse





if __name__ == "__main__":


    parser = argparse.ArgumentParser("Generates an animated visualization of GRACE satellite visibility to the GPS constellation for a single day.")

    parser.add_argument("date", type=str, nargs='*', help="date to visualize (format: YYYY-MM-DD)")
    parser.add_argument("-c", "--casesensitive", help="count lower and upper case letters individually", action="store_true")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")
    parser.add_argument("--min", type=int, help="minimum number of occurrences to be considered")

    print("Programm ENDE")