import pytest
from Nochovca import TRACK, TRACK_BORDER, FINISH_POSITION, RED_CAR

def test_pytest():
    assert (3 + 4) == 7

def test_overlay():
    assert TRACK.get_height() == TRACK_BORDER.get_height()

def test_finish():
    assert FINISH_POSITION[0] == 138 and FINISH_POSITION[1] == 240

def test_car_width():
    assert RED_CAR.get_width() < (TRACK.get_width() * 0.1)

def test_car_height():
    assert RED_CAR.get_height() < (TRACK.get_height() / 5)



if __name__ == '__main__':
    pytest.main()
