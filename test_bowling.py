# -*- coding: utf-8 -*-


import unittest

import bowling
from bowling import InternalGameResult, InternationalGameResult


class BowlingTest(unittest.TestCase):

    def test_internal_strikes(self):
        game = InternalGameResult('XXXXXXXXXX')
        game_result = game.get_score()
        self.assertEqual(game_result, 200)

    def test_international_strikes(self):
        game = InternationalGameResult('XXXXXXXXXX')
        game_result = game.get_score()
        self.assertEqual(game_result, 270)

    def test_internal_spares(self):
        game = InternalGameResult('1/1/1/1/1/1/1/1/1/1/')
        game_result = game.get_score()
        self.assertEqual(game_result, 150)

    def test_international_spares(self):
        game = InternationalGameResult('1/1/1/1/1/1/1/1/1/1/')
        game_result = game.get_score()
        self.assertEqual(game_result, 109)

    def test_internal_zero_points(self):
        game = InternalGameResult('--------------------')
        game_result = game.get_score()
        self.assertEqual(game_result, 0)

    def test_international_zero_points(self):
        game = InternationalGameResult('--------------------')
        game_result = game.get_score()
        self.assertEqual(game_result, 0)

    def test_internal_all_elements(self):
        game = InternalGameResult('X-123456/72819-XX')
        game_result = game.get_score()
        self.assertEqual(game_result, 117)

    def test_international_all_elements(self):
        game = InternationalGameResult('X-123456/72819-XX')
        game_result = game.get_score()
        self.assertEqual(game_result, 100)

    def test_internal_incorrect_data_error(self):
        with self.assertRaises(bowling.IncorrectDataError):
            game = InternalGameResult('X-123456/72810-XX')
            game.get_score()

    def test_international_incorrect_data_error(self):
        with self.assertRaises(bowling.IncorrectDataError):
            game = InternationalGameResult('X-123456/72810-XX')
            game.get_score()

    def test_internal_frame_quantity_error(self):
        with self.assertRaises(bowling.FrameQuantityError):
            game = InternalGameResult('111111111111111111111')
            game.get_score()

    def test_international_frame_quantity_error(self):
        with self.assertRaises(bowling.FrameQuantityError):
            game = InternationalGameResult('111111111111111111111')
            game.get_score()

    def test_internal_game_over_error(self):
        with self.assertRaises(bowling.GameOverError):
            game = InternalGameResult('1111')
            game.get_score()

    def test_international_game_over_error(self):
        with self.assertRaises(bowling.GameOverError):
            game = InternationalGameResult('1111')
            game.get_score()

    def test_internal_skittle_quantity_error(self):
        with self.assertRaises(bowling.SkittleQuantityError):
            game = InternalGameResult('391/1/1/1/1/1/1/1/1/')
            game.get_score()

    def test_international_skittle_quantity_error(self):
        with self.assertRaises(bowling.SkittleQuantityError):
            game = InternationalGameResult('391/1/1/1/1/1/1/1/1/')
            game.get_score()

    def test_internal_spare_error(self):
        with self.assertRaises(bowling.SpareError):
            game = InternalGameResult('/1/1/1/1/1/1/1/1/1/1')
            game.get_score()

    def test_international_spare_error(self):
        with self.assertRaises(bowling.SpareError):
            game = InternationalGameResult('/1/1/1/1/1/1/1/1/1/1')
            game.get_score()


if __name__ == '__main__':
    unittest.main()
