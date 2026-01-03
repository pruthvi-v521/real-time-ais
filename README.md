real-time-ais/
├── input/                       # Place your AIS CSV input files here
│   └── AIS_Klaipeda_From20250908_To20251008 2.csv
├── outputs/                     # Real-time outputs (CSV files will appear here)
│   ├── position_class_a.csv
│   ├── position_class_b.csv
│   ├── static_voyage.csv
│   ├── base_station.csv
│   ├── safety_related.csv
│   └── binary_misc.csv
├── 1stream_simulator.py         # Simulates real-time streaming from CSV
├── 2realtime_pipeline.py        # Receives, decodes, normalizes, classifies, cleans, writes output
└── README.md

How to Run
Step 1: Prepare input

Create a folder called input

Place your AIS CSV file(s) in it, e.g., AIS_sample.csv

Ensure the CSV has a column called nmea_message containing the AIS messages

STEP 2: Run Stream Simulator (Terminal 1)
python3 1stream_simulator.py


Starts a TCP server on 0.0.0.0:9000

Simulates sending AIS messages line-by-line with a small delay

STEP 3: Run Real-Time Pipeline (Terminal 2)
python3 2realtime_pipeline.py


Connects to the simulator server (127.0.0.1:9000)

Decodes, normalizes, classifies, cleans, and writes CSV files

Outputs appear in outputs/ folder continuously

Tip: You can monitor live CSV growth using:
tail -f outputs/position_class_a.csv

Once server is stopped :
Cleaning summary is obtained
CLEANING SUMMARY

position_class_a
----------------
Total rows   : 4999
Kept rows    : 4711
Removed rows : 288
Removal reasons:
  - invalid_lat: 287
  - invalid_sog: 1

position_class_b
----------------
Total rows   : 281
Kept rows    : 281
Removed rows : 0

static_voyage
-------------
Total rows   : 296
Kept rows    : 141
Removed rows : 132
Removal reasons:
  - invalid_mmsi: 132

base_station
------------
Total rows   : 243
Kept rows    : 243
Removed rows : 0

safety_related
--------------
Total rows   : 111
Kept rows    : 20
Removed rows : 80
Removal reasons:
  - invalid_mmsi: 80

binary_misc
-----------
Total rows   : 965
Kept rows    : 424
Removed rows : 0
similar to this
