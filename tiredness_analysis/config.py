import logging
import os
from datetime import datetime


PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(PROJECT_ROOT_DIR, 'output')


ANALYSIS_DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
ANALYSIS_OUTPUT_DIR = os.path.join(OUTPUTS_DIR, ANALYSIS_DATE)

# Videos to analyze should be videos from the same recording/working
# session inserted in the recording order for the script to produce
# proper results. Script assumes continuity of the videos in its analysis.
VIDS_TO_ANALYZE = [
     'paths/to/videos/to/analyze'
]
# Path to the file storing closedness data. File should follow/follows csv
# format with 4 columns of the same length, respectively: timespan, left
# closedness, right closedness, reprojection error. Depending on the variable
# content, 3 different cases may follow:
# 1. If None, data will be neither saved to not loaded from the file.
# 2. If file under the path exists, it will be used to load the closedness data
#   instead of processing the videos frame by frame.
# 3. Otherwise, after extraction of the closedness data from the videos, it
#   will be saved in a newly created file under the specified filepath.
DATA_FILEPATH = None

BATCH_SIZE = 30  # How many frames are analyzed at once
FRAMES_TO_SKIP = 1  # Every frametoskip'th frame is included in the analysis
RENDER_FIGS = True

LOGGING_LEVEL = logging.INFO
