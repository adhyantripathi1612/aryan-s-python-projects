import socket
import threading
import sys
from datetime import datetime

# Chat log file
log_file = "chat_history.txt"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 5050
wifi_ip = socket.gethostbyname(socket.gethostname())

print(f"🌐 LOCAL: 127.0.0.1:{PORT}")
print(f"📶 WIFI: {wifi_ip}:{PORT}")

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", PORT))
server.listen(5)
print("✅ Server ready - Logs saved to chat_history.txt")

clients = {}

def log_message(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

def handle_client(conn, addr):
    # Get client name
    try:
        name = conn.recv(1024).decode().strip()
        if not name:
            name = "Anonymous"
    except:
        name = "Anonymous"
    
    clients[conn] = name
    print(f"✅ {name} ({addr}) joined")
    
    # Log + broadcast join
    log_message(f"** {name} joined **")
    broadcast(f"** {name} joined **\n".encode())
    
    while True:
        try:
            msg = conn.recv(1024).decode().strip()
            if msg:
                full_msg = f"{name}: {msg}"
                log_message(full_msg)
                broadcast(f"{full_msg}\n".encode())
        except:
            print(f"❌ {name} left")
            log_message(f"** {name} left **")
            broadcast(f"** {name} left **\n".encode())
            if conn in clients:
                del clients[conn]
            conn.close()
            break

def broadcast(msg):
    for conn in list(clients.keys()):
        try:
            conn.send(msg)
        except:
            if conn in clients:
                del clients[conn]

print("🚀 Waiting for connections...")
while True:
    try:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
