"""Fields."""
import os

from django.contrib.admin.widgets import AdminFileWidget
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.utils.translation import gettext_lazy as _

from .files import VersatileImageFieldFile, VersatileImageFileDescriptor
from .forms import SizedImageCenterpointClickDjangoAdminField
from .placeholder import OnStoragePlaceholderImage
from .settings import VERSATILEIMAGEFIELD_PLACEHOLDER_DIRNAME
from .validators import validate_ppoi


class Creator(object):
    """Provides a way to set the attribute on the model."""

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, objtype=None):
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class VersatileImageField(ImageField):
    """Extends ImageField."""

    attr_class = VersatileImageFieldFile
    descriptor_class = VersatileImageFileDescriptor
    description = _('Versatile Image Field')

    def __init__(self, verbose_name=None, name=None, width_field=None,
                 height_field=None, ppoi_field=None, placeholder_image=None,
                 **kwargs):
        """Initialize an instance."""
        self.ppoi_field = ppoi_field
        super(VersatileImageField, self).__init__(
            verbose_name, name, width_field, height_field, **kwargs
        )
        self.placeholder_image = placeholder_image
        self.placeholder_image_name = None

    def process_placeholder_image(self):
        """
        Process the field's placeholder image.

        Ensures the placeholder image has been saved to the same storage class
        as the field in a top level folder with a name specified by
        settings.VERSATILEIMAGEFIELD_SETTINGS['placeholder_directory_name']

        This should be called by the VersatileImageFileDescriptor __get__.
        If self.placeholder_image_name is already set it just returns right away.
        """
        pass

    def pre_save(self, model_instance, add):
        """Return field's value just before saving."""
        pass

    def update_ppoi_field(self, instance, *args, **kwargs):
        """
        Update field's ppoi field, if defined.

        This method is hooked up this field's pre_save method to update
        the ppoi immediately before the model instance (`instance`)
        it is associated with is saved.

        This field's ppoi can be forced to update with force=True,
        which is how VersatileImageField.pre_save calls this method.
        """
        pass

    def save_form_data(self, instance, data):
        """
        Handle data sent from MultiValueField forms that set ppoi values.

        `instance`: The model instance that is being altered via a form
        `data`: The data sent from the form to this field which can be either:
        * `None`: This is unset data from an optional field
        * A two-position tuple: (image_form_data, ppoi_data)
            * `image_form-data` options:
                * `None` the file for this field is unchanged
                * `False` unassign the file form the field
            * `ppoi_data` data structure:
                * `%(x_coordinate)sx%(y_coordinate)s': The ppoi data to
                  assign to the unchanged file

        """
        pass

    def formfield(self, **kwargs):
        """Return a formfield."""
        pass


class PPOIField(CharField):

    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = '0.5x0.5'
        kwargs['default'] = self.get_prep_value(
            value=validate_ppoi(
                kwargs['default'],
                return_converted_tuple=True
            )
        )
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 20
        # Forcing editable = False since PPOI values are set directly on
        # VersatileImageField.
        kwargs['editable'] = False
        super(PPOIField, self).__init__(*args, **kwargs)
        self.validators.append(validate_ppoi)

    def contribute_to_class(self, cls, name, **kwargs):
        pass

    def from_db_value(self, value, *args, **kwargs):
        pass

    def to_python(self, value):
        pass

    def get_prep_value(self, value):
        pass

    def value_to_string(self, obj):
        """Prepare field for serialization."""
        pass


__all__ = ['VersatileImageField', 'PPOIField']
