import logging
from collections import deque, namedtuple

from teyered.data_processing.blinks.blinks_detection import detect_blinks


logger = logging.getLogger(__name__)


SECONDS_IN_MIN = 60
PERCLOS_CLOSEDNESS_THRESHOLD = 0.8


AnalyzedData = namedtuple('AnalyzedData',
                          ['left_eye_closedness', 'right_eye_closedness',
                           'left_perclos', 'right_perclos',
                           'left_blink_lengths', 'right_blink_lengths',
                           'left_time_between_blinks', 'right_time_between_blinks',
                           'left_blink_rate', 'right_blink_rate',
                           'pose_reprojection_err'])


def analyze_data(data):
    """Analyzes processed videos data and returns results of the analysis."""
    logger.info('Removing frames with undetermined closedness.')
    left_closedness = zip(data.timespans, data.left_eye_closedness)
    left_closedness = _remove_undetermined_closedness(left_closedness)

    right_closedness = zip(data.timespans, data.right_eye_closedness)
    right_closedness = _remove_undetermined_closedness(right_closedness)
    logger.info('Removed.')

    logger.info('Starting PERCLOS calculation...')
    left_perclos = _calc_perclos(left_closedness)
    right_perclos = _calc_perclos(right_closedness)
    logger.info('PERCLOS values have been calculated')

    logger.info('Starting blinks calculation...')
    left_between, left_lengths, left_rate = _calc_blinks_data(left_closedness)
    right_between, right_lengths, right_rate = _calc_blinks_data(right_closedness)
    logger.info('Blinks calculation has finished')

    return AnalyzedData(left_eye_closedness=left_closedness,
                        right_eye_closedness=right_closedness,
                        left_perclos=left_perclos,
                        right_perclos=right_perclos,
                        left_time_between_blinks=left_between,
                        right_time_between_blinks=right_between,
                        left_blink_lengths=left_lengths,
                        right_blink_lengths=right_lengths,
                        left_blink_rate=left_rate,
                        right_blink_rate=right_rate,
                        pose_reprojection_err=zip(data.timespans,
                                                  data.pose_reprojection_err))


def _remove_undetermined_closedness(eye_closedness):
    """Filter out all frames for which closedness couldn't be determined."""
    return [(t, c) for (t, c) in eye_closedness if c >= 0.]


def _calc_perclos(eye_closedness):
    perclos = deque()
    time_window = deque()
    height_window = deque()
    for curr_time, curr_closedness in eye_closedness:
        time_window.append(curr_time)
        height_window.append(curr_closedness)
        # Get rid of all frames outside the 1min window
        while time_window[0] < curr_time - SECONDS_IN_MIN:
            time_window.popleft()
            height_window.popleft()

        total_frames_count = len(height_window)
        closed_frames_count = len([h for h in height_window
                                   if h < PERCLOS_CLOSEDNESS_THRESHOLD])
        perclos.append((curr_time, closed_frames_count / total_frames_count))

    return perclos


def _calc_blinks_data(eye_closedness):
    blinks = detect_blinks(eye_closedness)

    time_between_blinks = deque()
    blink_lengths = deque([(blinks[0].get_time_range()[0], blinks[0].get_duration())])
    for i in range(1, len(blinks)):
        prev_blink_end = blinks[i - 1].get_time_range()[1]
        curr_blink_start = blinks[i].get_time_range()[0]

        time_between_blinks.append((prev_blink_end, curr_blink_start - prev_blink_end))
        blink_lengths.append((curr_blink_start, blinks[i].get_duration()))

    blinks_window = deque()
    blink_rates = deque()
    for curr_blink in blinks:
        blinks_window.append(curr_blink)
        window_end = curr_blink.get_time_range()[1]
        window_start = window_end - SECONDS_IN_MIN
        # Get rid of all blinks that are fully outside 1min window
        while blinks_window[0].get_time_range()[1] < window_start:
            blinks_window.popleft()

        # If blink starts outside of the window but ends inside
        # include proportion of the blink that is within the window
        partial_blink_proportion = 1
        if blinks_window[0].get_time_range()[0] < window_start:
            duration_inside_window = (blinks_window[0].get_time_range()[1] - window_start)
            partial_blink_proportion = (duration_inside_window
                                        / blinks_window[0].get_duration())

        rate = len(blinks_window) - 1 + partial_blink_proportion
        blink_rates.append((window_end, rate))

    return time_between_blinks, blink_lengths, blink_rates
