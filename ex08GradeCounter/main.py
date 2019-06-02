

def checkGrade(grade):

    print("- Checking input %s" % str(grade))



if __name__ == "__main__":

    input_str = "run programm"

    while input_str != "exit":
        print("Please Enter a Grade: ")
        input_str = input()

        #if input_str == "exit":
        #    print("Good Bye - Stopping Program")
        #    break

        print("input: %s" % input_str, " input str == exit ", input_str == "exit")

        if input_str == KeyboardInterrupt:
            print("STRG + C")

        try:
            checkGrade(input_str)

        except KeyboardInterrupt:
            print("Good Bye - Stopped Programm via STRG + C")
        except:
            print("Something went South")