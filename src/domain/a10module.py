class IterableDataStructure:
    class Iterator:
        def __init__(self, data_structure):
            self._data_structure = data_structure
            self._position = 0

        def __next__(self):
            #  It stops the iteration when other elements are not available
            if self._position > len(self._data_structure) - 1:
                raise StopIteration
            # Else, it moves to the next element
            self._position = self._position + 1
            return self._data_structure[self._position - 1]

    def __init__(self):
        self._data_structure = []

    def __iter__(self):
        return self.Iterator(self)

    def append(self, item):
        self._data_structure.append(item)

    def pop(self, item):
        self._data_structure.remove(item)

    def __getitem__(self, item_index):
        return self._data_structure[item_index]

    def __setitem__(self, item_index, value):
        self._data_structure[item_index] = value

    def __len__(self):
        return len(self._data_structure)

    def get_all(self):
        return self._data_structure


def filter_function(list_to_be_filtered, function):
    filtered_list = []
    length = len(list_to_be_filtered)
    for index in range(length):
        if function(list_to_be_filtered[index]):
            filtered_list.append(list_to_be_filtered[index])
    return filtered_list


def gnome_sort(list_to_be_sorted, comparison_function):
    index = 0
    list_length = len(list_to_be_sorted)
    while index < list_length:
        if index == 0:
            index = index + 1
        elif comparison_function(list_to_be_sorted[index - 1], list_to_be_sorted[index]):
            index = index + 1
        else:
            list_to_be_sorted[index - 1], list_to_be_sorted[index] = list_to_be_sorted[index], list_to_be_sorted[index - 1]
            index = index - 1
    return list_to_be_sorted
