import os
import errno
import logging
import signal


class Downloader(object):
    """Base class used to start external programs to
       download media content"""

    def __init__(self, url, stream):
        self._url = url
        self._stream = stream

    def start(self):
        """Start the external program in a new process"""
        raise NotImplementedError

    def pid(self):
        """Returns the native process identifier
           for the running process"""
        raise NotImplementedError

    def wait_for_finished(self):
        """Blocks until the process has finished"""

        # IMPORTANT: this must be this wait to avoid EINTR
        for pid in self.pid():
            while True:
                try:
                    os.waitpid(pid, 0)
                    break
                except OSError as e:
                    if e.errno == errno.EINTR:
                        continue
                    else:
                        break
        self.cleanup()

    def cleanup(self):
        logging.debug("Cleaning up tmp directories")
        self.do_cleanup()

    def do_cleanup(self):
        pass

    def terminate(self):
        """Attempts to terminate the process."""
        for pid in self.pid():
            if not pid:
                continue
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError as e:
                logging.error("OSError occured: %s" % e)

    def kill(self):
        """Kills the current process,
           causing it to exit immediately."""
        for pid in self.pid():
            if not pid:
                continue
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError as e:
                logging.error("OSError occured: %s" % e)
