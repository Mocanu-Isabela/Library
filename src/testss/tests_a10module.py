import unittest
from src.domain.a10module import IterableDataStructure, gnome_sort, filter_function


class IterableDataStructureTests(unittest.TestCase):
    def test_iterable_data_structure(self):
        iterable_data_structure_list = IterableDataStructure()
        iterable_data_structure_list.append(0)
        iterable_data_structure_list.append(1)
        iterable_data_structure_list.append(2)
        iterable_data_structure_list.append(3)
        for i in range(0, 4):
            self.assertEqual(iterable_data_structure_list[i], i)
        self.assertEqual(len(iterable_data_structure_list), 4)
        self.assertEqual(iterable_data_structure_list.__getitem__(2), 2)
        iterable_data_structure_list.__setitem__(2, 8)
        self.assertEqual(iterable_data_structure_list.__getitem__(2), 8)
        iterable_data_structure_list.pop(0)
        all_elements = iterable_data_structure_list.get_all()
        self.assertEqual(all_elements, [1, 8, 3])


class GnomeSortAndFilterTests(unittest.TestCase):
    def test_gnome_sort(self):
        test_list_1 = [8, 10, -2, 0, 5, -7, -9, 1]
        #  sort in ascending order list 1
        sorted_list = gnome_sort(test_list_1, lambda x, y: x < y)
        self.assertEqual(sorted_list, [-9, -7, -2, 0, 1, 5, 8, 10])
        test_list_1 = [8, 10, -2, 0, 5, -7, -9, 1]
        #  sort in descending order list 1
        sorted_list = gnome_sort(test_list_1, lambda x, y: x > y)
        self.assertEqual(sorted_list, [10, 8, 5, 1, 0, -2, -7, -9])

        test_list_2 = ["Followers", "The Glass Hotel", "Long Bright River", "Uncanny Valley", "Murder on the Orient Express", "A Study in Scarlet"]
        #  sort in ascending order list 2
        sorted_list = gnome_sort(test_list_2, lambda x, y: x < y)
        self.assertEqual(sorted_list, ["A Study in Scarlet", "Followers", "Long Bright River", "Murder on the Orient Express", "The Glass Hotel", "Uncanny Valley"])
        test_list_2 = ["Followers", "The Glass Hotel", "Long Bright River", "Uncanny Valley", "Murder on the Orient Express", "A Study in Scarlet"]
        #  sort in descending order list 2
        sorted_list = gnome_sort(test_list_2, lambda x, y: x > y)
        self.assertEqual(sorted_list, ["Uncanny Valley", "The Glass Hotel", "Murder on the Orient Express", "Long Bright River", "Followers", "A Study in Scarlet"])

        test_list_3 = []
        #  sort in ascending order list 3
        sorted_empty_list = gnome_sort(test_list_3, lambda x, y: x < y)
        self.assertEqual(sorted_empty_list, [])

    def test_filter(self):
        test_list = [8, 10, -2, 0, 5, -7, -9, 1]

        filtered_list = filter_function(test_list, lambda x: x > 0)
        self.assertEqual(filtered_list, [8, 10, 5, 1])
        filtered_list = filter_function(test_list, lambda x: x < 2)
        self.assertEqual(filtered_list, [-2, 0, -7, -9, 1])
