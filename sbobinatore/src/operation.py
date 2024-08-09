from time import time
from sys import stdout
from datetime import timedelta


class Operation:
    def __init__(self, name: str = ''):
        """Tracks the time needed to complete an operation. With the "start" method
        the timer starts, when the "stop" method is called the
        timer stops and the elapsed time is returned.

        :param name: name of the operation
        :type name: str
        """
        self.name = name
        self.time = None

    def new(self, name: str = '') -> 'Operation':
        """Reset this object to a new name and returns this object.

        :param name: name of the operation
        :type name: str
        :return: this object
        :rtype: Operation
        """
        self.name = name
        self.time = None
        return self

    def start(self) -> 'Operation':
        """Starts the timer and returns this object.

        :return: this object
        :rtype: Operation
        """
        if self.name:
            stdout.write(self.name + '...')
            stdout.flush()
        self.time = time()
        return self

    def stop(self, precision: int = 2) -> 'Operation':
        """Stops the timer and returns this object.

        :param precision: [Optional] The precision of the float value, default is 2
        :type precision: int
        :return: this object
        :rtype: Operation
        """
        self.time = round(time() - self.time, precision)
        if self.name:
            if self.time < 60:
                print(f'OK ({self.time}s)')
            else:
                print(f'OK ({timedelta(seconds=round(self.time))})')
            print()
        return self
