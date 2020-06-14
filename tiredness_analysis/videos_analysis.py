import logging
from collections import deque, namedtuple
from typing import Tuple, Iterable, Deque

from teyered.data_processing.blinks.blinks_detection import detect_blinks

from tiredness_analysis.videos_processor import ProcessedVideos

logger = logging.getLogger(__name__)


SECONDS_PER_MIN = 60
PERCLOS_CLOSEDNESS_THRESHOLD = 0.8


AnalyzedData = namedtuple('AnalyzedData',
                          ['left_eye_closedness', 'right_eye_closedness',
                           'left_perclos', 'right_perclos',
                           'left_blink_lengths', 'right_blink_lengths',
                           'left_time_between_blinks', 'right_time_between_blinks',
                           'pose_reprojection_err'])


def analyze_data(data: ProcessedVideos) -> AnalyzedData:
    """Analyzes processed videos data and returns results of the analysis."""
    logger.info('Removing frames with undetermined closedness.')
    left_closedness = deque(zip(data.timespans, data.left_eye_closedness))
    left_closedness = _remove_undetermined_closedness(left_closedness)

    right_closedness = deque(zip(data.timespans, data.right_eye_closedness))
    right_closedness = _remove_undetermined_closedness(right_closedness)
    logger.info('Removed.')

    logger.info('Starting PERCLOS calculation...')
    left_perclos = _calc_perclos(left_closedness)
    right_perclos = _calc_perclos(right_closedness)
    logger.info('PERCLOS values have been calculated')

    logger.info('Starting blinks calculation...')
    left_between, left_lengths = _calc_blinks_data(left_closedness)
    right_between, right_lengths = _calc_blinks_data(right_closedness)
    logger.info('Blinks calculation has finished')

    return AnalyzedData(left_eye_closedness=left_closedness,
                        right_eye_closedness=right_closedness,
                        left_perclos=left_perclos,
                        right_perclos=right_perclos,
                        left_time_between_blinks=left_between,
                        right_time_between_blinks=right_between,
                        left_blink_lengths=left_lengths,
                        right_blink_lengths=right_lengths,
                        pose_reprojection_err=deque(zip(data.timespans,
                                                    data.pose_reprojection_err)))


def _remove_undetermined_closedness(eye_closedness: Iterable[Tuple[float, float]]
                                    ) -> Deque[Tuple[float, float]]:
    """Filter out all frames for which closedness couldn't be determined."""
    return deque((t, c) for (t, c) in eye_closedness if c >= 0.)


def _calc_perclos(eye_closedness: Iterable[Tuple[float, float]]
                  ) -> Deque[Tuple[float, float]]:
    """Calculates PERCLOS signal (1 if below the threshold, 0 otherwise)"""
    return deque((t, float(c < PERCLOS_CLOSEDNESS_THRESHOLD)) for t, c in eye_closedness)


def _calc_blinks_data(eye_closedness: Iterable[Tuple[float, float]]
                      ) -> Tuple[Deque[Tuple[float, float]],
                                 Deque[Tuple[float, float]]]:
    """Calculates different blink metrics.

    Produces:
        1. `time_between_blinks` - time duration of gaps between each blink.
        2. `blink_lengths` - time duration of each blink.
    """
    blinks = detect_blinks(eye_closedness)

    time_between_blinks = deque()
    blink_lengths = deque([(blinks[0].get_time_range()[0], blinks[0].get_duration())])
    for i in range(1, len(blinks)):
        prev_blink_end = blinks[i - 1].get_time_range()[1]
        curr_blink_start = blinks[i].get_time_range()[0]

        time_between_blinks.append((prev_blink_end, curr_blink_start - prev_blink_end))
        blink_lengths.append((curr_blink_start, blinks[i].get_duration()))

    return time_between_blinks, blink_lengths
