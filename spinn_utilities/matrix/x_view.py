class XView(object):

    def __init__(self, x, matrix):
        self._x = x
        self._matrix = matrix

    def __getitem__(self, key):
        return self._matrix.get_data(x=self._x, y=key)

    def __setitem__(self, key, value):
        self._matrix.set_data(x=self._x, y=key, value=value)
