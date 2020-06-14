import csv
import logging
import sys
import time
from collections import deque, namedtuple

from teyered.io.video_generator import VideoGenerator
from teyered.teyered_processor import TeyeredProcessor


logger = logging.getLogger(__name__)


ProcessedVideos = namedtuple('ProcessedVideos', ['timespans',
                                                 'left_eye_closedness',
                                                 'right_eye_closedness',
                                                 'pose_reprojection_err'])


class VideosProcessor:

    def __init__(self, batch_size, frames_to_skip=1):
        logger.debug('Initializing VideoProcessor...')
        self._processor = TeyeredProcessor()
        self._batch_size = batch_size
        self._frames_to_skip = frames_to_skip

        self._last_vid_end_timespan = 0
        self._processed_data = ProcessedVideos(deque(), deque(), deque(), deque())
        logger.debug('VideoProcessor initialized.')

    def process_videos(self, videos):
        """Processes videos one by one and outputs processed video data."""
        for vid in videos:
            logger.info(f'Processing video {vid}...')
            with VideoGenerator(vid, self._frames_to_skip) as vid_gen:
                self._process_video(vid_gen)

        return self._processed_data

    def _process_video(self, video):
        self._processor.reset()
        analysis_start = time.time()
        curr_vid_end_timespan = 0
        times = deque()
        batch = deque()
        for i, (timespan, frame) in enumerate(video):
            times.append(self._last_vid_end_timespan + timespan)
            batch.append(frame)
            if len(batch) % self._batch_size == 0 or video.is_over():
                curr_vid_end_timespan = self._last_vid_end_timespan + timespan
                processed_batch = self._processor.process(batch)
                self._processed_data.timespans.extend(times)
                self._processed_data.left_eye_closedness \
                    .extend(processed_batch.left_eye_closedness)
                self._processed_data.right_eye_closedness \
                    .extend(processed_batch.right_eye_closedness)
                self._processed_data.pose_reprojection_err \
                    .extend(processed_batch.pose_reprojection_err)

                # Use sys.stdout.write instead of logger so as to
                # flush frequently without generating a line break.
                sys.stdout.write(f'\rAnalyzed {i + 1} frames so far, time '
                                 f'passed: {time.time() - analysis_start}')
                sys.stdout.flush()
                batch = []
                times = []

        self._last_vid_end_timespan = curr_vid_end_timespan


def save_processed_videos(processed_videos, output_file):
    logger.info(f'Saving processed videos to {output_file}...')
    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(processed_videos._fields)
        writer.writerows(zip(*processed_videos._asdict().values()))
    logger.info(f'Saving processed videos has finished.')


def load_processed_videos(processed_videos_file):
    logger.info(f'Loading processed videos from {processed_videos_file}...')
    data = ProcessedVideos(deque(), deque(), deque(), deque())
    with open(processed_videos_file, 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            for key, value in line.items():
                getattr(data, key).append(float(value))

    logger.info(f'Loading processed videos has finished.')
    return data
