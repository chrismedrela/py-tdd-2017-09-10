import unittest

from bowling_game import BowlingGame


class BowlingGameTests(unittest.TestCase):
    def setUp(self):
        self.game = BowlingGame()

    def roll_many(self, pins, rolls):
        for i in range(rolls):
            self.game.roll(pins)

    def test_when_all_throws_one_then_score_should_be_twenty(self):
        self.roll_many(pins=1, rolls=20)
        self.assertEqual(self.game.score(), 20)

    def test_when_all_throws_in_gutter_then_score_should_be_zero(self):
        self.roll_many(pins=0, rolls=20)
        self.assertEqual(self.game.score(), 0)

    def test_when_one_spare_then_next_roll_is_counted_twice(self):
        self.roll_many(pins=5, rolls=2)
        self.game.roll(4)
        self.roll_many(pins=0, rolls=17)
        self.assertEqual(self.game.score(), 18)

    def test_when_spare_in_last_frame_then_third_roll_is_counted_once(self):
        self.roll_many(pins=0, rolls=18)
        self.roll_many(pins=5, rolls=3)
        self.assertEqual(self.game.score(), 15)

    def test_when_strike_then_next_two_rolls_are_counted_twice(self):
        self.game.roll(10)
        self.roll_many(pins=4, rolls=18)
        bonus = 2*4
        self.assertEqual(self.game.score(), 10 + 18*4 + bonus)

    def test_when_perfect_game_then_score_should_be_300(self):
        self.roll_many(pins=10, rolls=12)
        self.assertEqual(self.game.score(), 300)



if __name__ == '__main__':
    unittest.main()