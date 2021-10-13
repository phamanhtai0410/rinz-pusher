import string
from random import random

from bson import ObjectId


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def gen_oid():
    return str(ObjectId())
