# WP02 - Convert + Compress UTA-RLDD Dataset 

Loops through the UTA-RLDD videos and runs `ffpmeg -vcodec libx265 -crf 28` to reduce the size of the video and convert to the same format. 

## Steps to reproduce
- Place the contents of UTA-RLDD zip files to be in the folder `tiredness-analysis/video/` 
- Run `work_products/WP02/run.sh`
