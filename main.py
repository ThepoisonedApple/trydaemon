import threading
import time
from sh import tail

class LogParserService(threading.Thread):
    def __init__(self):
        super(Concur, self).__init__()
        self.daemon = True  # Allow main to exit even if still running.
        self.paused = True  # Start out paused.
        self.state = threading.Condition()
        self.path="/var/log/mylog.log"

    def run(self):
        self.resume()
        for line in tail("-f",self.path,_iter=True):
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            print(line)
            

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    def pause(self):
        with self.state:
            self.paused = True  # Block self.


class Stopwatch(object):
    """ Simple class to measure elapsed times. """
    def start(self):
        """ Establish reference point for elapsed time measurements. """
        self.start_time = time.time()
        return self.start_time

    @property
    def elapsed_time(self):
        """ Seconds since started. """
        try:
            start_time = self.start_time
        except AttributeError:  # Wasn't explicitly started.
            start_time = self.start()

        return time.time() - start_time


MAX_RUN_TIME = 5  # Seconds.
concur = Concur()
stopwatch = Stopwatch()

print('Running for {} seconds...'.format(MAX_RUN_TIME))
concur.start()
while stopwatch.elapsed_time < MAX_RUN_TIME:
    concur.resume()
    # ... do some concurrent operations.
    concur.pause()
    # Do some other stuff...

# Show Concur thread executed.
