import bluetooth
import threading

import Record
import Detect

def main():
    PORT = 1
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(('', PORT))
    server_sock.listen(1) # backlog: 接続待ち受け数
    
    detect = threading.Thread(target=Detect.detect)
    record = threading.Thread(target=Record.record)
    
    client_sock, client_addrport = server_sock.accept() # blocking until connection
    
    while True: 
        data = client_sock.recv(1024)
        #print(data) # bytes
        rec = data.decode('ascii')
        if rec == "d" and not detect.is_alive():
            detect.start()
        if rec == "r" and not record.is_alive():
            record.start()
        if rec == "s":
            Detect.set_exit()
            Record.set_exit()
            print("stop")


if __name__ == "__main__":
    main()