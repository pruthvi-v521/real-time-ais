FOLDER STRUCTURE
Real Time/

1stream_simulator.py        # Simulates real-time AIS stream

2realtime_simulator.py      # Processes stream (decode + classify)


input/
AIS_Klaipeda_From20250908_To20251008 2.csv          # Input CSV file


outputs/
    position_class_a.csv
    position_class_b.csv
    static_voyage.csv
    base_station.csv
    aids_navigation.csv
    safety_related.csv
    binary_misc.csv
    unknown_or_rare.csv

Commands to run :
In terminal 1
1. "python3 1stream_simulator.py"

   
In terminal 2:
Run this command "python3 1stream_simulator.py | python3 2realtime_simulator.py"

Checking Real-Time File Updates
"tail -f outputs/position_class_a.csv"


STEP1:
How the Real-Time Simulation Works
1stream_simulator.py

Reads the AIS CSV file line by line

Adds a small delay between messages, speed up or slower the delay by changing seconds.

Prints NMEA messages to stdout (simulated live feed)

STEP 2: 
2realtime_simulator.py

Reads messages from stdin

Decodes messages using pyais

Classifies messages by semantic meaning

Appends decoded data continuously to CSV files

💡 Files are updated continuously while the stream is running

RETURNED OUTPUT
| Output CSV             | AIS Message Types | Meaning                     |
| ---------------------- | ----------------- | --------------------------- |
| `position_class_a.csv` | 1, 2, 3           | Class A ship positions      |
| `position_class_b.csv` | 18, 19            | Class B ship positions      |
| `static_voyage.csv`    | 5, 24             | Static vessel info          |
| `base_station.csv`     | 4                 | Shore base stations         |
| `aids_navigation.csv`  | 21                | AtoN                        |
| `safety_related.csv`   | 7, 10, 12–15      | Safety & acknowledgments    |
| `binary_misc.csv`      | 6, 8, 20, 23, 27  | Binary / addressed messages |
| `unknown_or_rare.csv`  | 9, 11             | Rare or special             |
