import unittest
from dragon_vs_robots import DragonVsRobots
from models.data.scoreboard import Scoreboard

class TestScoreboard(unittest.TestCase):
    def setUp(self):
        game = DragonVsRobots()
        self.scoreboard = Scoreboard(game)
        self.scoreboard.stats.score = 10

    def test_reset_score(self):
        # Act
        self.scoreboard.reset_score()

        # Assert
        self.assertEqual(self.scoreboard.stats.score, 0)

    def test_update_score_with_positive_adjustment(self):
        # Act
        self.scoreboard.update_score(1)

        # Assert
        self.assertEqual(self.scoreboard.stats.score, 11)

    def test_update_score_with_negative_adjustment(self):
        # Act
        self.scoreboard.update_score(-1)

        # Assert
        self.assertEqual(self.scoreboard.stats.score, 9)

if __name__ == '__main__':
    unittest.main()
