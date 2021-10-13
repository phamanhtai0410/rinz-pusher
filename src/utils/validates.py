from bson import ObjectId


def is_oid(oid):
    return ObjectId.is_valid(oid)


def is_not_blank(obj):
    if hasattr(obj, 'strip'):
        obj = obj.strip()
    return True if obj else False
