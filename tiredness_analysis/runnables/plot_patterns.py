import logging
import pathlib

import click
import matplotlib.pyplot as plt
import numpy as np

from tiredness_analysis.videos_analysis import analyze_data
from tiredness_analysis.videos_processor import load_processed_videos


logger = logging.getLogger(__name__)


SUBPLOT_NROWS = 1
SUBPLOT_NCOLS = 2
VARIANCE_OPACITY = 0.5
MOVING_STATS_POINTS = 10
OUTLIERS_THRESHOLD_COEFF = 3


@click.command('plot_patterns')
@click.option('--input_data', '-i', required=True,
              type=click.Path(dir_okay=False, exists=True, readable=True),
              help='Path to the processed (extracted) video data.')
@click.option('--output_dir', '-o', required=True,
              type=click.Path(file_okay=False, writable=True),
              help='Directory where produced plots should be saved.')
def plot_patterns(input_data, output_dir):
    """Performs an analysis of the videos data and plots its results."""
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    data = load_processed_videos(input_data)
    data = analyze_data(data)
    _plot_data(data, output_dir=output_dir)


def _plot_data(data, output_dir=None):
    for i, (key, data) in enumerate(data._asdict().items()):
        logger.info(f'Plotting {key}...')
        timespans, values = zip(*data)  # unzip list of tuples

        # Calculate moving stats and trends
        moving_mean, moving_std = _calc_moving_stats(values)
        std_above = moving_mean + moving_std
        std_below = moving_mean - moving_std
        mvstats_timespans = timespans[len(timespans) - len(moving_mean):]
        mean_trend = np.poly1d(np.polyfit(mvstats_timespans, moving_mean, 1))
        std_above_trend = np.poly1d(np.polyfit(mvstats_timespans, std_above, 1))
        std_below_trend = np.poly1d(np.polyfit(mvstats_timespans, std_below, 1))

        # Find maximum and minimum values (excluding outliers) to limit plots
        min_plot_val, max_plot_val = _find_min_max_excluding_outliers(values)

        plt.figure(key, figsize=(12.8, 4.8))
        plt.suptitle(key)

        # Plotting pure values subplot
        plt.subplot(SUBPLOT_NROWS, SUBPLOT_NCOLS, 1)
        plt.title('values')
        plt.xlabel('time')
        plt.ylabel('value')
        plt.ylim(min_plot_val, max_plot_val)
        plt.plot(timespans, values, 'b.', zorder=0, label='data', markersize=1)
        plt.fill_between(mvstats_timespans, std_below, std_above, zorder=1,
                         facecolor='r',  alpha=1 - VARIANCE_OPACITY)
        plt.plot(mvstats_timespans, std_above_trend(mvstats_timespans), 'k:',
                 zorder=2)
        plt.plot(mvstats_timespans, std_below_trend(mvstats_timespans), 'k:',
                 zorder=2, label='std trends')
        plt.plot(mvstats_timespans, mean_trend(mvstats_timespans), 'k--',
                 zorder=2, label='trend')
        plt.plot(mvstats_timespans, moving_mean, 'r-',
                 zorder=3, label='moving mean')
        plt.legend(loc='best')
        plt.grid(True)

        # Plotting histogram subplot
        plt.subplot(SUBPLOT_NROWS, SUBPLOT_NCOLS, 2)
        plt.title('histogram')
        plt.xlabel('value')
        plt.ylabel('frequency')
        plt.hist(values, bins=50, range=(min_plot_val, max_plot_val))
        plt.grid(True)

        # Saving/rendering plots
        if output_dir:
            fig_path = pathlib.Path(output_dir).joinpath(f'{key}.png')
            plt.savefig(fig_path)


def _calc_moving_stats(data):
    window_size = len(data) // MOVING_STATS_POINTS
    stats_length = len(data) - window_size + 1
    mean = np.zeros(stats_length)
    variance = np.zeros(stats_length)

    # Calc initial window
    mean[0] = np.mean(data[:window_size])
    variance[0] = np.var(data[:window_size])

    # Calculate following windows reusing the initial one
    for i in range(1, stats_length):
        new_x = data[i + window_size - 1]
        old_x = data[i - 1]
        mean_change = (new_x-old_x) / window_size
        mean[i] = mean[i - 1] + mean_change
        variance_change = (new_x-old_x) * (new_x-mean[i] + old_x-mean[i - 1])
        variance_change = variance_change / window_size
        variance[i] = variance[i - 1] + variance_change

    return mean, np.sqrt(variance)


def _find_min_max_excluding_outliers(values):
    std = np.std(values)
    mean = np.mean(values)
    min_val = mean
    max_val = mean
    max_distace_from_mean = std * OUTLIERS_THRESHOLD_COEFF
    for v in values:
        if v > max_val and max_val - mean < max_distace_from_mean:
            max_val = v

        if v < min_val and mean - min_val < max_distace_from_mean:
            min_val = v

    return min_val, max_val
