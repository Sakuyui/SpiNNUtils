from spinn_utilities.lazy.range_dictionary import RangeDictionary

defaults = {"a": "alpha", "b": "bravo"}

rd = RangeDictionary(10, defaults)


def test_full():
    assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == rd.ids()


def test_single():
    view = rd[2]
    assert [2] == view.ids()


def test_simple_slice():
    view = rd[2:6]
    assert [2, 3, 4, 5] == view.ids()


def test_extended_slice():
    view = rd[2:8:2]
    assert [2, 4, 6] == view.ids()


def test_tuple():
    view = rd[2, 4, 7]
    assert [2, 4, 7] == view.ids()


def test_unsorted_tuple():
    view = rd[2, 7, 3]
    assert [2, 3, 7] == view.ids()


def test_list():
    l = [2, 7, 3]
    view = rd[l]
    assert [2, 3, 7] == view.ids()


def test_double_slice():
    view1 = rd[2:7]
    assert [2, 3, 4, 5, 6] == view1.ids()
    view2 = view1[2:4]
    assert [4, 5] == view2.ids()


def test_double_list():
    l = [2, 7, 1, 3, 5, 8]
    view1 = rd[l]
    assert [1, 2, 3, 5, 7, 8] == view1.ids()
    view2 = view1[2, 3, 5]
    assert [3, 5, 8] == view2.ids()
