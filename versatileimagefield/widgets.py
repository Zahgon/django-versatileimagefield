from django.forms.widgets import ClearableFileInput, HiddenInput, MultiWidget, Select
from django.utils.safestring import mark_safe

CENTERPOINT_CHOICES = (
    ('0.0x0.0', 'Top Left'),
    ('0.0x0.5', 'Top Center'),
    ('0.0x1.0', 'Top Right'),
    ('0.5x0.0', 'Middle Left'),
    ('0.5x0.5', 'Middle Center'),
    ('0.5x1.0', 'Middle Right'),
    ('1.0x0.0', 'Bottom Left'),
    ('1.0x0.5', 'Bottom Center'),
    ('1.0x1.0', 'Bottom Right'),
)


class ClearableFileInputWithImagePreview(ClearableFileInput):

    template_name = 'versatileimagefield/forms/widgets/versatile_image.html'

    def get_hidden_field_id(self, name):
        pass

    def image_preview_id(self, name):
        """Given the name of the image preview tag, return the HTML id for it."""
        pass

    def get_ppoi_id(self, name):
        """Given the name of the primary point of interest tag, return the HTML id for it."""
        pass

    def get_point_stage_id(self, name):
        pass

    def get_sized_url(self, value):
        """Do not fail completely on invalid images"""
        pass

    def get_context(self, name, value, attrs):
        """Get the context to render this widget with."""
        pass

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Build an attribute dictionary."""
        pass


class SizedImageCenterpointWidgetMixIn(object):

    def decompress(self, value):
        pass


class VersatileImagePPOISelectWidget(SizedImageCenterpointWidgetMixIn, MultiWidget):

    def __init__(self, widgets=None, attrs=None):
        widgets = [
            ClearableFileInput(attrs=None),
            Select(attrs=attrs, choices=CENTERPOINT_CHOICES)
        ]
        super(VersatileImagePPOISelectWidget, self).__init__(widgets, attrs)


class VersatileImagePPOIClickWidget(SizedImageCenterpointWidgetMixIn, MultiWidget):

    def __init__(self, widgets=None, attrs=None, image_preview_template=None):
        widgets = (
            ClearableFileInputWithImagePreview(attrs={'class': 'file-chooser'}),
            HiddenInput(attrs={'class': 'ppoi-input'})
        )
        super(VersatileImagePPOIClickWidget, self).__init__(widgets, attrs)

    class Media:
        css = {
            'all': ('versatileimagefield/css/versatileimagefield.css',),
        }
        js = ('versatileimagefield/js/versatileimagefield.js',)

    def render(self, name, value, attrs=None, renderer=None):
        pass


class SizedImageCenterpointClickDjangoAdminWidget(VersatileImagePPOIClickWidget):

    class Media:
        css = {
            'all': ('versatileimagefield/css/versatileimagefield-djangoadmin.css',),
        }


class Bootstrap3ClearableFileInputWithImagePreview(ClearableFileInputWithImagePreview):
    """A Bootstrap 3 version of the clearable file input with image preview."""

    template_name = 'versatileimagefield/forms/widgets/versatile_image_bootstrap.html'


class SizedImageCenterpointClickBootstrap3Widget(VersatileImagePPOIClickWidget):

    def __init__(self, widgets=None, attrs=None):
        widgets = (
            Bootstrap3ClearableFileInputWithImagePreview(attrs={'class': 'file-chooser'}),
            HiddenInput(attrs={'class': 'ppoi-input'})
        )
        super(VersatileImagePPOIClickWidget, self).__init__(widgets, attrs)

    class Media:
        css = {
            'all': ('versatileimagefield/css/versatileimagefield-bootstrap3.css',),
        }
