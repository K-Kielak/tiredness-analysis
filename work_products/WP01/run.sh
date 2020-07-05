#!/bin/bash
for person_id_folder in video/*; do
  for video_class in $person_id_folder/*; do
    person_id="$(cut -d'/' -f2 <<<"$video_class")"
    class_id="$(cut -d'/' -f3 <<<"$video_class")"
    class_id="${class_id%.*}"
    output_filename=output/$person_id'_'$class_id'.csv'
    python main.py process_videos $video_class $output_filename &
    done
wait
done
