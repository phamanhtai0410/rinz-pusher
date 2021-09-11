from bson import ObjectId


def is_oid(oid):
    return ObjectId.is_valid(oid)
