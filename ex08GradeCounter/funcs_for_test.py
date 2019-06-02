import ex08GradeCounter
def print_something():
    print("imported function file")
    print(locals())

print("\ndieser Code wird ausgeführt obwohl wir ihn gar nicht aufrufen\n")


if __name__ == "__main__":

    print("Ich bin das main programm ")
    print(locals())