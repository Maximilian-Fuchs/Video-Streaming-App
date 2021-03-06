import sys
import gi
import dns.resolver
import time

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

def hostname_resolves(hostname):
    try:
        dns.resolver.Resolver().query(hostname, 'A')
        return True
    except dns.resolver.NXDOMAIN:
        return False

hostname = 'stream-smoothen'
while not hostname_resolves(hostname):
    time.sleep(3)
source_address = dns.resolver.Resolver().query(hostname, 'A')[0]
source_uri = 'rtsp://{}:6003/stream'.format(source_address)

loop = GObject.MainLoop()
GObject.threads_init()
Gst.init(None)

class MyFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        return Gst.parse_launch('( uridecodebin uri={} ! video/x-raw ! videoconvert ! clockoverlay text=Arrival: valignment=bottom halignment=left font-desc="Sans, 11" ! videoconvert ! x264enc ! rtph264pay name=pay0 pt=96 )'.format(source_uri))


class GstServer():
    def __init__(self):
        self.server = GstRtspServer.RTSPServer()
        f = MyFactory()
        f.set_shared(True)
        m = self.server.get_mount_points()
        m.add_factory("/stream", f)
        self.server.set_service('6004')
        self.server.attach(None)

s = GstServer()
loop.run()
