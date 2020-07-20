# Extract features from processed UTA-RLDD dataset

Extracts features from processed UTA-RLDD videos using `extract_features` script.
After running the main `run.sh` script, CSV with extracted features and matched 
labels can be found in the `outputs/data.csv` location in the WP.

## Steps to reproduce
Place the processed videos in the `processed_videos/` directory inside the WP.

Videos are expected to be in subdirectories corresponding to their label. I.e.
videos with label `0` are expected to be in `processed_videos/0/`, with `5` 
in `processed_videos/5/` and with `10` in `processed_videos/10/`.

