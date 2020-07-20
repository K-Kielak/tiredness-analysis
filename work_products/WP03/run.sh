

#trap "exit" INT TERM ERR
#trap "kill 0" EXIT

cd $(dirname $0)


mkdir output
output_file="output/data.csv"
log_file="output/out.log"
failed_files=0

echo "*****PROCESSING NON-TIRED VIDEOS*****"
for video in processed_videos/0/*; do
  echo "Processing non-tired video ${video}..." | tee -a ${log_file}
  python ../../main.py extract_features \
    -i "${video}" \
    -o temp.csv \
    -p 120 \
    &>> ${log_file}

  if [ $? != 0 ]; then
    failed_files=$((failed_files + 1))
  fi

  if test -f "${output_file}"; then
    echo "Writing data without header..."
    cat temp.csv \
      | sed 's/.$//' \
      | awk 'NR>1{printf("%s,0\n", $0)}' \
      >> "${output_file}"
  else
    echo "Writing data with header..."
    cat temp.csv \
      | sed 's/.$//' \
      | awk 'NR==1{printf("%s,label\n", $0)}NR>1{printf("%s,0\n", $0)}' \
      > "${output_file}"
  fi
  rm temp.csv
  echo ""
done


echo "*****PROCESSING SEMI-TIRED VIDEOS*****"
for video in processed_videos/5/*; do
  echo "Processing semi-tired video ${video}..." | tee -a ${log_file}
  python ../../main.py extract_features \
    -i "${video}" \
    -o temp.csv \
    -p 120 \
    &>> ${log_file}

  if [ $? != 0 ]; then
    failed_files=$((failed_files + 1))
  fi

  echo "Writing data without header..."
  cat temp.csv \
    | sed 's/.$//' \
    | awk 'NR>1{printf("%s,5\n", $0)}' \
    >> "${output_file}"
  rm temp.csv
  echo ""
done


echo "*****PROCESSING TIRED VIDEOS*****"
for video in processed_videos/10/*; do
  echo "Processing tired video ${video}..." | tee -a ${log_file}
  python ../../main.py extract_features \
    -i "${video}" \
    -o temp.csv \
    -p 120 \
    &>> ${log_file}

  if [ $? != 0 ]; then
    failed_files=$((failed_files + 1))
  fi

  echo "Writing data without header..."
  cat temp.csv \
    | sed 's/.$//' \
    | awk 'NR>1{printf("%s,10\n", $0)}' \
    >> "${output_file}"
  rm temp.csv
  echo ""
done

echo "[WARNING] Failed to process ${failed_files} files"
echo "Finished"
