from django.contrib import admin
from django.db.models import Sum
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
    save_on_top = True
    exclude = ('deleted_at',)
    inlines = [ImageInline]


def delete_views(modelAdmin, request, queryset):
    for image in queryset:
        image.views.all().delete()


delete_views.short_description = 'Delete image views'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    exclude = ('deleted_at',)
    fields = ['title', 'image', 'pack', get_image_preview, 'get_views']
    readonly_fields = [get_image_preview, 'get_views']
    list_display = ('pk', '__str__', 'get_views', 'last_viewed')
    actions = [delete_views, ]

    def last_viewed(self, obj=None):
        if obj is None:
            return
        last_view = obj.views.order_by('-viewed_at').first()
        if last_view:
            return last_view.viewed_at

    def get_views(self, obj=None):
        if obj is None:
            return 0
        return obj.views.aggregate(Sum('count'))['count__sum'] or 0

    get_views.short_description = "Number of views"

