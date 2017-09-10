from contextlib import redirect_stdout
import io
import unittest


class Shape:
    def __init__(self, shape):
        assert shape in ('circle', 'dot')
        self.shape = shape

    def draw(self):
        if self.shape == 'circle':
            print('o')
        elif self.shape == 'dot':
            print('.')


class ShapeTests(unittest.TestCase):
    def test_circle(self):
        self._test(shape=Shape('circle'),
                   expected_output='o')

    def test_dot(self):
        self._test(shape=Shape('dot'),
                   expected_output='.')

    def _test(self, shape, expected_output):
        f = io.StringIO()
        with redirect_stdout(f):
            shape.draw()
        output = f.getvalue()
        self.assertEqual(output, expected_output+'\n')


if __name__ == "__main__":
    unittest.main()
