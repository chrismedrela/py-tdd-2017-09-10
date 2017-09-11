import unittest

from bowling_game import BowlingGame


class BowlingGameTests(unittest.TestCase):
    def test_when_all_throws_one_then_score_should_be_twenty(self):
        game = BowlingGame()
        for i in range(20):
            game.roll(1)
        self.assertEqual(game.score(), 20)

    def test_when_all_throws_in_gutter_then_score_should_be_zero(self):
        game = BowlingGame()
        for i in range(20):
            game.roll(0)
        self.assertEqual(game.score(), 0)


if __name__ == '__main__':
    unittest.main()