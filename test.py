import unittest
from darts import logic
from darts.dart import Dart


class DartClassTest(unittest.TestCase):

    def helper(self, dart, score, string):
        self.assertEqual(dart.score(), score)
        self.assertEqual(str(dart), string)

    def test_bull(self):
        self.helper(Dart(50, 1), 50, 'BULL')

    def test_t20(self):
        self.helper(Dart(20, 3), 60, 'T20')

    def test_d20(self):
        self.helper(Dart(20, 2), 40, 'D20')

    def test_20(self):
        self.helper(Dart(20, 1), 20, '20')

    def test_out(self):
        self.helper(Dart(0, 1), 0, 'OUT')


class DartFromString(unittest.TestCase):
    def test_bull(self):
        self.assertEqual(Dart('BULL').score(), 50)

    def test_triple(self):
        self.assertEqual(Dart('T20').score(), 60)

    def test_double(self):
        self.assertEqual(Dart('D20').score(), 40)


class DartFromPolarTest(unittest.TestCase):
    def helper(self, distance, angle, expected_score):
        dart = logic.dart_from_polar(distance, angle)
        self.assertEqual(dart.score(), expected_score)

    def test_bull1(self):
        self.helper(distance=0, angle=0, expected_score=50)

    def test_bull2(self):
        self.helper(distance=logic.BOARD_SIZE * logic.BULL - 0.01, angle=0, expected_score=50)

    def test_6(self):
        self.helper(distance=0.45 * logic.BOARD_SIZE, angle=0, expected_score=6)
        self.helper(distance=0.45 * logic.BOARD_SIZE, angle=8.99, expected_score=6)

    def test_20(self):
        self.helper(distance=0.45 * logic.BOARD_SIZE, angle=90, expected_score=20)
        self.helper(distance=0.45 * logic.BOARD_SIZE, angle=81, expected_score=20)

    def test_11(self):
        self.helper(distance=0.45 * logic.BOARD_SIZE, angle=180, expected_score=11)
        self.helper(distance=0.45 * logic.BOARD_SIZE, angle=171, expected_score=11)

    def test_10(self):
        self.helper(distance=0.45 * logic.BOARD_SIZE, angle=333, expected_score=10)
        self.helper(distance=0.45 * logic.BOARD_SIZE, angle=350.99, expected_score=10)

    def test_triple(self):
        self.helper(distance=logic.TRIPLE_RING[0] * logic.BOARD_SIZE + .001, angle=90, expected_score=60)
        self.helper(distance=logic.TRIPLE_RING[1] * logic.BOARD_SIZE - .001, angle=90, expected_score=60)

    def test_double(self):
        self.helper(distance=logic.DOUBLE_RING[0] * logic.BOARD_SIZE + .001, angle=90, expected_score=40)
        self.helper(distance=logic.DOUBLE_RING[1] * logic.BOARD_SIZE - .001, angle=90, expected_score=40)


if __name__ == '__main__':
    unittest.main()