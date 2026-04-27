"""Base datastructures for manipulated images."""
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile

from ..settings import (
    JPEG_QUAL,
    VERSATILEIMAGEFIELD_PROGRESSIVE_JPEG,
    VERSATILEIMAGEFIELD_LOSSLESS_WEBP,
    WEBP_QUAL,
)
from ..utils import get_image_metadata_from_file

EXIF_ORIENTATION_KEY = 274


class ProcessedImage(object):
    """
    A base class for processing/saving different renditions of an image.

    Constructor arguments:
        * `path_to_image`: A path to a file within `storage`
        * `storage`: A django storage class
        * `create_on_demand`: A bool signifying whether new images should be
                              created on-demand.

    Subclasses must define the `process_image` method. see
    versatileimagefield.datastructures.filteredimage.FilteredImage and
    versatileimagefield.datastructures.sizedimage.SizedImage
    for examples.

    Includes a preprocessing API based on image format/file type. See
    the `preprocess` method for more specific information.
    """

    name = None
    url = None

    def __init__(self, path_to_image, storage, create_on_demand,
                 placeholder_image=None):
        """Construct a ProcessedImage."""
        self.path_to_image = path_to_image
        self.storage = storage
        self.create_on_demand = create_on_demand
        self.placeholder_image = placeholder_image

    def process_image(self, image, image_format, **kwargs):
        """
        Ensure NotImplemented is raised if not overloaded by subclasses.

        Arguments:
            * `image`: a PIL Image instance
            * `image_format`: str, a valid PIL format (i.e. 'JPEG' or 'GIF')

        Returns a BytesIO representation of the resized image.

        Subclasses MUST implement this method.
        """
        raise NotImplementedError(
            'Subclasses MUST provide a `process_image` method.'
        )

    def preprocess(self, image, image_format):
        """
        Preprocess an image.

        An API hook for image pre-processing. Calls any image format specific
        pre-processors (if defined). I.E. If `image_format` is 'JPEG', this
        method will look for a method named `preprocess_JPEG`, if found
        `image` will be passed to it.

        Arguments:
            * `image`: a PIL Image instance
            * `image_format`: str, a valid PIL format (i.e. 'JPEG' or 'GIF')

        Subclasses should return a 2-tuple:
            * [0]: A PIL Image instance.
            * [1]: A dictionary of additional keyword arguments to be used
                   when the instance is saved. If no additional keyword
                   arguments, return an empty dict ({}).
        """
        pass

    def preprocess_GIF(self, image, **kwargs):
        """
        Receive a PIL Image instance of a GIF and return 2-tuple.

        Args:
            * [0]: Original Image instance (passed to `image`)
            * [1]: Dict with a transparency key (to GIF transparency layer)
        """
        pass

    def preprocess_JPEG(self, image, **kwargs):
        """
        Receive a PIL Image instance of a JPEG and returns 2-tuple.

        Args:
            * [0]: Image instance, converted to RGB
            * [1]: Dict with a quality key (mapped to the value of `JPEG_QUAL`
                   defined by the `VERSATILEIMAGEFIELD_JPEG_RESIZE_QUALITY`
                   setting)
        """
        pass

    def preprocess_WEBP(self, image, **kwargs):
        """
        Receive a PIL Image instance of a WEBP and return 2-tuple.

        Args:
            * [0]: Original Image instance (passed to `image`)
            * [1]: Dict with a quality key (mapped to the value of `WEBP_QUAL`
                   as defined by the `VERSATILEIMAGEFIELD_RESIZE_QUALITY`
                   setting)
        """
        pass

    def retrieve_image(self, path_to_image):
        """Return a PIL Image instance stored at `path_to_image`."""
        pass

    def save_image(self, imagefile, save_path, file_ext, mime_type):
        """
        Save an image to self.storage at `save_path`.

        Arguments:
            `imagefile`: Raw image data, typically a BytesIO instance.
            `save_path`: The path within self.storage where the image should
                         be saved.
            `file_ext`: The file extension of the image-to-be-saved.
            `mime_type`: A valid image mime type (as found in
                         versatileimagefield.utils)
        """
        pass
