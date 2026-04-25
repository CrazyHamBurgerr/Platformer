from scripts.scoreboard import ScoreBoard
import unittest
import time

class TestScoreBoardFunctions(unittest.TestCase):
    def setUp(self):
        self.mock_score = ScoreBoard('mockscore.json')

    def test_scoreboard_singleton_creation(self):
        a = ScoreBoard('mockscore.json')
        b = ScoreBoard('mockscore.json')
        self.assertIs(a, b)
        del a, b

    def test_valid_entry(self):
        self.assertTrue(self.mock_score.check_valid_position(5))

    def test_invalid_entry(self):
        self.assertFalse(self.mock_score.check_valid_position(2103))
        self.assertFalse(self.mock_score.check_valid_position(None))
        self.assertFalse(self.mock_score.check_valid_position("3413"))
    
    def test_new_entry_creation(self):
        self.assertTrue(self.mock_score.new_entry(3500, int(time.time())))
        self.assertEqual(self.mock_score.delete_entry(3), "entry 3 deleted")
    
    def test_new_entry_creation_position(self):
        self.assertTrue(self.mock_score.new_entry(3500, int(time.time())))
        self.assertTrue(self.mock_score.new_entry(3500, int(time.time())))
    
    def test_invalid_new_entry_score(self):
        self.assertEqual(self.mock_score.new_entry(123045, int(time.time())), "invalid score")
        self.assertEqual(self.mock_score.new_entry(-699, int(time.time())), "invalid score")
    
    def test_invalid_new_entry_score_type(self):
        self.assertEqual(self.mock_score.new_entry("gabagool", int(time.time())), "invalid score type")
        self.assertEqual(self.mock_score.new_entry(None, int(time.time())), "invalid score type")

    def test_invalid_new_entry_timestamp(self):
        self.assertEqual(self.mock_score.new_entry(4000, None), "bad timestamp")
        self.assertEqual(self.mock_score.new_entry(3000, -213), "bad timestamp") 

    def test_entry_deletion(self):
        self.assertEqual(self.mock_score.delete_entry(5), "entry 5 deleted")

    def test_scoreboard_entry(self):
        entry_7 = self.mock_score.return_entry(7)
        self.assertDictEqual({'score': 5800, 'timestamp': 1776978398}, entry_7)

    def test_scoreboard_sorting(self):
        entry_7 = self.mock_score.return_entry(7)
        entry_5 = self.mock_score.return_entry(5)
        self.assertDictEqual({'score': 5800, 'timestamp': 1776978398}, entry_7)
        self.assertDictEqual({'score': 2675, 'timestamp': 1777016735}, entry_5)
        del entry_7, entry_5
        # after sorting these entries should be first and second based on highest score

        self.mock_score.sort() 
        entry_1 = self.mock_score.return_entry(1)
        entry_2 = self.mock_score.return_entry(2)
        self.assertDictEqual({'score': 5800, 'timestamp': 1776978398}, entry_1)
        self.assertDictEqual({'score': 2675, 'timestamp': 1777016735}, entry_2)
        del entry_1, entry_2

if __name__ == '__main__':
    unittest.main(verbosity = 2)