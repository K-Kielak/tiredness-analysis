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
FRAMES_TO_SKIP = 1  # Every frametoskip'th frame is included in the analysis
RENDER_FIGS = True
SAVE_FIGS = True

LOGGING_LEVEL = logging.INFO
