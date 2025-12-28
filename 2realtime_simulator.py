'''Reads messages from stdin

Applies Step 1 (preprocess)

Applies Step 2 (decode)

Applies Step 3 (classification)'''

import sys
import csv
from collections import Counter
from pyais.stream import IterMessages
from pathlib import Path

# =====================
# OUTPUT FILES
# =====================
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

FILES = {
    "position_class_a": (1, 2, 3),
    "position_class_b": (18, 19),
    "static_voyage": (5, 24),
    "aids_navigation": (21,),
    "base_station": (4,),
    "safety_related": (7, 10, 12, 13, 14, 15),
    "binary_misc": (6, 8, 20, 23, 27),
}

writers = {}
files = {}
counts = Counter()

def get_writer(name, fields):
    if name not in writers:
        f = open(OUT_DIR / f"{name}.csv", "w", newline="")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writers[name] = writer
        files[name] = f
    return writers[name]

# =====================
# REAL-TIME LOOP
# =====================
print("🚀 Real-time AIS processing started...\n")

for msg in IterMessages(sys.stdin.buffer):
    try:
        decoded = msg.decode()
        data = decoded.asdict()

        msg_type = data.get("msg_type")
        if msg_type is None:
            continue

        # classification
        target = "binary_misc"
        for name, types in FILES.items():
            if msg_type in types:
                target = name
                break

        writer = get_writer(target, data.keys())
        writer.writerow(data)

        counts[f"type{msg_type}"] += 1

    except Exception:
        continue

# =====================
# CLEANUP
# =====================
for f in files.values():
    f.close()

print("\n📊 Message counts:")
for k, v in counts.most_common():
    print(k, v)
