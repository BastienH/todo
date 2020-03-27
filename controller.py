from datetime import datetime

class Control:
    def __init__(self):
        self.state = False
        self.last_start = ""
        self.last_stop = ""
        
    def start(self):
        self.state = True
        self.start_time = datetime.now()

    def stop(self):
        self.state = False
        self.last_stop = datetime.now()

