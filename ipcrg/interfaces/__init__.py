"""Initilize interfaces module."""
from .mongo import MongoDBInterface

INTERFACE_FACTORY = {
    'mongo': MongoDBInterface
}