import unittest

import pygame

import game


class TestGetGrid(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()
        cls.game.get_grid()

    def test_get_grid_fills_grid_with_lists(self):
        for item in self.game.grid:
            self.assertIsInstance(item, list)

    def test_lists_in_grid_contain_dicts(self):
        for list_ in self.game.grid:
            for item in list_:
                self.assertIsInstance(item, dict)

    def test_dicts_in_lists_contain_expected_keys(self):
        for list_ in self.game.grid:
            for dict_ in list_:
                self.assertIn("color", dict_)
                self.assertIn("rect", dict_)

    def test_dicts_in_lists_contain_expected_values(self):
        for list_ in self.game.grid:
            for dict_ in list_:
                self.assertEqual(dict_["color"], self.game.black)
                self.assertIsInstance(dict_["rect"], pygame.Rect)

    def test_grid_has_expected_number_of_columns(self):
        expected_number_of_columns = len(self.game.rect_locations)
        self.assertEqual(len(self.game.grid), expected_number_of_columns)

    def test_grid_has_expected_number_of_rows(self):
        expected_number_of_rows = len(self.game.rect_locations)
        for list_ in self.game.grid:
            self.assertEqual(len(list_), expected_number_of_rows)

    def test_rects_in_dicts_are_the_expected_size_and_at_the_expected_location(self):
        expected_size = (64, 64)
        for list_, x in zip(self.game.grid, self.game.rect_locations):
            for dict_, y in zip(list_, self.game.rect_locations):
                self.assertEqual(dict_["rect"].size, expected_size)
                self.assertEqual(dict_["rect"].x, x)
                self.assertEqual(dict_["rect"].y, y)

    def test_get_grid_clears_grid(self):
        grid = self.game.grid
        self.game.get_grid()
        self.assertEqual(grid, self.game.grid)


class TestColumnFull(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()
        cls.game.get_grid()

    def test_column_full_returns_false_when_column_contains_all_black_disks(self):
        self.assertFalse(self.game.column_full(column=self.game.grid[0]))

    def test_column_full_returns_false_when_column_contains_some_black_disks(self):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[0][-2]["color"] = self.game.blue
        self.assertFalse(self.game.column_full(column=self.game.grid[0]))

    def test_column_full_returns_true_when_column_contains_no_black_disks(self):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[0][-2]["color"] = self.game.blue
        self.game.grid[0][-3]["color"] = self.game.red
        self.game.grid[0][-4]["color"] = self.game.blue
        self.game.grid[0][-5]["color"] = self.game.red
        self.game.grid[0][-6]["color"] = self.game.blue
        self.game.grid[0][-7]["color"] = self.game.red
        self.assertTrue(self.game.column_full(column=self.game.grid[0]))


class TestDropDiskInColumn(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()
        cls.game.get_grid()
        cls.column_length = len(cls.game.rect_locations)

    def test_last_disk_in_column_that_is_red(self):
        column = 0
        self.game.current_players_disk_color = self.game.red
        self.game.drop_disk_in_column(self.game.grid[column])
        self.assertEqual(self.game.grid[column][-1]["color"], self.game.red)

    def test_second_to_last_disk_in_column_is_blue(self):
        column = 0
        self.game.current_players_disk_color = self.game.blue
        self.game.drop_disk_in_column(self.game.grid[column])
        self.assertEqual(self.game.grid[column][-2]["color"], self.game.blue)


class TestFourInARow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()

    def setUp(self):
        self.game.get_grid()

    def test_returns_none_when_grid_is_empty(self):
        self.assertIs(self.game.four_in_a_row(), None)

    def test_returns_none_when_grid_is_not_empty_but_has_no_four_in_a_row(self):
        self.game.grid[0][0]["color"] = self.game.red
        self.game.grid[0][6]["color"] = self.game.red
        self.game.grid[6][-6]["color"] = self.game.red
        self.game.grid[6][0]["color"] = self.game.red
        self.assertIs(self.game.four_in_a_row(), None)

    def test_returns_expected_disks_when_grid_has_4_horizontally_adjacent_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-1],
            self.game.grid[1][-1],
            self.game.grid[2][-1],
            self.game.grid[3][-1],
        ]
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[1][-1]["color"] = self.game.red
        self.game.grid[2][-1]["color"] = self.game.red
        self.game.grid[3][-1]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row(), expected_disks)

    def test_returns_expected_disks_when_grid_has_4_vertically_adjacent_disks_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-4],
            self.game.grid[0][-3],
            self.game.grid[0][-2],
            self.game.grid[0][-1],
        ]
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[0][-2]["color"] = self.game.red
        self.game.grid[0][-3]["color"] = self.game.red
        self.game.grid[0][-4]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row(), expected_disks)

    def test_returns_expected_disks_when_grid_has_4_diagonally_descending_adjacent_disks_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-4],
            self.game.grid[1][-3],
            self.game.grid[2][-2],
            self.game.grid[3][-1],
        ]
        self.game.grid[0][-4]["color"] = self.game.red
        self.game.grid[1][-3]["color"] = self.game.red
        self.game.grid[2][-2]["color"] = self.game.red
        self.game.grid[3][-1]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row(), expected_disks)

    def test_returns_expected_disks_when_grid_has_4_diagonally_ascending_adjacent_disks_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-1],
            self.game.grid[1][-2],
            self.game.grid[2][-3],
            self.game.grid[3][-4],
        ]
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[1][-2]["color"] = self.game.red
        self.game.grid[2][-3]["color"] = self.game.red
        self.game.grid[3][-4]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row(), expected_disks)


class TestFourInARowHorizontal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()

    def setUp(self):
        self.game.get_grid()

    def test_returns_none_when_grid_is_empty(self):
        self.assertIs(self.game.four_in_a_row_horizontal(), None)

    def test_returns_none_when_row_has_3_horizontally_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.blue
        self.game.grid[1][-1]["color"] = self.game.blue
        self.game.grid[2][-1]["color"] = self.game.blue
        self.assertIs(self.game.four_in_a_row_horizontal(), None)

    def test_returns_none_when_row_has_4_horizontally_adjacent_disks_of_different_colors(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[1][-1]["color"] = self.game.blue
        self.game.grid[2][-1]["color"] = self.game.red
        self.game.grid[3][-1]["color"] = self.game.blue
        self.assertIs(self.game.four_in_a_row_horizontal(), None)

    def test_returns_expected_disks_when_row_has_4_horizontally_adjacent_disks_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-1],
            self.game.grid[1][-1],
            self.game.grid[2][-1],
            self.game.grid[3][-1],
        ]
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[1][-1]["color"] = self.game.red
        self.game.grid[2][-1]["color"] = self.game.red
        self.game.grid[3][-1]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row_horizontal(), expected_disks)

    def test_returns_expected_disks_row_has_4_horizontally_adjacent_disks_of_the_same_color_in_the_last_row(
        self,
    ):
        expected_disks = [
            self.game.grid[3][0],
            self.game.grid[4][0],
            self.game.grid[5][0],
            self.game.grid[6][0],
        ]
        self.game.grid[3][0]["color"] = self.game.red
        self.game.grid[4][0]["color"] = self.game.red
        self.game.grid[5][0]["color"] = self.game.red
        self.game.grid[6][0]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row_horizontal(), expected_disks)

    def test_returns_expected_disks_when_row_has_4_horizontally_adjacent_disks_of_the_same_color_preceded_by_3_disks_of_varying_color(
        self,
    ):
        expected_disks = [
            self.game.grid[3][-1],
            self.game.grid[4][-1],
            self.game.grid[5][-1],
            self.game.grid[6][-1],
        ]
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[1][-1]["color"] = self.game.blue
        self.game.grid[2][-1]["color"] = self.game.red
        self.game.grid[3][-1]["color"] = self.game.blue
        self.game.grid[4][-1]["color"] = self.game.blue
        self.game.grid[5][-1]["color"] = self.game.blue
        self.game.grid[6][-1]["color"] = self.game.blue
        self.assertEqual(self.game.four_in_a_row_horizontal(), expected_disks)

    def test_returns_none_when_one_row_has_2_disks_at_the_end_and_another_has_2_disks_at_the_beginning_of_the_same_color(
        self,
    ):
        self.game.grid[5][0]["color"] = self.game.red
        self.game.grid[6][0]["color"] = self.game.red
        self.game.grid[0][1]["color"] = self.game.red
        self.game.grid[1][1]["color"] = self.game.red
        self.assertIs(self.game.four_in_a_row_horizontal(), None)

    def test_returns_expected_disks_when_row_has_5_horizontally_adjacent_disks_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-1],
            self.game.grid[1][-1],
            self.game.grid[2][-1],
            self.game.grid[3][-1],
        ]
        self.game.grid[0][-1]["color"] = self.game.blue
        self.game.grid[1][-1]["color"] = self.game.blue
        self.game.grid[2][-1]["color"] = self.game.blue
        self.game.grid[3][-1]["color"] = self.game.blue
        self.game.grid[4][-1]["color"] = self.game.blue
        self.assertEqual(self.game.four_in_a_row_horizontal(), expected_disks)

    def test_returns_none_when_column_has_4_vertically_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[0][-2]["color"] = self.game.red
        self.game.grid[0][-3]["color"] = self.game.red
        self.game.grid[0][-4]["color"] = self.game.red
        self.assertIs(self.game.four_in_a_row_horizontal(), None)

    def test_returns_none_when_grid_has_4_diagonally_descending_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-4]["color"] = self.game.blue
        self.game.grid[1][-3]["color"] = self.game.blue
        self.game.grid[2][-2]["color"] = self.game.blue
        self.game.grid[3][-1]["color"] = self.game.blue
        self.assertIs(self.game.four_in_a_row_horizontal(), None)

    def test_returns_none_when_grid_has_4_diagonally_ascending_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.blue
        self.game.grid[1][-2]["color"] = self.game.blue
        self.game.grid[2][-3]["color"] = self.game.blue
        self.game.grid[3][-4]["color"] = self.game.blue
        self.assertIs(self.game.four_in_a_row_horizontal(), None)


class TestFourInARowVertical(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()

    def setUp(self):
        self.game.get_grid()

    def test_returns_none_when_grid_is_empty(self):
        self.assertIs(self.game.four_in_a_row_vertical(), None)

    def test_returns_none_when_column_has_3_vertically_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.blue
        self.game.grid[0][-2]["color"] = self.game.blue
        self.game.grid[0][-3]["color"] = self.game.blue
        self.assertIs(self.game.four_in_a_row_vertical(), None)

    def test_returns_none_when_column_has_4_vertically_adjacent_disks_of_different_colors(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[0][-2]["color"] = self.game.blue
        self.game.grid[0][-3]["color"] = self.game.red
        self.game.grid[0][-4]["color"] = self.game.blue
        self.assertIs(self.game.four_in_a_row_vertical(), None)

    def test_returns_expected_disks_when_column_has_4_vertically_adjacent_disks_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-4],
            self.game.grid[0][-3],
            self.game.grid[0][-2],
            self.game.grid[0][-1],
        ]
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[0][-2]["color"] = self.game.red
        self.game.grid[0][-3]["color"] = self.game.red
        self.game.grid[0][-4]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row_vertical(), expected_disks)

    def test_returns_expected_disks_when_column_has_4_vertically_adjacent_disks_of_the_same_color_in_the_last_column(
        self,
    ):
        expected_disks = [
            self.game.grid[6][-4],
            self.game.grid[6][-3],
            self.game.grid[6][-2],
            self.game.grid[6][-1],
        ]
        self.game.grid[6][-1]["color"] = self.game.red
        self.game.grid[6][-2]["color"] = self.game.red
        self.game.grid[6][-3]["color"] = self.game.red
        self.game.grid[6][-4]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row_vertical(), expected_disks)

    def test_returns_expected_disks_when_column_has_4_vertically_adjacent_disks_of_the_same_color_preceded_by_3_disks_of_varying_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-7],
            self.game.grid[0][-6],
            self.game.grid[0][-5],
            self.game.grid[0][-4],
        ]
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[0][-2]["color"] = self.game.blue
        self.game.grid[0][-3]["color"] = self.game.red
        self.game.grid[0][-4]["color"] = self.game.blue
        self.game.grid[0][-5]["color"] = self.game.blue
        self.game.grid[0][-6]["color"] = self.game.blue
        self.game.grid[0][-7]["color"] = self.game.blue
        self.assertEqual(self.game.four_in_a_row_vertical(), expected_disks)

    def test_returns_none_when_one_column_has_2_disks_on_the_bottom_and_another_has_2_disks_on_the_top_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[0][-2]["color"] = self.game.red
        self.game.grid[1][0]["color"] = self.game.red
        self.game.grid[1][1]["color"] = self.game.red
        self.assertIs(self.game.four_in_a_row_vertical(), None)

    def test_returns_expected_disks_when_column_has_5_vertically_adjacent_disks_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-5],
            self.game.grid[0][-4],
            self.game.grid[0][-3],
            self.game.grid[0][-2],
        ]
        self.game.grid[0][-1]["color"] = self.game.blue
        self.game.grid[0][-2]["color"] = self.game.blue
        self.game.grid[0][-3]["color"] = self.game.blue
        self.game.grid[0][-4]["color"] = self.game.blue
        self.game.grid[0][-5]["color"] = self.game.blue
        self.assertEqual(self.game.four_in_a_row_vertical(), expected_disks)

    def test_returns_none_when_row_has_4_horizontally_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[1][-1]["color"] = self.game.red
        self.game.grid[2][-1]["color"] = self.game.red
        self.game.grid[3][-1]["color"] = self.game.red
        self.assertIs(self.game.four_in_a_row_vertical(), None)

    def test_returns_none_when_grid_has_4_diagonally_descending_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-4]["color"] = self.game.blue
        self.game.grid[1][-3]["color"] = self.game.blue
        self.game.grid[2][-2]["color"] = self.game.blue
        self.game.grid[3][-1]["color"] = self.game.blue
        self.assertIs(self.game.four_in_a_row_vertical(), None)

    def test_returns_none_when_grid_has_4_diagonally_ascending_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.blue
        self.game.grid[1][-2]["color"] = self.game.blue
        self.game.grid[2][-3]["color"] = self.game.blue
        self.game.grid[3][-4]["color"] = self.game.blue
        self.assertIs(self.game.four_in_a_row_vertical(), None)


class TestFourInARowDiagonalDescending(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()

    def setUp(self):
        self.game.get_grid()

    def test_returns_none_when_grid_is_empty(self):
        self.assertIsNone(self.game.four_in_a_row_diagonal_descending())

    def test_returns_none_when_grid_has_3_diagonally_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-3]["color"] = self.game.blue
        self.game.grid[1][-2]["color"] = self.game.blue
        self.game.grid[2][-1]["color"] = self.game.blue
        self.assertIsNone(self.game.four_in_a_row_diagonal_descending())

    def test_returns_none_when_grid_has_4_diagonally_adjacent_disks_of_different_colors(
        self,
    ):
        self.game.grid[0][-4]["color"] = self.game.red
        self.game.grid[1][-3]["color"] = self.game.blue
        self.game.grid[2][-2]["color"] = self.game.red
        self.game.grid[3][-1]["color"] = self.game.blue
        self.assertIsNone(self.game.four_in_a_row_diagonal_descending())

    def test_returns_true_expected_disks_grid_has_4_diagonally_adjacent_disks_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-4],
            self.game.grid[1][-3],
            self.game.grid[2][-2],
            self.game.grid[3][-1],
        ]
        self.game.grid[0][-4]["color"] = self.game.red
        self.game.grid[1][-3]["color"] = self.game.red
        self.game.grid[2][-2]["color"] = self.game.red
        self.game.grid[3][-1]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row_diagonal_descending(), expected_disks)

    def test_returns_expected_disks_when_grid_has_4_diagonally_adjacent_disks_of_the_same_color_in_the_last_columns_and_rows(
        self,
    ):
        expected_disks = [
            self.game.grid[3][-4],
            self.game.grid[4][-3],
            self.game.grid[5][-2],
            self.game.grid[6][-1],
        ]
        self.game.grid[3][-4]["color"] = self.game.red
        self.game.grid[4][-3]["color"] = self.game.red
        self.game.grid[5][-2]["color"] = self.game.red
        self.game.grid[6][-1]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row_diagonal_descending(), expected_disks)

    def test_returns_expected_disks_when_grid_has_4_diagonally_adjacent_disks_of_the_same_color_preceded_by_3_disks_of_varying_color(
        self,
    ):
        expected_disks = [
            self.game.grid[3][-4],
            self.game.grid[4][-3],
            self.game.grid[5][-2],
            self.game.grid[6][-1],
        ]
        self.game.grid[0][-7]["color"] = self.game.red
        self.game.grid[1][-6]["color"] = self.game.blue
        self.game.grid[2][-5]["color"] = self.game.red
        self.game.grid[3][-4]["color"] = self.game.blue
        self.game.grid[4][-3]["color"] = self.game.blue
        self.game.grid[5][-2]["color"] = self.game.blue
        self.game.grid[6][-1]["color"] = self.game.blue
        self.assertEqual(self.game.four_in_a_row_diagonal_descending(), expected_disks)

    def test_returns_none_when_the_first_two_columns_have_2_disks_on_the_bottom_and_the_last_two_have_2_disks_on_the_top_of_the_same_color(
        self,
    ):
        self.game.grid[2][-5]["color"] = self.game.red
        self.game.grid[3][-4]["color"] = self.game.red
        self.game.grid[1][-7]["color"] = self.game.red
        self.game.grid[2][-6]["color"] = self.game.red
        self.assertIsNone(self.game.four_in_a_row_diagonal_descending())

    def test_returns_expected_disks_when_grid_has_5_diagonally_adjacent_disks_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-5],
            self.game.grid[1][-4],
            self.game.grid[2][-3],
            self.game.grid[3][-2],
        ]
        self.game.grid[0][-5]["color"] = self.game.blue
        self.game.grid[1][-4]["color"] = self.game.blue
        self.game.grid[2][-3]["color"] = self.game.blue
        self.game.grid[3][-2]["color"] = self.game.blue
        self.game.grid[4][-1]["color"] = self.game.blue
        self.assertEqual(self.game.four_in_a_row_diagonal_descending(), expected_disks)

    def test_returns_none_when_row_has_4_horizontally_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[1][-1]["color"] = self.game.red
        self.game.grid[2][-1]["color"] = self.game.red
        self.game.grid[3][-1]["color"] = self.game.red
        self.assertIsNone(self.game.four_in_a_row_diagonal_descending())

    def test_returns_none_when_column_has_4_vertically_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[0][-2]["color"] = self.game.red
        self.game.grid[0][-3]["color"] = self.game.red
        self.game.grid[0][-4]["color"] = self.game.red
        self.assertIsNone(self.game.four_in_a_row_diagonal_descending())

    def test_returns_none_when_grid_has_4_diagonally_ascending_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.blue
        self.game.grid[1][-2]["color"] = self.game.blue
        self.game.grid[2][-3]["color"] = self.game.blue
        self.game.grid[3][-4]["color"] = self.game.blue
        self.assertIsNone(self.game.four_in_a_row_diagonal_descending())


class TestFourInARowDiagonalAscending(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()

    def setUp(self):
        self.game.get_grid()

    def test_returns_none_when_grid_is_empty(self):
        self.assertIs(self.game.four_in_a_row_diagonal_ascending(), None)

    def test_returns_none_when_grid_has_3_diagonally_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.blue
        self.game.grid[1][-2]["color"] = self.game.blue
        self.game.grid[2][-3]["color"] = self.game.blue
        self.assertIs(self.game.four_in_a_row_diagonal_ascending(), None)

    def test_returns_none_when_grid_has_4_diagonally_adjacent_disks_of_different_colors(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[1][-2]["color"] = self.game.blue
        self.game.grid[2][-3]["color"] = self.game.red
        self.game.grid[3][-4]["color"] = self.game.blue
        self.assertIs(self.game.four_in_a_row_diagonal_ascending(), None)

    def test_returns_expected_disks_when_grid_has_4_diagonally_adjacent_disks_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-1],
            self.game.grid[1][-2],
            self.game.grid[2][-3],
            self.game.grid[3][-4],
        ]
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[1][-2]["color"] = self.game.red
        self.game.grid[2][-3]["color"] = self.game.red
        self.game.grid[3][-4]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row_diagonal_ascending(), expected_disks)

    def test_returns_expected_disks_when_grid_has_4_diagonally_adjacent_disks_of_the_same_color_in_the_last_columns_and_rows(
        self,
    ):
        expected_disks = [
            self.game.grid[3][-1],
            self.game.grid[4][-2],
            self.game.grid[5][-3],
            self.game.grid[6][-4],
        ]
        self.game.grid[3][-1]["color"] = self.game.red
        self.game.grid[4][-2]["color"] = self.game.red
        self.game.grid[5][-3]["color"] = self.game.red
        self.game.grid[6][-4]["color"] = self.game.red
        self.assertEqual(self.game.four_in_a_row_diagonal_ascending(), expected_disks)

    def test_returns_expected_disks_when_grid_has_4_diagonally_adjacent_disks_of_the_same_color_preceded_by_3_disks_of_varying_color(
        self,
    ):
        expected_disks = [
            self.game.grid[3][-4],
            self.game.grid[4][-5],
            self.game.grid[5][-6],
            self.game.grid[6][-7],
        ]
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[1][-2]["color"] = self.game.blue
        self.game.grid[2][-3]["color"] = self.game.red
        self.game.grid[3][-4]["color"] = self.game.blue
        self.game.grid[4][-5]["color"] = self.game.blue
        self.game.grid[5][-6]["color"] = self.game.blue
        self.game.grid[6][-7]["color"] = self.game.blue
        self.assertTrue(self.game.four_in_a_row_diagonal_ascending())

    def test_returns_none_when_the_first_two_columns_have_2_disks_on_the_top_and_the_last_two_have_2_disks_on_the_bottom_of_the_same_color(
        self,
    ):
        self.game.grid[2][-6]["color"] = self.game.red
        self.game.grid[3][-7]["color"] = self.game.red
        self.game.grid[1][-4]["color"] = self.game.red
        self.game.grid[2][-5]["color"] = self.game.red
        self.assertIs(self.game.four_in_a_row_diagonal_ascending(), None)

    def test_returns_expected_disks_when_grid_has_5_diagonally_adjacent_disks_of_the_same_color(
        self,
    ):
        expected_disks = [
            self.game.grid[0][-1],
            self.game.grid[1][-2],
            self.game.grid[2][-3],
            self.game.grid[3][-4],
        ]
        self.game.grid[0][-1]["color"] = self.game.blue
        self.game.grid[1][-2]["color"] = self.game.blue
        self.game.grid[2][-3]["color"] = self.game.blue
        self.game.grid[3][-4]["color"] = self.game.blue
        self.game.grid[4][-5]["color"] = self.game.blue
        self.assertTrue(self.game.four_in_a_row_diagonal_ascending())

    def test_returns_none_when_row_has_4_horizontally_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[1][-1]["color"] = self.game.red
        self.game.grid[2][-1]["color"] = self.game.red
        self.game.grid[3][-1]["color"] = self.game.red
        self.assertIs(self.game.four_in_a_row_diagonal_ascending(), None)

    def test_returns_none_when_column_has_4_vertically_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-1]["color"] = self.game.red
        self.game.grid[0][-2]["color"] = self.game.red
        self.game.grid[0][-3]["color"] = self.game.red
        self.game.grid[0][-4]["color"] = self.game.red
        self.assertIs(self.game.four_in_a_row_diagonal_ascending(), None)

    def test_returns_none_when_grid_has_4_diagonally_descending_adjacent_disks_of_the_same_color(
        self,
    ):
        self.game.grid[0][-4]["color"] = self.game.blue
        self.game.grid[1][-3]["color"] = self.game.blue
        self.game.grid[2][-2]["color"] = self.game.blue
        self.game.grid[3][-1]["color"] = self.game.blue
        self.assertIs(self.game.four_in_a_row_diagonal_ascending(), None)


class TestColorDisksGreen(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()
        cls.game.get_grid()

    def test_disks_become_green(self):
        disks = [
            self.game.grid[0][1],
            self.game.grid[0][2],
            self.game.grid[0][3],
            self.game.grid[0][4],
        ]
        self.game.grid[0][1]["color"] = self.game.red
        self.game.grid[0][2]["color"] = self.game.blue
        self.game.color_disks_green(disks)
        for disk in disks:
            self.assertEqual(disk["color"], self.game.green)


class TestIncrementScore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()

    def setUp(self):
        self.game.red_score = 0
        self.game.blue_score = 0

    def test_red_score_is_incremented(self):
        self.game.current_players_disk_color = self.game.red
        self.game.increment_score()
        self.assertEqual(self.game.red_score, 1)

    def test_blue_score_is_incremented(self):
        self.game.current_players_disk_color = self.game.blue
        self.game.increment_score()
        self.assertEqual(self.game.blue_score, 1)

    def test_red_score_is_not_incremented(self):
        self.game.current_players_disk_color = self.game.blue
        self.game.increment_score()
        self.assertEqual(self.game.red_score, 0)

    def test_blue_score_is_not_incremented(self):
        self.game.current_players_disk_color = self.game.red
        self.game.increment_score()
        self.assertEqual(self.game.blue_score, 0)


class TestSwapCurrentPlayersDiskColor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()

    def test_disk_color_becomes_blue(self):
        self.game.current_players_disk_color = self.game.red
        self.game.swap_current_players_disk_color()
        self.assertEqual(self.game.current_players_disk_color, self.game.blue)

    def test_disk_color_becomes_red(self):
        self.game.current_players_disk_color = self.game.blue
        self.game.swap_current_players_disk_color()
        self.assertEqual(self.game.current_players_disk_color, self.game.red)
