import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

empty = object()


class PlaceholderImage(object):
    """
    A class for configuring images to be used as 'placeholders' for
    blank/empty VersatileImageField fields.
    """

    _image_data = empty

    def setup(self):
        pass

    @property
    def image_data(self):
        pass


class OnDiscPlaceholderImage(PlaceholderImage):
    """
    A placeholder image saved to the same disc as the running
    application.
    """

    def __init__(self, path):
        """
        `path` - An absolute path to an on-disc image.
        """
        self.path = path

    def setup(self):
        pass


class OnStoragePlaceholderImage(PlaceholderImage):
    """
    A placeholder saved to a storage class. Does not necessarily need to
    be on the same storage as the field it is associated with.
    """

    def __init__(self, path, storage=None):
        """
        `path` - A path on `storage` to an Image.
        `storage` - A django storage class.
        """
        self.path = path
        self.storage = storage

    def setup(self):
        pass
