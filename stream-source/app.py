import sys
import gi
from urllib.request import urlopen

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

loop = GObject.MainLoop()
GObject.threads_init()
Gst.init(None)

tagesschau24 = 'http://tagesschau-lh.akamaihd.net/i/tagesschau_1@119231/index_384_av-p.m3u8?sd=10&rebase=on'
arte = 'http://artelive-lh.akamaihd.net/i/artelive_de@393591/index_3_av-p.m3u8?sd=10&rebase=on'
n24 = 'http://p.live.akamai.n-tv.de/hls-live/ntvlive/ntvlive_1500.m3u8'
zdf = 'https://zdf1314-lh.akamaihd.net/i/de14_v1@392878/index_776_av-b.m3u8?sd=10&rebase=on&id='

class MyFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        return Gst.parse_launch('( uridecodebin uri={} ! video/x-raw ! clockoverlay text=Departure: valignment=top halignment=left font-desc="Sans, 11" ! videoconvert ! x264enc ! rtph264pay name=pay0 pt=96 )'.format(arte))


class GstServer():
    def __init__(self):
        self.server = GstRtspServer.RTSPServer()
        f = MyFactory()
        f.set_shared(True)
        m = self.server.get_mount_points()
        m.add_factory("/stream", f)
        self.server.set_service('6000')
        self.server.attach(None)

s = GstServer()
loop.run()
