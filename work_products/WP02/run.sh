#!/bin/bash
for person_id_folder in video/*; do
  for video_class in $person_id_folder/*; do
    person_id="$(cut -d'/' -f2 <<<"$video_class")"
    class_id="$(cut -d'/' -f3 <<<"$video_class")"
    class_id="${class_id%.*}"
    ffmpeg -i $video_class -vcodec libx265 -crf 28 video/$person_id/$class_id'_compressed.mp4' &
    done
wait
done
