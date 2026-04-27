from django.forms.fields import MultiValueField, CharField, ImageField

from .widgets import (
    SizedImageCenterpointClickDjangoAdminWidget, SizedImageCenterpointClickBootstrap3Widget,
    VersatileImagePPOIClickWidget
)


class SizedImageCenterpointMixIn(object):

    def compress(self, data_list):
        pass


class VersatileImageFormField(ImageField):

    def to_python(self, data):
        """Ensure data is prepped properly before handing off to ImageField."""
        pass


class VersatileImagePPOIClickField(SizedImageCenterpointMixIn, MultiValueField):

    widget = VersatileImagePPOIClickWidget

    def __init__(self, *args, **kwargs):
        max_length = kwargs.pop('max_length', None)
        del max_length
        fields = (
            VersatileImageFormField(label='Image'),
            CharField(required=False)
        )
        super(VersatileImagePPOIClickField, self).__init__(
            tuple(fields), *args, **kwargs
        )

    def bound_data(self, data, initial):
        pass


class SizedImageCenterpointClickDjangoAdminField(VersatileImagePPOIClickField):

    widget = SizedImageCenterpointClickDjangoAdminWidget
    # Need to remove `None` and `u''` so required fields will work
    # TODO: Better validation handling
    empty_values = [[], (), {}]


class SizedImageCenterpointClickBootstrap3Field(SizedImageCenterpointClickDjangoAdminField):

    widget = SizedImageCenterpointClickBootstrap3Widget
