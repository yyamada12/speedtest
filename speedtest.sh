while true; do
  speedtest --csv >> internet_speed.log
  sleep 60
done