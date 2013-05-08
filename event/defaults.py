"""
Default settings for the ``mezzanine.blog`` app. Each of these can be
overridden in your project's settings module, just like regular
Django settings. The ``editable`` argument for each controls whether
the setting is editable via Django's admin.

Thought should be given to how a setting is actually used before
making it editable, as it may be inappropriate - for example settings
that are only read during startup shouldn't be editable, since changing
them would require an application reload.
"""

from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting


register_setting(
    name="EVENT_USE_FEATURED_IMAGE",
    description=_("Enable featured images in event posts"),
    editable=False,
    default=False,
)

register_setting(
    name="EVENT_URLS_USE_DATE",
    label=_("Use date URLs"),
    description=_("If ``True``, URLs for event post include the month and "
        "year. Eg: /event/yyyy/mm/slug/"),
    editable=False,
    default=False,
)

register_setting(
    name="EVENT_POST_PER_PAGE",
    label=_("Event posts per page"),
    description=_("Number of event posts shown on a event listing page."),
    editable=True,
    default=5,
)

register_setting(
    name="EVENT_RSS_LIMIT",
    label=_("Event posts RSS limit"),
    description=_("Number of most recent event posts shown in the RSS feed. "
        "Set to ``None`` to display all event posts in the RSS feed."),
    editable=False,
    default=20,
)

register_setting(
    name="EVENT_SLUG",
    description=_("Slug of the page object for the event."),
    editable=True,
    default="event",
)