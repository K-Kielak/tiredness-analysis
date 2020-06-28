import logging
import os
from typing import Union, Sequence

import click

from tiredness_analysis.videos_processor import VideosProcessor
from tiredness_analysis.videos_processor import save_processed_videos


logger = logging.getLogger(__name__)


@click.command('process_videos')
@click.option('--batch_size', '-b', default=100, show_default=True, type=int,
              help='Batch size used for processing videos. The bigger, the '
                   'faster the processing but higher RAM usage.')
@click.option('--frames_to_skip', '-f', default=0, show_default=True, type=int,
              help='For each extracted frame, further `frames_to_skip` will '
                   'be skipped. The higher, the faster the processing but '
                   'the less accurate is the output.')
@click.argument('videos', required=True, type=click.Path(exists=True, readable=True), nargs=-1)
@click.argument('output_file', required=True, type=click.Path(dir_okay=False, writable=True), nargs=1)
def process_videos(batch_size: int,
                   frames_to_skip: int,
                   videos: Sequence[Union[str, os.PathLike]],
                   output_file: Union[str, os.PathLike]):
    """Extracts all the necessary data from videos and saves it for analysis.

    VIDEOS is the list of videos that are going to be processed. This tool
    assumes that all the given videos are part of *the same continuous
    session* and are provided *in order* (i.e. video 2 starts just after
    video 1 has finished, video 3 starts just after video 2 has finished,
    and so on). If you want to process multiple videos from different
    sessions, you need to run this tool for each of the sessions
    separately.

    OUTPUT_FILE is the filename under which data extracted from videos
    should be saved.
    """
    logger.info('Processing videos...')
    processor = VideosProcessor(batch_size, frames_to_skip)
    processed_vids = processor.process_videos(videos)
    save_processed_videos(processed_vids, output_file)


