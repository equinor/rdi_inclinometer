from _socket import gethostname
from datetime import datetime
from xml.etree import ElementTree


def export_gpx(track_list):
    gpx_root = ElementTree.Element('gpx', version="1.0", creator="MMO")

    track_node = ElementTree.SubElement(gpx_root, 'trk')
    track_seg_node = ElementTree.SubElement(track_node, 'trkseg')

    ElementTree.SubElement(track_node, 'name').text = "MMO Export from {} at {}".format(gethostname(), datetime.utcnow())

    for p in track_list:
        pt = ElementTree.SubElement(track_seg_node, 'trkpt', lat=str(p.lat), lon=str(p.lon))
        ElementTree.SubElement(pt, 'ele').text = str(p.alt)
        ElementTree.SubElement(pt, 'time').text = p.gps_time.isoformat()

    return ElementTree.tostring(gpx_root)