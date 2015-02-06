import simplejson
import datetime

def json_serial(obj):
    """Default JSON serializer."""

    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial


def dump_as_json(a_dict):
    return simplejson.dumps(a_dict, default=json_serial)
