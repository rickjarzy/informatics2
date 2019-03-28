# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A

import copy

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

    def __str__(self):
        start_str = "["
        end_str = "]"

        for item in self._vector_data:
            start_str = start_str + str(item) + ","

        return start_str[:-1] + end_str


v1 = Vector([1,2,3,4,5])
print(len(v1))
print(v1)
print(v1[-1])
print(v1._vector_data)





