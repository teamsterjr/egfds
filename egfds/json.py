from datetime import datetime
import dateutil
from flask.json import JSONEncoder


class DateJSONEncoder(JSONEncoder):

    def default(self, obj):
        from_zone = dateutil.tz.gettz('UTC')
        to_zone = dateutil.tz.gettz('Europe/London')
        try:
            if isinstance(obj, datetime):
                obj=obj.replace(tzinfo=from_zone)
                return obj.replace(tzinfo=from_zone).astimezone(to_zone).strftime("%c")
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return super().default(self, obj)