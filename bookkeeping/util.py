from datetime import date, datetime
from decimal import *
import json


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return str(obj)

    raise TypeError("Type %s not serializable" % type(obj))


def to_json(data):
    if isinstance(data, list):
        # 多条数据
        res = {
            "data": {
                "results": data,
                "total": len(data)
            }
        }
    res.update({"_remark": "data from db"})
    return json.dumps(res, default=json_serial, ensure_ascii=False)

