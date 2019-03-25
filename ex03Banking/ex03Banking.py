class BankAccount:
    """
    Class for Bankaccounts
    """
    # Konstruktor with an optional attribute
    def __init__(self, holder, balance=0.):
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
        if float(balance) >= 0. :
            # if balance input is valid assign it to instance attribute
            self.__balance = float(balance)
            print("".format(self.__holder, self.__balance))
        else:
            # raise error and print screenmessage and abort instantiation of class if input is not valid
            print("!! instance creation - FAILED - \   input balance = {} | is negative or not a number".format(balance))
            raise ValueError

    # print bank account information to screen if print() is called
    def __str__(self):
        """
        prints the bank account information to the screen if instance is printed via print()
        :return: string with bank account information
        """
        return "\n- bank account owner: {} \n- balance: {}".format(self.__holder, self.__balance)

    def __del__(self):
        """
        overwrite __del__ so it gives you some prints when you delete an instance
        :return: Nothing
        """
        print("- Bank Account of {} was deleted ".format(self.__holder))

    # getter method to print the bank account holder to the screen
    def get_holder(self):
        """
        getter method to print the bank account owner
        :return: print bank acctount owner to output device
        """
        print("- Bank Account Owner: %s" % self.__holder)

    def get_holder_name(self):
        """
        returns the bank accoung holder name as string
        :return: the bank account holder as string
        """
        return self.__holder

    # setter methof to add cash to the bank account balance
    def deposit(self, deposite_amount):
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
            print("- deposit - SUCCESS -\n  deposit {} to {} ".format(deposite_amount, self.__holder))
            return True
        else:
            print("!! deposit - FAILED - \n   input deposit ammount = {} | is negative or not a number".format(deposite_amount))
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
            print("- withdraw - SUCCESS - \n  withdraw {} from {}".format(withdraw_amount, self.__holder))
            return True
        else:
            print("!! withdraw - FAILED - \n   input withdrawl ammount = {} | is negative, not a number or bigger than the balance\n"
                  "   balance: {}".format(withdraw_amount, self.__balance))
            return False

    # setter method transfer money from one instance object to another
    def transfer(self,transfer_object,transfer_ammount):
        """
        allows to transfer a certain amount of money from one class to the other
        :param object: other class instance
        :param transfer_ammount: ammount of money that will be subtracted from self and deposit at the other instance
        :return: True/False if transfer is valid
        """
        check_sum_transfer_withdraw =self.withdraw(transfer_ammount)

        if check_sum_transfer_withdraw:
            print("- transfer - SUCCESS -\n  {} from {} to bank account of {} - SUCCESS -".format(transfer_ammount, self.__holder,
                                                                       transfer_object.get_holder_name()))

            transfer_object.deposit(transfer_ammount)

        else:
            print("!! transfer - FAILED -\n   {} from {} to bank account of {} ".format(transfer_ammount, self.__holder,
                                                                       transfer_object.get_holder_name()))




account1 = BankAccount("Bender")
print(account1)
account1.withdraw(100)
account1.deposit(1000)
account1.withdraw(100)
print(account1)
account2 = BankAccount("Marvin")
account1.transfer(account2, 1000)
account1.transfer(account2, 500)
account2.deposit("lkjklj")
print(account1)
del account1
print(account2)


#konto1 = BankAccount("Paul", "200")
#konto2 = BankAccount("Andi", "3000")
#konto1.get_holder()
#konto1._BankAccount__balance = -1000
#konto1.withdraw(6000)
#konto1._BankAccount__holder = "Josef"
#konto1.deposit(300)
#print(konto1.__dict__)
#print(konto1)
#konto2.transfer(konto1, 200)
#print(konto1)
