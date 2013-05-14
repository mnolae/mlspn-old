
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from evento.models import EventoPost, EventoCategory
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin


eventopost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
eventopost_fieldsets[0][1]["fields"].insert(1, "categories")
eventopost_fieldsets[0][1]["fields"].extend(["content", "allow_comments"])
eventopost_list_display = ["title", "user", "status", "admin_link"]
if settings.EVENTO_USE_FEATURED_IMAGE:
    eventopost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    eventopost_list_display.insert(0, "admin_thumb")
eventopost_fieldsets = list(eventopost_fieldsets)
eventopost_fieldsets.insert(1, (_("Other posts"), {
    "classes": ("collapse-closed",),
    "fields": ("related_posts",)}))
eventopost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)


class EventoPostAdmin(DisplayableAdmin, OwnableAdmin):
    """
    Admin class for evento posts.
    """

    fieldsets = eventopost_fieldsets
    list_display = eventopost_list_display
    list_filter = eventopost_list_filter
    filter_horizontal = ("categories", "related_posts",)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class EventoCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for evento categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "evento.EventoCategory" in items:
                return True
        return False


admin.site.register(EventoPost, EventoPostAdmin)
admin.site.register(EventoCategory, EventoCategoryAdmin)
