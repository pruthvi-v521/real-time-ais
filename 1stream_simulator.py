import csv
import time
import sys

INPUT_CSV = "input/AIS_Klaipeda_From20250908_To20251008 2.csv"
DELAY_SECONDS = 0.01   # adjust: 0.1 = slower, 0.001 = faster

def stream():
    with open(INPUT_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nmea = row["nmea_message"].strip()
            if nmea:
                print(nmea)
                sys.stdout.flush()
                time.sleep(DELAY_SECONDS)

if __name__ == "__main__":
    stream()
