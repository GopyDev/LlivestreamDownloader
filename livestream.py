import sys
import os
import errno
import logging
import signal
import subprocess
import shlex

from base import Downloader

RUN_PROG = "livestreamer"

def full_path(name):
    for path in os.getenv("PATH").split(os.path.pathsep):
        full_path = path + os.sep + name
        if os.path.exists(full_path):
            return full_path

class livestreamDownloader(Downloader):
    """Derived class used to start external programs to
       download media ustream content"""

    def __init__(self, url, outfile):
        self._url = url
        self._stream = None
        self.outfile = outfile

    def create_arguments(self):
        args = shlex.split(sys.executable) + shlex.split(full_path(RUN_PROG))
        if not self._stream:
            args = args + shlex.split(self._url)
        else:
            args = args + shlex.split("-o %s" %self.outfile) + shlex.split(self._url) + shlex.split("%s" %self._stream)
        return args

    def start(self):
        """Start the external program in a new process"""
        if not self._stream:
            self.proc = subprocess.Popen(self.create_arguments(), bufsize = 0, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            self.out, self.err = self.proc.communicate()
            return self.out, self.err
        else:
            self.proc = subprocess.Popen(self.create_arguments(), bufsize = 0 )
        self.pid = self.proc.pid

        return

    def pid(self):
        """Returns the native process identifier
           for the running process"""
        return self.pid

    def wait_for_finished(self):
        """Blocks until the process has finished"""
        self.proc.wait()
        # IMPORTANT: this must be this wait to avoid EINTR
        """
        for pid in self.pid():
            while True:
                try:
                    os.waitpid(pid, 0)
                    break
                except OSError, e:
                    if e.errno == errno.EINTR:
                        continue
                    else:
                        break
        """
        self.cleanup()

    def cleanup(self):
        logging.debug("Cleaning up tmp directories")
        self.do_cleanup()

    def do_cleanup(self):
        pass

    def terminate(self):
        """Attempts to terminate the process."""
        try:
            self.proc.terminate()
        except:
            pass
        """
        for pid in self.pid():
            if not pid:
                continue
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError, e:
                logging.error("OSError occured: %s" % e)
        """

    def kill(self):
        """Kills the current process,
           causing it to exit immediately."""
        try:
            self.proc.kill()
        except:
            pass
        """
        for pid in self.pid():
            if not pid:
                continue
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError, e:
                logging.error("OSError occured: %s" % e)
        """