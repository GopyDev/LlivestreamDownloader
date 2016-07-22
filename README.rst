
Livestream Downloader
==============
This is tool to download the video or audio from livestream in python.


Development
============
    customized the livestreamer library
    create the ustream download in python
    create the livestream download in python
    create the youtube download in python

Environment
============
    Ubuntu 12.04, 14.04 desktop 64bit, Python 2.7 or 3.x

Installation
============

Install livestreamer

.. Use virtualenv.

    pip install -U git+https://github.com/chrippa/livestreamer.git
    (Note. livestraemer requires python-librtmp)

To overwrite ustreamtv.py that is customized.(livestreamer-modified/ustreamtv.py)

Run our main.py.

    python main.py -s 600 http://www.ustream.tv/channel/orocoipo out.mp4
    (Note. in the case that '-s' is not given, default value 300 is applied.)
