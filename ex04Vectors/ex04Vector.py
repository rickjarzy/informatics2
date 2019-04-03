# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A

import copy
import math

class Vector:
    """
    class Vector
    """

    def __init__(self, input_list):
        """
        Constructor of class Vector
        :param input_list: list with integer elements
        """

        self._vector_data = copy.deepcopy(input_list)

    def __len__(self):
        """
        overwrite the len method so a vector instance can have a length
        :return: length of the self._vector_data list
        """
        return len(self._vector_data)

    def __getitem__(self, key):
        """
        overwrite the __getitem__ method so you are able to select a single element in the data
        :param key: integer that selects a dataelement at a certain position
        :return: the element of the self._vector_data list at the key-index
        """
        return self._vector_data[key]

    def __setitem__(self, key, value):

        """
        overwrite the __setitem__ method so you are able to select a certain element with an index and replace it
        :param key:     index to access the self._vector_data
        :param value:   value that replacec the actual element at index key
        :return:        no return value
        """
        self._vector_data[key] = value
        print(self._vector_data)


    def __add__(self, other):
        """
        overwrites the __add__ method so you can create the sum of two instances of the class vector.
        for that all elements of the self._vector_data will summerized via a for loop and saved in a new list.
        with this list a new instance if the class Vector is created and returned
        :param other: an other instance of class Vector
        :return: a new instance of class Vector
        """
        # check if the _vector_data lists have the same length
        if len(self) == len(other):

            return Vector([self._vector_data[i] + other._vector_data[i] for i in range(0, len(self._vector_data))])
        else:
            raise ValueError("\n!! ERROR - len of summand one {} is not len of summand two {}".format(len(self), len(other)))

    def __iadd__(self, other):

        """
        overwrites the __iadd__ method so you can increment/summarize two instances of the class vector.
        for that all elements of the self._vector_data will summerized via a for loop and saved in a new list.
        with this list a new instance if the class Vector is created and returned
        :param other: an other instance of class Vector
        :return: a new instance of class Vector
        """
        # check if the _vector_data lists have the same length
        if len(self) == len(other):
            return Vector([self._vector_data[i] + other._vector_data[i] for i in range(0, len(self._vector_data))])
        else:
            raise ValueError("\n!! ERROR - len of summand one {} is not len of summand two {}".format(len(self), len(other)))

    def __sub__(self, other):
        """
        overwrites the __sub__ method so you can subtract two instances of the class vector.
        for that all elements of the self._vector_data will be subtracted via a for loop and saved in a new list.
        with this list a new instance if the class Vector is created and returned
        :param other: an other instance of class Vector
        :return: a new instance of class Vector
        """
        # check if the _vector_data lists have the same length
        if len(self) == len(other):
            return Vector([self._vector_data[i] - other._vector_data[i] for i in range(0, len(self._vector_data))])
        else:
            raise ValueError("\n!! ERROR - len of minuend {} is not len of subtrahend {}".format(len(self), len(other)))

    def __isub__(self, other):
        """
        overwrites the __isub__ method so you can subtracted/decrement two instances of the class vector.
        for that all elements of the self._vector_data will be subtracted via a for loop and saved in a new list.
        with this list a new instance if the class Vector is created and returned
        :param other: an other instance of class Vector
        :return: a new instance of class Vector
        """
        # check if the _vector_data lists have the same length
        if len(self) == len(other):
            return Vector([self._vector_data[i] - other._vector_data[i] for i in range(0, len(self._vector_data))])
        else:
            raise ValueError("\n!! ERROR - len of minuend {} is not len of subtrahend {}".format(len(self), len(other)))


    def __str__(self):
        """
        the string representation if you print an instance to the screen
        :return: string with a list representation of the self._vector_data content
        """

        start_str = "["
        end_str = "]"

        for item in self._vector_data:
            start_str = start_str + str(item) + ","

        return start_str[:-1] + end_str

    def __del__(self):
        """
        overwrite the __del__ method so if an instance gets deleted you will see a notification on the screen
        :return: No return value
        """
        print("-  Deleting Vector Instance of type {} with elements {}".format(type(self), self.__str__()))

    # own getter methods
    def norm(self):
        return_norm_val = 0
        for item in self._vector_data:
            return_norm_val += item**2
        return math.sqrt(return_norm_val)


class Vector3d(Vector):
    """
    class Vector3d inherits all the methods from class Vector
    todo: check if inputs that are handed are numbers and nothing else
    """

    def __init__(self, x=0, y=0, z=0):
        """
        Constructor for the class Vector3d. 3 values can be handed and will get stored in the same way as in the class Vector
        from wich class Vector3d inherits. The 3 values x, y, z will be stored as a copy of a list on the protected variable
        self._vector_data
        self.vector_data = copy.deepcopy([x, y, z])
        :param x: input value for first element in _vector_data
        :param y: input value for second element in _vector_data
        :param z: input value for third element in _vector_data
        """
        print("+  Create 3D Vector - data: {}".format([x, y, z]))
        # call the base class and save it to the protected attribute _vector_data
        super().__init__([x,y,z])

    # private setter methods
    def __setX(self, x):
        """
        set x value in the list of self._vector_data
        :param x: integer value that will be set on first position of the _vector_data
        :return: no return value
        """
        self._vector_data[0] = x

    def __setY(self, y):
        """
        set y value in the list of self._vector_data
        :param y: integer value that will be set on second position of the _vector_data
        :return: no return value
        """
        self._vector_data[1] = y

    # private getter methods
    def __getX(self):
        """
        select the x coordinate of the _vector_data list and return it
        :return: no return value
        """
        return self._vector_data[0]

    def __getY(self):
        """
        select the y coordinate of the _vector_data list and return it
        :return: no return value
        """
        return self._vector_data[1]

    # using a decorater to define a property that can be called like a public attribute from outside the class
    # https://www.programiz.com/python-programming/property
    # property getter method
    @property
    def z(self):
        """
        defines z as property and allowes it to be called from outside of the class Vector3d and get the value for the z coordinate
        in the protected _vector_data attribute

        :return: number - z value of _vector_data
        """
        return self._vector_data[2]

    # the setter method for the property
    @z.setter
    def z(self, value):
        """
        setter method for property z. allows to set the z coordinate from outside the class Vector3d ro be set on the protected
        attribute _vector_data
        :param value: new value for the third element in the _vector_data
        :return: no return value
        """
        self._vector_data[2] = value

    def crossProduct(self, other):

        """
        create the cross product of to instances of the class Vector3d with their protected attribute _vector_data
        :param other: instance of class Vector3d
        :return: new instance of the class Vector3d with the result of the cross product as result. result gets stored on the
        instance _vector_data attribute
        """

        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x

        return Vector3d(x, y, z)

    # properties - can be set outside the class Vector3d
    x = property(__getX, __setX)
    y = property(__getY, __setY)


# main program code
if __name__ == "__main__":
    print("================================\nEX04 - Vector\n================================\n")
    vec1 = Vector([1,2,3,4])
    vec2 = Vector([10,20,30,40])
    print("Index 2 of vec1:", vec1[2])
    print("len of vec2: ", len(vec2))
    print("sum vec1 + vec2: ", vec1 + vec2)
    print("vec1: ", vec1)
    vec3 = vec1 - vec2
    print("norm vec3: ", vec3.norm())
    print("create vec4")
    vec4 = Vector3d(2, 3, 4)
    print("create vec5")
    vec5 = Vector3d(5, 6, 7)
    print("create vec6 via crossporoduct")
    vec6 = Vector3d.crossProduct(vec4, vec5)
    print("len of vec6 (result instance of crossProduct): ", len(vec6))
    print("vec6 (result instance of crossProduct): ", vec6)
    print("vec6.norm(): ", vec6.norm())
    print("create vec7")
    vec7 = Vector3d(z=5)
    vec7.y = 9
    vec7.z = 900000
    print("vec7: ", vec7)
    print("create vec8")
    vec8 = Vector([100, 200, 300])
    print("sum of vec7 and vec8: ", vec7 + vec8)
    vec7 += vec8
    print("vec7: ", vec7)
    print("subtract vec1 from vec7")
    try:
        vec7 -= vec1
    except Exception as ex:
        print(ex)

    print("================================\nProgramm ENDE\n================================\n")




