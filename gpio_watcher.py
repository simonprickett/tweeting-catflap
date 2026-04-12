from gpiozero import Button
from signal import pause
import time


class GPIOWatcher(object):

    def __init__(self, headerNo, onChange=None, debounceSeconds=2):
        """
        headerNo - the physical pin number of the GPIO header
        onChange - a function called when the button is pressed
        debounceSeconds - don't fire a press event if one has been fired within this time
        """
        self.onChange = onChange
        self.debounceSeconds = debounceSeconds
        self.lastEventTime = 0
        self.button = Button("BOARD%d" % headerNo)
        self.button.when_pressed = self._on_press

    def _on_press(self):
        timeNow = time.time()
        if timeNow > self.lastEventTime + self.debounceSeconds:
            self.lastEventTime = timeNow
            if self.onChange:
                try:
                    self.onChange()
                except Exception as e:
                    print(f"Error in onChange callback: {e}")

    def enter_loop(self):
        """Block forever, waiting for button presses"""
        pause()


if __name__ == "__main__":
    def printMessage():
        print("Change detected!")
    watcher = GPIOWatcher(7, onChange=printMessage)
    watcher.enter_loop()
