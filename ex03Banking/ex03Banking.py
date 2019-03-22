class BankAccount:
    """
    Class for Bankaccounts
    """
    # Konstruktor with an optional attribute
    def __init__(self, holder, balance=0):
        """
        Constructor for class BankAccount. If the balance input is not a positive number greater 0 a ValueError is raised
        and the class creation is aborted.
        :param holder: string
        :param balance: integer
        """
        # assign holder name to instance attribute
        self.__holder = holder
        self.irgendwas = None
        # check if input balance is a number and not negative - if not a positive number raise a ValueError and stop instance creation
        if float(balance) > 0 :
            # if balance input is valid assign it to instance attribute
            self.__balance = float(balance)
            print(" - created bank account for {} successfully\n - balance: {}".format(self.__holder, self.__balance))
        else:
            # raise error and print screenmessage and abort instantiation of class if input is not valid
            print("! input balance = {} | is negative or not a number".format(balance))
            raise ValueError

    # print bank account information to screen if print() is called
    def __str__(self):
        """
        prints the bank account information to the screen if instance is printed via print()
        :return: string with bank account information
        """
        return "\n - bank account owner: {} \n - balance: {}".format(self.__holder, self.__balance)

    # getter method to print the bank account holder to the screen
    def get_holder(self):
        """
        getter method to print the bank account owner
        :return: print bank acctount owner to output device
        """
        print("Bank Account Owner: %s" % self.__holder)

    # setter methof to add cash to the bank account balance
    def desposit(self, deposite_amount):
        """
        the input of the setter function is subtracted from the actual bank account balance. it is first
        checked if the input withdraw amount is greater than 0 and number. If that fits the input is added to
        the balance and True is returned. If the input fits not an errormessage is written
        to the screen and False returned as the return value

        :param deposite_amount:     a number - is checked if valid
        :return:                    True / False  - depending if deposit was possible or not
        """
        if float(deposite_amount) > 0:
            self.__balance += float(deposite_amount)
            return True
        else:
            print("! input deposit ammount = {} | is negative or not a number".format(deposite_amount))
            return False


    # setter method to withdraw cash from the bank account balance
    def withdraw(self, withdraw_amount):
        """
        the input of the setter function is subtracted from the actual bank account balance. it is first
        checked if the input withdraw amount is greater than 0 and number. If that fits the input is checked if it is smaller or equals
        the actuall instance attribute balance. If that is True the withdraw_amount is subtracted from the attribute balance
        and True is returned. If the input fits not an errormessage is written to the screen and False returned

        :param withdraw_amount:     a number - is checked if valid
        :return:                    True / False  - depending if withdrawl is possible or not
        """
        if float(withdraw_amount) <= self.__balance and float(withdraw_amount) > 0:
            self.__balance -= float(withdraw_amount)
            return True
        else:
            print("! input withdrawl ammount = {} | is negative, not a number or bigger than the balance\n"
                  "- balance {}".format(withdraw_amount, self.__balance))
            return False


konto1 = BankAccount("Paul", "200")
konto1.get_holder()
konto1._BankAccount__balance = -1000
konto1.withdraw(6000)
#konto1._BankAccount__holder = "Josef"
konto1.desposit(300)
print(konto1.__dict__)
print(konto1)
print(help(BankAccount))