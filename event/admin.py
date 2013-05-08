
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import EventPost, EventCategory
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin


eventpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
eventpost_fieldsets[0][1]["fields"].insert(1, "categories")
eventpost_fieldsets[0][1]["fields"].extend(["content", "allow_comments"])
eventpost_list_display = ["title", "user", "status", "admin_link"]
if settings.EVENT_USE_FEATURED_IMAGE:
    eventpost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    eventpost_list_display.insert(0, "admin_thumb")
eventpost_fieldsets = list(eventpost_fieldsets)
eventpost_fieldsets.insert(1, (_("Other posts"), {
    "classes": ("collapse-closed",),
    "fields": ("related_posts",)}))
eventpost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)


class EventPostAdmin(DisplayableAdmin, OwnableAdmin):
    """
    Admin class for event posts.
    """

    fieldsets = eventpost_fieldsets
    list_display = eventpost_list_display
    list_filter = eventpost_list_filter
    filter_horizontal = ("categories", "related_posts",)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class EventCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for event categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "event.EventCategory" in items:
                return True
        return False


admin.site.register(EventPost, EventPostAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
