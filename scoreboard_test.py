from scripts.scoreboard import ScoreBoard
import unittest

class TestScoreBoardFunctions(unittest.TestCase):
    def test_scoreboard_singleton_creation(self):
        a = ScoreBoard('mockscore.json')
        b = ScoreBoard('mockscore.json')
        self.assertIs(a, b)
    def test_scoreboard_sorting(self):
        mock_score = ScoreBoard('mockscore.json')
        mock_score.sort()
        self.assertEqual(mock_score.print())
if __name__ == '__main__':
    unittest.main(verbosity = 2)