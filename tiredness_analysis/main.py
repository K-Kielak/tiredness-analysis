import logging
import os

import matplotlib.pyplot as plt
import numpy as np

from tiredness_analysis.config import ANALYSIS_OUTPUT_DIR, BATCH_SIZE
from tiredness_analysis.config import DATA_FILEPATH, FRAMES_TO_SKIP
from tiredness_analysis.config import LOGGING_LEVEL, RENDER_FIGS
from tiredness_analysis.config import VIDS_TO_ANALYZE
from tiredness_analysis.videos_analyzer import VideoAnalyzer


logger = logging.getLogger(__name__)


SUBPLOT_NROWS = 1
SUBPLOT_NCOLS = 2
VARIANCE_OPACITY = 0.5
MOVING_STATS_POINTS = 10
OUTLIERS_THRESHOLD_COEFF = 3


def main():
    os.mkdir(ANALYSIS_OUTPUT_DIR)
    videos_analyzer = VideoAnalyzer(BATCH_SIZE)
    analyzed_data = videos_analyzer.analyze_videos(VIDS_TO_ANALYZE,
                                                   FRAMES_TO_SKIP,
                                                   DATA_FILEPATH)
    _plot_data(analyzed_data,
               render_figs=RENDER_FIGS,
               output_dir=ANALYSIS_OUTPUT_DIR)


def _plot_data(data_dict, render_figs=True, output_dir=None):
    """
    Takes data and plots it to make it ready for human-driven analysis.
    :param data_dict: string -> list dict. Key string indicates the name of the
        data that is the stored in a list of tuples (timespan, value).
    :param render_figs: boolean specifying if the figures should be rendered
        live while executing the program.
    :param output_dir: string specifying directory path where the figures
        should be saved. None if figures shouldn't be saved anywhere.
    """
    for i, (key, data) in enumerate(data_dict.items()):
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
        min_plot_val, max_plot_val = _find_min_max_excuding_outliers(values)

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
        plt.plot(mvstats_timespans, moving_mean, 'r-', zorder=3,
                 label='moving mean')
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
            fig_path = os.path.join(output_dir, f'{key}.png')
            plt.savefig(fig_path)
        if render_figs:
            plt.show()


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


def _find_min_max_excuding_outliers(values):
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


if __name__ == '__main__':
    logging.basicConfig(level=LOGGING_LEVEL)
    main()
