"""versatileimagefield Field mixins."""
import os
import re

from .datastructures import FilterLibrary
from .registry import autodiscover, versatileimagefield_registry
from .settings import (
    cache,
    VERSATILEIMAGEFIELD_CREATE_ON_DEMAND,
    VERSATILEIMAGEFIELD_SIZED_DIRNAME,
    VERSATILEIMAGEFIELD_FILTERED_DIRNAME
)
from .validators import validate_ppoi

autodiscover()

filter_regex_snippet = r'__({registered_filters})__'.format(
    registered_filters='|'.join([
        key
        for key, filter_cls in versatileimagefield_registry._filter_registry.items()
    ])
)
sizer_regex_snippet = r'-({registered_sizers})-(\d+)x(\d+)(?:-\d+)?'.format(
    registered_sizers='|'.join([
        sizer_cls.get_filename_key_regex()
        for key, sizer_cls in versatileimagefield_registry._sizedimage_registry.items()
    ])
)
filter_regex = re.compile(filter_regex_snippet + '$')
sizer_regex = re.compile(sizer_regex_snippet + '$')
filter_and_sizer_regex = re.compile(
    filter_regex_snippet + sizer_regex_snippet + '$'
)


class VersatileImageMixIn(object):
    """A mix-in that provides the filtering/sizing API."""

    def __init__(self, *args, **kwargs):
        """Construct PPOI and create_on_demand."""
        self._create_on_demand = VERSATILEIMAGEFIELD_CREATE_ON_DEMAND
        super(VersatileImageMixIn, self).__init__(*args, **kwargs)
        self._ppoi_value = (0.5, 0.5)
        # Setting initial ppoi
        if self.field.ppoi_field:
            instance_ppoi_value = getattr(
                self.instance,
                self.field.ppoi_field,
                (0.5, 0.5)
            )
            self.ppoi = instance_ppoi_value

    @property
    def url(self):
        """
        Return the appropriate URL.

        URL is constructed based on these field conditions:
            * If empty (not `self.name`) and a placeholder is defined, the
              URL to the placeholder is returned.
            * Otherwise, defaults to vanilla ImageFieldFile behavior.
        """
        pass

    @property
    def create_on_demand(self):
        """create_on_demand getter."""
        pass

    @create_on_demand.setter
    def create_on_demand(self, value):
        pass

    @property
    def ppoi(self):
        """Primary Point of Interest (ppoi) getter."""
        pass

    @ppoi.setter
    def ppoi(self, value):
        """Primary Point of Interest (ppoi) setter."""
        pass

    def build_filters_and_sizers(self, ppoi_value, create_on_demand):
        """Build the filters and sizers for a field."""
        pass

    def get_filtered_root_folder(self):
        """Return the location where filtered images are stored."""
        pass

    def get_sized_root_folder(self):
        """Return the location where sized images are stored."""
        pass

    def get_filtered_sized_root_folder(self):
        """Return the location where filtered + sized images are stored."""
        pass

    def delete_matching_files_from_storage(self, root_folder, regex):
        """
        Delete files in `root_folder` which match `regex` before file ext.

        Example values:
            * root_folder = 'foo/'
            * self.name = 'bar.jpg'
            * regex = re.compile('-baz')

            Result:
                * foo/bar-baz.jpg <- Deleted
                * foo/bar-biz.jpg <- Not deleted
        """
        pass

    def delete_filtered_images(self):
        """Delete all filtered images created from `self.name`."""
        pass

    def delete_sized_images(self):
        """Delete all sized images created from `self.name`."""
        pass

    def delete_filtered_sized_images(self):
        """Delete all filtered sized images created from `self.name`."""
        pass

    def delete_all_created_images(self):
        """Delete all images created from `self.name`."""
        pass
