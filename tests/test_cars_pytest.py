import pytest
from Nochovca import TRACK, TRACK_BORDER, FINISH_POSITION, RED_CAR, GameBar, Car

def test_overlay():
    assert TRACK.get_height() == TRACK_BORDER.get_height()

def test_finish():
    assert FINISH_POSITION[0] == 138 and FINISH_POSITION[1] == 240

def test_car_width():
    assert RED_CAR.get_width() < (TRACK.get_width() * 0.1)

def test_car_height():
    assert RED_CAR.get_height() < (TRACK.get_height() / 5)

# def test_car_min_height():
#     assert RED_CAR.get_height() >= 15
#
# def test_car_min_width():
#     assert RED_CAR.get_width() >= 4

def test_game_time():
    time = GameBar.TIME
    assert min(time) >= 950

def test_car_speed():
    speed = GameBar.SPEED
    assert max(speed) <= 15

def test_car_rotation():
    rotation = GameBar.ROTATION
    assert max(rotation) <= 12

def test_initialization_car_height():
    assert Car.START_POS[0] - (RED_CAR.get_height() / 2) > FINISH_POSITION[0]


def _func(a, b):
    return a >= b

@pytest.fixture()
def func():
    return _func

@pytest.mark.parametrize('property_car, test, result', [
    (RED_CAR.get_height(), 15, True),
    (RED_CAR.get_width(), 4, True)
])

def test_car_properties(property_car, test, result, func):
    assert func(property_car, test) == result
# if __name__ == '__main__':
#     pytest.main()
