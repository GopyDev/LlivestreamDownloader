#!/usr/bin/env/python

import errno
import os
import sys
import signal
import optparse

from threading import Timer

from ustream import ustreamDownloader
from livestream import livestreamDownloader
from youtube import youtubeDownloader

pyVer = sys.version_info[0]

def sigint_handler(signum, frame):
    downloader.kill()

def sigalrm_handler(signum, frame):
    signal.alarm(0)
    downloader.kill()

def set_stream(msg):
    if pyVer > 2:
        stream = input("%sInput your stream:" %msg)
    else:
        stream = raw_input("%sInput your stream:" %msg)
    return stream

def CreateDownloader(url, out_file):
    if url.startswith("http://www.ustream.tv"):
        return ustreamDownloader(url, out_file)
    elif url.startswith("http://livestream.com"):
        return livestreamDownloader(url, out_file)
    elif url.startswith("https://www.youtube.com") or url.startswith("https://youtu.be"):
        return youtubeDownloader(url, out_file)
    else:
        sys.exit("Ouch!... Unsupported URL.")

if __name__ == '__main__':
    """parser arguments"""
    if (len(sys.argv) < 3):
        exit("Usage: {0} [-s duration] url output_file".format(sys.argv[0]))

    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGALRM, sigalrm_handler)

    # parses options
    parser = optparse.OptionParser(
            usage = 'Usage: %prog [options] url output_file',
            version = '2016.07.12',
            conflict_handler = 'resolve'
            )

    parser.add_option('-s', '--stop', action='store', dest='duration', help='time (in seconds) to run to dump streaming, defaults to 300.')
    (opts, args) = parser.parse_args()
    (init_url, out_file) = args

    """get the available channel"""
    downloader = CreateDownloader(init_url, out_file)
    outmsg, errmsg = downloader.start()
    if errmsg or outmsg.__contains__(b"error"):
        sys.exit(errmsg + outmsg)
    else:
        if pyVer > 2: 
            downloader._stream = set_stream(str(outmsg, "utf-8"))
        else:
            downloader._stream = set_stream(str(outmsg))
    """Start download..."""
    downloader.start()

    if opts.duration:
        dur_secs = int(opts.duration)
    else:
        dur_secs = 300
    signal.alarm(dur_secs)

    downloader.wait_for_finished()




