#! /bin/sh
for ws in ws_1 ws_2 ws_3 ws_4 ws_5 ws_6 ws_7 ws_8 ws_9 ws_10 ws_17 ws_18 ws_19 ws_20 
   do
   echo "measuring throughput of web service : $ws"
   multimech-run ./$ws
   echo "collecting throughput data of web service : $ws"
   python qos_throughput.py $ws
done
