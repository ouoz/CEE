import bluetooth
import threading

import BlueRecord
import BlueDetect

def main():
    PORT = 1
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(('', PORT))
    server_sock.listen(1) # backlog: 接続待ち受け数
    
    #Detect = BlueDetect.Detecting()
    #Record = BlueRecord.Recording()
    
    #detect = threading.Thread(target=Detect.detect)
    #record = threading.Thread(target=Record.record)
    
    client_sock, client_addrport = server_sock.accept() # blocking until connection
    dalive = False
    ralive = False
    while True: 
        data = client_sock.recv(1024)
        #print(data) # bytes
        rec = data.decode('ascii')
        if rec == "d":
            Detect = BlueDetect.Detecting()
            detect = threading.Thread(target=Detect.detect)
            detect.start()
            dalive = True
            
        if rec == "r":
            Record = BlueRecord.Recording()
            record = threading.Thread(target=Record.record)
            record.start()
            ralive = True
            
        if rec == "s":
            if dalive:
                Detect.set_exit()
                detect.join()
                dalive = False
            if ralive:
                Record.set_exit()
                record.join()
                ralive = False
            #Detect.set_exit()
            ##Record.set_exit()
            print("stop")


if __name__ == "__main__":
    main()