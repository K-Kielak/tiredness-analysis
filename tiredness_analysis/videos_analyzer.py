import csv
import logging
import os
import sys
import time

from teyered.data_processing.blinks.blinks_detection import detect_blinks
from teyered.io.video_generator import VideoGenerator
from teyered.teyered_processor import TeyeredProcessor


logger = logging.getLogger(__name__)


LEFT_EYE_PREFIX = 'left_'
RIGHT_EYE_PREFIX = 'right_'


class VideoAnalyzer:

    def __init__(self, batch_size):
        """
        Initializes VideoAnalyzer object
        :param batch_size: int, specifies how many video frame are extracted
            into the frames batch before processing and extracting information
            from the batch. Higher batch size may lead to slightly faster
            algorithm but highly increases RAM requirements.
        """
        self._processor = TeyeredProcessor()
        self._batch_size = batch_size
        # Objects init lazily on _reset() when analyze_videos(...) is called
        self._data = {}
        self._last_vid_end_timespan = 0

    def analyze_videos(self, vids_paths, frames_to_skip=1, data_path=None):
        """
        Analyzes videos and returns the results of the analysis. Assumes
        that passed videos are single, distinct chunk of recording and are
        ordered chronologically.
        :param vids_paths: absolute path to the videos that should be analyzed.
        :param frames_to_skip: int, how many frames should be skipped in
            in between successfuly analyzed frames. Can be used to trade-off
            quality of analysis for performance/data usage.
        :param data_path: file path where the freshly extracted data from the
            videos should be saved. If file exists, it will be used to load
            the data instead of processing the videos frame by frame. None if
            data should be neither saved nor loaded.
        :return: The necessary results of analysis - eyes closedness and pose
            projection error.
        """
        self._reset()
        if data_path is not None and os.path.exists(data_path):
            self._load_data(data_path)
        else:
            self._process_videos(vids_paths, frames_to_skip)
            if data_path is not None:
                self._save_data(data_path)

        logger.info('Extracting information from all videos has finished.')
        logger.info('Starting blinks calculation...')
        self._remove_undetermined_closedness(LEFT_EYE_PREFIX)
        self._remove_undetermined_closedness(RIGHT_EYE_PREFIX)
        self._calc_blinks_data(LEFT_EYE_PREFIX)
        self._calc_blinks_data(RIGHT_EYE_PREFIX)
        logger.info('Blinks calculation has finished')
        return self._data

    def _load_data(self, data_path):
        logger.info(f'Loading data from {data_path}...')
        with open(data_path, 'r') as datafile:
            reader = csv.reader(datafile)
            for t, lc, rc, err in reader:
                t = float(t)
                self._data['left_eye_closedness'].append((t, float(lc)))
                self._data['right_eye_closedness'].append((t, float(rc)))
                self._data['pose_reprojection_err'].append((t, float(err)))
        logger.info('Loading data has finished.')

    def _save_data(self, data_path):
        logger.info(f'Saving data to {data_path}...')
        with open(data_path, 'w') as datafile:
            writer = csv.writer(datafile)
            data_to_save = zip(
                self._data['left_eye_closedness'],
                self._data['right_eye_closedness'],
                self._data['pose_reprojection_err']
            )
            for lc, rc, err in data_to_save:
                timespan = lc[0]  # == rc[0] == err[0]
                writer.writerow((timespan, lc[1], rc[1], err[1]))
        logger.info(f'Saving data has finished.')

    def _process_videos(self, vids_paths, frames_to_skip):
        for filepath in vids_paths:
            logger.info(f'Analyzing video {filepath}...')
            with VideoGenerator(filepath, frames_to_skip) as video:
                self._analyze_video(video)
            logger.info(f'Analyzing video {filepath} has finished.')

    def _analyze_video(self, video):
        self._processor.reset()

        analysis_start = time.time()
        curr_vid_end_timespan = 0
        times = []
        batch = []
        for i, (timespan, frame) in enumerate(video):
            times.append(self._last_vid_end_timespan + timespan)
            batch.append(frame)
            if len(batch) % self._batch_size == 0 or video.is_over():
                curr_vid_end_timespan = self._last_vid_end_timespan + timespan
                processed_batch = self._processor.process(batch)
                self._data['left_eye_closedness'] += \
                    zip(times, processed_batch.left_eye_closedness)
                self._data['right_eye_closedness'] += \
                    zip(times, processed_batch.right_eye_closedness)
                self._data['pose_reprojection_err'] += \
                    zip(times, processed_batch.pose_reprojection_err)
                # Use sys.stdout.write instead of logger so as to
                # flush frequently without generating a line break.
                sys.stdout.write(f'\rAnalyzed {i+1} frames so far, time '
                                 f'passed: {time.time() - analysis_start}')
                sys.stdout.flush()
                batch = []
                times = []

        self._last_vid_end_timespan = curr_vid_end_timespan

    def _remove_undetermined_closedness(self, prefix):
        self._data[f'{prefix}eye_closedness'] = \
            [(t, c) for t, c in self._data[f'{prefix}eye_closedness'] if c >= 0]

    def _calc_blinks_data(self, prefix):
        measurements = self._data[f'{prefix}eye_closedness']
        blinks = detect_blinks(measurements)
        self._data[f'{prefix}blink_lengths'] = [(blinks[0].get_time_range()[0],
                                                 blinks[0].get_duration())]
        for i in range(1, len(blinks)):
            prev_blink_end = blinks[i - 1].get_time_range()[1]
            curr_blink_start = blinks[i].get_time_range()[0]
            self._data[f'{prefix}blink_lengths']\
                .append((curr_blink_start, blinks[i].get_duration()))
            self._data[f'{prefix}time_between_blinks']\
                .append((prev_blink_end, curr_blink_start - prev_blink_end))

    def _reset(self):
        self._processor.reset()
        self._data = {
            'left_eye_closedness': [],
            'right_eye_closedness': [],
            'pose_reprojection_err': [],
            'left_blink_lengths': [],
            'left_time_between_blinks': [],
            'right_blink_lengths': [],
            'right_time_between_blinks': []
        }
        self._last_vid_end_timespan = 0
