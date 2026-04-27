"""Default sizer & filter definitions."""
from io import BytesIO

from PIL import Image, ImageOps

from .datastructures import FilteredImage, SizedImage
from .registry import versatileimagefield_registry


try:
    ANTIALIAS = Image.Resampling.LANCZOS
except AttributeError:
    ANTIALIAS = Image.ANTIALIAS  # deprecated in 9.1.0 and removed in 10.0.0


class CroppedImage(SizedImage):
    """
    A SizedImage subclass that creates a 'cropped' image.

    See the `process_image` method for more details.
    """

    filename_key = 'crop'
    filename_key_regex = r'crop-c[0-9-]+__[0-9-]+'

    def get_filename_key(self):
        """Return the filename key for cropped images."""
        pass

    def crop_on_centerpoint(self, image, width, height, ppoi=(0.5, 0.5)):
        """
        Return a PIL Image instance cropped from `image`.

        Image has an aspect ratio provided by dividing `width` / `height`),
        sized down to `width`x`height`. Any 'excess pixels' are trimmed away
        in respect to the pixel of `image` that corresponds to `ppoi` (Primary
        Point of Interest).

        `image`: A PIL Image instance
        `width`: Integer, width of the image to return (in pixels)
        `height`: Integer, height of the image to return (in pixels)
        `ppoi`: A 2-tuple of floats with values greater than 0 and less than 1
                These values are converted into a cartesian coordinate that
                signifies the 'center pixel' which the crop will center on
                (to trim the excess from the 'long side').

        Determines whether to trim away pixels from either the left/right or
        top/bottom sides by comparing the aspect ratio of `image` vs the
        aspect ratio of `width`x`height`.

        Will trim from the left/right sides if the aspect ratio of `image`
        is greater-than-or-equal-to the aspect ratio of `width`x`height`.

        Will trim from the top/bottom sides if the aspect ration of `image`
        is less-than the aspect ratio or `width`x`height`.

        Similar to Kevin Cazabon's ImageOps.fit method but uses the
        ppoi value as an absolute centerpoint (as opposed as a
        percentage to trim off the 'long sides').
        """
        pass

    def process_image(self, image, image_format, save_kwargs,
                      width, height):
        """
        Return a BytesIO instance of `image` cropped to `width` and `height`.

        Cropping will first reduce an image down to its longest side
        and then crop inwards centered on the Primary Point of Interest
        (as specified by `self.ppoi`)
        """
        pass


class ThumbnailImage(SizedImage):
    """
    Sizes an image down to fit within a bounding box.

    See the `process_image()` method for more information
    """

    filename_key = 'thumbnail'

    def process_image(self, image, image_format, save_kwargs,
                      width, height):
        """
        Return a BytesIO instance of `image` that fits in a bounding box.

        Bounding box dimensions are `width`x`height`.
        """
        pass


class InvertImage(FilteredImage):
    """
    Invert the color palette of an image.

    See the `process_image()` for more specifics
    """

    def process_image(self, image, image_format, save_kwargs={}):
        """Return a BytesIO instance of `image` with inverted colors."""
        pass


versatileimagefield_registry.register_sizer('crop', CroppedImage)
versatileimagefield_registry.register_sizer('thumbnail', ThumbnailImage)
versatileimagefield_registry.register_filter('invert', InvertImage)
