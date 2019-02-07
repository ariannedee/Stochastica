from django.contrib import admin
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html

from .models import Pack, Image


def get_image_preview(obj):
    if obj.pk:  # if object has already been saved and has a primary key, show picture preview
        return format_html('<img src="{src}" alt="{title}" style="max-width: 150px; max-height: 150px;" />',
                           src=obj.image.url,
                           title=obj.title,
                           )
    return "Choose a picture and save and continue editing to see the preview"


get_image_preview.allow_tags = True
get_image_preview.short_description = 'Image preview'


class ImageInline(admin.StackedInline):
    model = Image
    exclude = ('viewed_by', 'deleted_at')
    fields = ['title', 'image', 'get_edit_link', get_image_preview]
    readonly_fields = ['get_edit_link', get_image_preview]
    extra = 0

    def get_edit_link(self, obj=None):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            return format_html('<a href="{url}">{text}</a>',
                               url=url,
                               text=f'Edit this {obj._meta.verbose_name}',
                               )
        return "Save and continue editing to create a link"

    get_edit_link.short_description = "Edit link"
    get_edit_link.allow_tags = True


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    exclude = ('deleted_at',)
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    exclude = ('deleted_at',)
    fields = ['title', 'image', 'pack', get_image_preview]
    readonly_fields = [get_image_preview]
