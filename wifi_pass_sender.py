import subprocess
import re
command = "netsh wlan show profile"
test_str = subprocess.check_output("netsh wlan show profile", shell=True)


regex = rb": (.*?\r\n)"
regex2 = rb"(?: Key Content            : )(.*?\n)"

password = []
matches = re.findall(regex, test_str, re.DOTALL)

for i in matches:
    i = (i.decode("utf-8")).rstrip()
    out = subprocess.check_output('netsh wlan show profile'+' "'+i+'" key=clear', shell=True)
    output = re.findall(regex2, out, re.DOTALL)
    try:
        password.append({"wifi": i, "password": (output[0].decode("utf-8")).rstrip()})
    except IndexError:
        password.append({"wifi": i, "password": ""})

print(password)
    #password.append({"wifi": i, "password": output})
