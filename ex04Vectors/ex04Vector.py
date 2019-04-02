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
        self._vector_data = copy.deepcopy(input_list)

    def __len__(self):
        return len(self._vector_data)

    def __getitem__(self, key):
        return self._vector_data[key]

    def __setitem__(self, key, value):

        self._vector_data[key] = value
        print(self._vector_data)

    def __add__(self, other):

        if len(self) == len(other):

            return Vector([self._vector_data[i] + other._vector_data[i] for i in range(0, len(self._vector_data))])
        else:
            raise ValueError("!! ERROR - len of summand one {} is not len of summand two {}".format(len(self), len(other)))

    def __iadd__(self, other):

        if len(self) == len(other):
            return Vector([self._vector_data[i] + other._vector_data[i] for i in range(0, len(self._vector_data))])
        else:
            raise ValueError("!! ERROR - len of summand one {} is not len of summand two {}".format(len(self), len(other)))

    def __sub__(self, other):

        if len(self) == len(other):
            return Vector([self._vector_data[i] - other._vector_data[i] for i in range(0, len(self._vector_data))])
        else:
            raise ValueError("!! ERROR - len of minuend {} is not len of subtrahend {}".format(len(self), len(other)))

    def __isub__(self, other):

        if len(self) == len(other):
            return Vector([self._vector_data[i] - other._vector_data[i] for i in range(0, len(self._vector_data))])
        else:
            raise ValueError("!! ERROR - len of minuend {} is not len of subtrahend {}".format(len(self), len(other)))


    def __str__(self):
        start_str = "["
        end_str = "]"

        for item in self._vector_data:
            start_str = start_str + str(item) + ","

        return start_str[:-1] + end_str

    def __del__(self):
        print("-  Deleting Vector Instance with elements {}".format(self.__str__()))

    # own getter methods
    def norm(self):
        return_norm_val = 0
        for item in self._vector_data:
            return_norm_val += item**2
        return math.sqrt(return_norm_val)


class Vector3d(Vector):

    def __init__(self, x=0, y=0, z=0):
        super().__init__([x,y,z])

    # private setter methods
    def __setX(self, x):
        self._vector_data[0] = x

    def __setY(self, y):
        self._vector_data[1] = y

    def __setZ(self, z):
        self._vector_data = z

    # private getter methods
    def __getX(self):
        return self._vector_data[0]

    def __getY(self):
        return self._vector_data[1]

    def __getZ(self):
        return self._vector_data[2]

    def crossProduct(self, other):

        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x

        return Vector3d(x, y, z)

    x = property(__getX, __setX)
    y = property(__getY, __setY)
    z = property(__getZ, __setZ)



vec1 = Vector([1,2,3,4])
vec2 = Vector([10,20,30,40])
print(vec1[2])
print(len(vec2))
print(vec1 + vec2)
print(vec1)
vec3 = vec1 - vec2
print(vec3.norm())
vec4 = Vector3d(2, 3, 4)
vec5 = Vector3d(5, 6, 7)
vec6 = Vector3d.crossProduct(vec4, vec5)
print(len(vec6))
print(vec6)
print(vec6.norm())
vec7 = Vector3d(z=5)
vec7.y = 9
vec8 = Vector([100, 200, 300])
vec7 += vec8
print(vec7)
try:
    vec7 -= vec1
except Exception as ex:
    print(ex)




