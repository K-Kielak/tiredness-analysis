###### Blink frequency
###### Amplitude
###### Lid movement speed (closure and opening)
###### average opening level
###### Eye closed duration
###### maximum close duration
###### PERCLOS
# Blink duration 50_50
# Duration at 80%
# Eye gaze
import numpy as np


def calculate_blink_frequency(blinks, time_length):
    """

    :param blinks: List of blink objects to analyze, should be ordered by time.
    :param time_length: int (seconds) in which the blinks were detected.
    :return:
    """

    blink_frequency = blinks.shape[0] / time_length

    return blink_frequency


def calculate_max_height(eye_heights):
    """

    :param eye_heights: List of eye heights
    :return: float of max value of eye heights
    """
    max_height = np.max(eye_heights)
    return max_height


def calculate_lid_movement_speed(eye_heights, blinks, time_length):
    """
    Calculate difference in timestamps between minimum point and time at end
    of blink (closure speed) and beginning of blink and time at minimum
    point (opening speed)

    Calculate average
    """


def calculate_avg_opening_level():
    """
    Select non_blinks and calculate average eye_height
    """


def calculate_closure_duration():
    """
    Select timestamps duration of eye_heights where blink == True below a
    further standard deviation

    (or select points from minimum height of blink and use low SD values to
    consider eye as closed)

    Also must return max closed duration
    """

def calculate_perclos():

    """

    Blinks have to be removed for perclos to be calculated accurately. An
    average of both eyes can be taken.

    PERCLOS = duration_eye_closed / time_range

    For a specific time range, count how many seconds within this time range
    were below a threshold (closed). Then divide by time range

    There are variations, ie. PERCLOS80 --> where threshold for "eye_closed"
    is 80% as well as PERCLOS70.

    time_range window is usually 20, 30 or 60 s

    More info: https://ieeexplore.ieee.org/document/5625097
    """