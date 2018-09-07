import time


class StopWatch:

    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        duration = time.time() - self.start_time
        '''From seconds to Days;Hours:Minutes;Seconds'''

        value_d = (((duration / 365) / 24) / 60)
        days = int(value_d)

        value_h = (value_d - days) * 365
        hours = int(value_h)

        value_m = (value_h - hours) * 24
        minutes = int(value_m)

        value_s = (value_m - minutes) * 60
        seconds = int(value_s)

        print("Rendering took", days, ";", hours, ":", minutes, ";", seconds)
