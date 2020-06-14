import csv
import itertools
import logging
import os
from collections import deque
from statistics import mean, stdev
from typing import Union

import click

from tiredness_analysis.videos_analysis import analyze_data, AnalyzedData
from tiredness_analysis.videos_processor import load_processed_videos


logger = logging.getLogger(__name__)


@click.command('extract_features')
@click.option('--input_data', '-i', required=True,
              type=click.Path(dir_okay=False, exists=True, readable=True),
              help='Path to the processed (extracted) video data.')
@click.option('--output_file', '-o', required=True,
              type=click.Path(dir_okay=False, writable=True),
              help='Directory where produced plots should be saved.')
@click.option('--period_length', '-p', default=float('inf'), show_default=True, type=float,
              help='Expects float value representing seconds. It controls '
                   'how much time is used for each data point. E.g., if '
                   'given `--input_data` contains 10 minutes of video data '
                   'and `--period_length` is 120 (2 minutes), the script '
                   'will produce 5 distinct feature vectors, each for the '
                   'separate 2 minute period.')
def extract_features(input_data: Union[str, os.PathLike],
                     output_file: Union[str, os.PathLike],
                     period_length: float):
    """Produces feature vectors based on the processed video data.

    Given video data can be transformed into a single feature vector (default
    behavior) or into multiple temporally segmented data points.
    """
    data = load_processed_videos(input_data)
    data = analyze_data(data)
    write_means_stds_to_csv(data, period_length, output_file)


def write_means_stds_to_csv(data: AnalyzedData,
                            period_length: float,
                            output_file: Union[str, os.PathLike]):
    """Splits data into distinct periods and saves it to csv.

    WARNING: it mutates provided data collection.
    """
    logger.info(f'Splitting data into periods '
                f'and writing features to {output_file}...')
    with open(output_file, 'w') as f:
        writer = csv.writer(f)

        header = ((f'{field}_mean', f'{field}_std') for field in data._fields)
        header = itertools.chain(*header)
        writer.writerow(header)

        curr_period_end = 0
        # While there are still values left in the passed data
        while sum([len(measurements) for measurements in data]) > 0:
            curr_period_end += period_length
            row = []
            for i, measurements in enumerate(data):
                curr_period_measurements = deque()
                while len(measurements) > 0 and measurements[0][0] < curr_period_end:
                    # Get all values for this measurement that fit into current period
                    curr_period_measurements.append(measurements.popleft()[1])

                row.append(mean(curr_period_measurements))
                if len(curr_period_measurements) > 2:
                    row.append(stdev(curr_period_measurements))
                else:
                    logger.warning(f'There was not enough data points for '
                                   f'{data._fields[i]} in period ending at'
                                   f'{curr_period_end} to calculate stanard'
                                   f'deviation. Writing `nan` instead.')
                    row.append(float('nan'))

            writer.writerow(row)

    logger.info('Features have been extracted and saved.')
