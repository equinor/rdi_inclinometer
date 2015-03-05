import simplejson
import datetime


def json_serial(obj):
    """Default JSON serializer."""

    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial


def dump_as_json(list_of_dicts):
    return simplejson.dumps(list_of_dicts, default=json_serial)
