import os
import logging
from collections import defaultdict

import matplotlib.pyplot as plt
from teyered.data_processing.blinks_detection import detect_blinks
from teyered.data_processing.eye_area_calculation import \
    calculate_polygon_area, normalize_eye_points
from teyered.data_processing.points_extractor import FacialPointsExtractor
from teyered.io.files import VideoGenerator

from tiredness_analysis.config import ANALYSIS_OUTPUT_DIR, FRAMES_TO_SKIP, \
     LOGGING_LEVEL, RENDER_FIGS, SAVE_FIGS, VIDS_TO_ANALYZE


logger = logging.getLogger(__name__)


def main():
    os.mkdir(ANALYSIS_OUTPUT_DIR)
    left_eye_data = defaultdict(list)
    right_eye_data = defaultdict(list)
    for vid in VIDS_TO_ANALYZE:
        logger.info(f'Analyzing video {vid}...')
        left, right = _analyze_video(vid, FRAMES_TO_SKIP)
        for key, value in left.items():
            left_eye_data[key] += value

        for key, value in right.items():
            right_eye_data[key] += value

        logger.info(f'Analyzing video {vid} finished')

    logger.info('Plotting left eye data...')
    _plot_data(left_eye_data, 'left')

    logger.info('Plotting right eye data...')
    _plot_data(right_eye_data, 'right')


def _analyze_video(filepath, frames_to_skip):
    pts_extractor = FacialPointsExtractor()

    left_eye_points = []
    right_eye_points = []
    with VideoGenerator(filepath, frames_to_skip) as video:
        logger.info('Extracting facial points...')
        while not video.is_over():
            timespan, frame = video.get_next_frame()
            facial_points = pts_extractor.extract_facial_points(frame)
            left_eye = facial_points['left_eye']
            if left_eye:
                left_eye_points.append((timespan, left_eye))

            right_eye = facial_points['right_eye']
            if right_eye:
                right_eye_points.append((timespan, right_eye))

    logger.info(f'Analyzing left eye... '
                f'(frames to analyze: {len(left_eye_points)}')
    left_eye_data = _analyze_eye(left_eye_points)

    logger.info(f'Analyzing right eye...'
                f'(frames to analyze: {len(right_eye_points)}')
    right_eye_data = _analyze_eye(right_eye_points)
    return left_eye_data, right_eye_data


def _analyze_eye(eye_points):
    """
    :param eye_points: (timespan, [eye_points]) tuple indicating detailed
        position of the eye at a given time.
    :return: string -> dataset tuple. Each dataset is 2-column
        (start_time, value) numpy array. Dictionary consists of
        eye areas, blink lengths, and time between blinks measurements.
    """
    measurements = []
    for t, points in eye_points:
        norm = normalize_eye_points(points)
        measurements.append((t, calculate_polygon_area(norm)))

    logger.info('Detecting blinks...')
    blinks = detect_blinks(measurements)
    lengths, times_between = _analyze_blinks(blinks)
    eye_data = {
        'eye_size [px^2]': measurements,
        'blink_lengths [s]': lengths,
        'times_between_blinks [s]': times_between
    }

    return eye_data


def _analyze_blinks(blinks):
    """
    :param blinks: List of blink objects to analyze, should be ordered by time.
    :return: Lengths, and times between blinks. Each as a 2-column
        (start_time, value) numpy array.
    """
    lengths = [(blinks[0].get_time_range()[0], blinks[0].get_duration())]
    times_between = []
    for i in range(1, len(blinks)):
        prev_blink_end = blinks[i - 1].get_time_range()[1]
        curr_blink_start = blinks[i].get_time_range()[0]

        lengths.append((curr_blink_start, blinks[i].get_duration()))
        times_between.append((prev_blink_end, curr_blink_start - prev_blink_end))

    return lengths, times_between


def _plot_data(data_dict, name_prefix):
    """
    Takes data and plots it to make it ready for human-driven analysis.
    :param data_dict: string -> numpy array dictionary. Key string
        indicates the name of the data that is the stored in 2-column
        (timespan, value) numpy array.
    :param name_prefix: What prefix should be used before standard
        data name for saving pyplot figures.
    """
    for i, (key, data) in enumerate(data_dict.items()):
        timespans, values = zip(*data)  # unzip list of tuples
        plt.figure(f'{name_prefix}_{key}')
        plt.suptitle(name_prefix + ' ' + key)
        plt.xlabel('time')
        plt.ylabel('value')
        plt.plot(timespans, values)
        if SAVE_FIGS:
            fig_path = os.path.join(ANALYSIS_OUTPUT_DIR,
                                    f'{name_prefix}_{key}.png')
            plt.savefig(fig_path)

        if RENDER_FIGS:
            plt.show()


if __name__ == '__main__':
    logging.basicConfig(level=LOGGING_LEVEL)
    main()
