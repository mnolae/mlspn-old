"""
Default settings for the ``mezzanine.evento`` app. Each of these can be
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
    name="EVENTO_USE_FEATURED_IMAGE",
    description=_("Enable featured images in evento posts"),
    editable=False,
    default=False,
)

register_setting(
    name="EVENTO_URLS_USE_DATE",
    label=_("Use date URLs"),
    description=_("If ``True``, URLs for evento post include the month and "
        "year. Eg: /evento/yyyy/mm/slug/"),
    editable=False,
    default=False,
)

register_setting(
    name="EVENTO_POST_PER_PAGE",
    label=_("Evento posts per page"),
    description=_("Number of evento posts shown on a evento listing page."),
    editable=True,
    default=5,
)

register_setting(
    name="EVENTO_RSS_LIMIT",
    label=_("Evento posts RSS limit"),
    description=_("Number of most recent evento posts shown in the RSS feed. "
        "Set to ``None`` to display all evento posts in the RSS feed."),
    editable=False,
    default=20,
)

register_setting(
    name="EVENTO_SLUG",
    description=_("Slug of the page object for the evento."),
    editable=False,
    default="evento",
)
