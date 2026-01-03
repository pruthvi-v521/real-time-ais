import socket
import csv
import time

HOST = "0.0.0.0"
PORT = 9000
CSV_FILE = "input/AIS_Klaipeda_From20250908_To20251008 2.csv"
DELAY_SECONDS = 1  # change to speed up or slow down

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"[SERVER] AIS Streaming Server running on {HOST}:{PORT}")
    print("[SERVER] Waiting for client connection...")

    conn, addr = server_socket.accept()
    print(f"[SERVER] Client connected from {addr}")

    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            nmea = row.get("nmea_message")
            if not nmea:
                continue

            message = nmea.strip() + "\n"
            conn.sendall(message.encode("utf-8"))

            print(f"[SERVER] Sent AIS message")
            time.sleep(DELAY_SECONDS)

    conn.close()
    server_socket.close()
    print("[SERVER] Streaming finished")

if __name__ == "__main__":
    start_server()