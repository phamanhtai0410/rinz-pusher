from bson import ObjectId


def is_oid(oid):
    return ObjectId.is_valid(oid)


def is_not_blank(obj):
    if hasattr(obj, 'strip'):
        obj = obj.strip()
    return True if obj else False


def is_oid_or_all(obj):
    if is_oid(obj):
        return True
    if obj == '*':
        return True
    return False
