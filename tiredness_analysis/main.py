import logging
import os

import matplotlib.pyplot as plt
import numpy as np

from tiredness_analysis.config import ANALYSIS_OUTPUT_DIR, BATCH_SIZE
from tiredness_analysis.config import FRAMES_TO_SKIP, LOGGING_LEVEL
from tiredness_analysis.config import RENDER_FIGS, VIDS_TO_ANALYZE
from tiredness_analysis.videos_analyzer import VideoAnalyzer


logger = logging.getLogger(__name__)


def main():
    os.mkdir(ANALYSIS_OUTPUT_DIR)
    videos_analyzer = VideoAnalyzer(BATCH_SIZE)
    analyzed_data = videos_analyzer.analyze_videos(VIDS_TO_ANALYZE,
                                                   FRAMES_TO_SKIP)
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
        linear_trend = np.poly1d(np.polyfit(timespans, values, 1))
        quadratic_trend = np.poly1d(np.polyfit(timespans, values, 2))
        cubic_trend = np.poly1d(np.polyfit(timespans, values, 3))
        quintic_trend = np.poly1d(np.polyfit(timespans, values, 5))

        plt.figure(key)
        plt.suptitle(key)
        plt.xlabel('time')
        plt.ylabel('value')
        plt.plot(timespans, values, 'bo', label='data')
        plt.plot(timespans, linear_trend(timespans),
                 '-r', label='linear trend')
        plt.plot(timespans, quadratic_trend(timespans),
                 '-g', label='quadratic trend')
        plt.plot(timespans, cubic_trend(timespans),
                 '-y', label='cubic trend')
        plt.plot(timespans, quintic_trend(timespans),
                 '-k', label='quintic trend')
        plt.legend(loc='best')
        plt.grid(True)

        if output_dir:
            fig_path = os.path.join(output_dir, f'{key}.png')
            plt.savefig(fig_path)

        if render_figs:
            plt.show()


if __name__ == '__main__':
    logging.basicConfig(level=LOGGING_LEVEL)
    main()
