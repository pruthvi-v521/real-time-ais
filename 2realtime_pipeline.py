import sys
import csv
import socket
from pathlib import Path
from collections import Counter, defaultdict
from pyais.stream import IterMessages

# ======================================================
# CONFIG
# ======================================================

USE_TCP = True        # set True if using socket server
TCP_HOST = "127.0.0.1"
TCP_PORT = 9000

OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

# Message type grouping
FILES = {
    "position_class_a": (1, 2, 3),
    "position_class_b": (18, 19),
    "static_voyage": (5, 24),
    "base_station": (4,),
    "aids_navigation": (21,),
    "safety_related": (7, 10, 12, 13, 14, 15),
    "binary_misc": (6, 8, 20, 23, 27),
}

# ======================================================
# CLEANING RULES (TYPE AWARE)
# ======================================================

def valid_mmsi(m):
    try:
        m = int(m)
        return 100000000 <= m <= 999999999
    except:
        return False

def valid_lat(lat):
    try:
        lat = float(lat)
        return -90 <= lat <= 90
    except:
        return False

def valid_lon(lon):
    try:
        lon = float(lon)
        return -180 <= lon <= 180
    except:
        return False

def valid_sog(sog):
    try:
        sog = float(sog)
        return 0 <= sog <= 102.2
    except:
        return False

def clean_row(group, row):
    """
    Returns: (keep: bool, reason: str | None)
    """

    # MMSI required for most messages
    if group not in ("base_station", "binary_misc"):
        if not valid_mmsi(row.get("mmsi")):
            return False, "invalid_mmsi"

    # Position messages
    if group in ("position_class_a", "position_class_b", "aids_navigation"):
        if not valid_lat(row.get("lat")):
            return False, "invalid_lat"
        if not valid_lon(row.get("lon")):
            return False, "invalid_lon"

    # Speed only applies to position reports
    if group in ("position_class_a", "position_class_b"):
        if not valid_sog(row.get("speed")):
            return False, "invalid_sog"

    # Static voyage: shipname allowed to be empty but MMSI must be valid
    if group == "static_voyage":
        if not valid_mmsi(row.get("mmsi")):
            return False, "invalid_mmsi"

    # Safety related: multiple MMSI fields allowed to be empty
    # Base station: MMSI can be shore station → do not filter

    return True, None

# ======================================================
# OUTPUT MANAGEMENT
# ======================================================

writers = {}
files = {}

stats_total = Counter()
stats_kept = Counter()
stats_removed = Counter()
removal_reasons = defaultdict(Counter)

def get_writer(name, fields):
    if name not in writers:
        f = open(OUT_DIR / f"{name}.csv", "w", newline="", buffering=1)
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writers[name] = writer
        files[name] = f
    return writers[name]

# ======================================================
# INPUT STREAM
# ======================================================

if USE_TCP:
    print("🔌 Connecting to TCP AIS stream...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_HOST, TCP_PORT))
    stream = sock.makefile("rb")
else:
    stream = sys.stdin.buffer

print("🚀 Real-time AIS pipeline started...\n")

# ======================================================
# MAIN REAL-TIME LOOP
# ======================================================

try:
    for msg in IterMessages(stream):
        try:
            decoded = msg.decode()
            data = decoded.asdict()
            msg_type = data.get("msg_type")

            if msg_type is None:
                continue

            # determine target group
            group = "binary_misc"
            for name, types in FILES.items():
                if msg_type in types:
                    group = name
                    break

            stats_total[group] += 1

            keep, reason = clean_row(group, data)

            if not keep:
                stats_removed[group] += 1
                removal_reasons[group][reason] += 1
                continue

            writer = get_writer(group, data.keys())
            writer.writerow(data)
            stats_kept[group] += 1

        except Exception:
            continue

except KeyboardInterrupt:
    print("\n🛑 Stream stopped by user")

# ======================================================
# CLEANUP
# ======================================================

for f in files.values():
    f.close()

if USE_TCP:
    sock.close()

# ======================================================
# FINAL REPORT
# ======================================================

print("\n📊 CLEANING SUMMARY\n")

for group in FILES.keys():
    total = stats_total[group]
    kept = stats_kept[group]
    removed = stats_removed[group]

    if total == 0:
        continue

    print(group)
    print("-" * len(group))
    print(f"Total rows   : {total}")
    print(f"Kept rows    : {kept}")
    print(f"Removed rows : {removed}")

    if removed:
        print("Removal reasons:")
        for r, c in removal_reasons[group].items():
            print(f"  - {r}: {c}")
    print()
