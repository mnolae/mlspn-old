
from django.conf.urls import patterns, url

from mezzanine.conf import settings

# Leading and trailing slahes for urlpatterns based on setup.
_slashes = (
    "/" if settings.EVENT_SLUG else "",
    "/" if settings.APPEND_SLASH else "",
)

# Blog patterns.
urlpatterns = patterns("event.views",
    url("^%sfeeds/(?P<format>.*)%s$" % _slashes,
        "event_post_feed", name="event_post_feed"),
    url("^%stag/(?P<tag>.*)/feeds/(?P<format>.*)%s$" % _slashes,
        "event_post_feed", name="event_post_feed_tag"),
    url("^%stag/(?P<tag>.*)%s$" % _slashes, "event_post_list",
        name="event_post_list_tag"),
    url("^%scategory/(?P<category>.*)/feeds/(?P<format>.*)%s$" % _slashes,
        "event_post_feed", name="event_post_feed_category"),
    url("^%scategory/(?P<category>.*)%s$" % _slashes,
        "event_post_list", name="event_post_list_category"),
    url("^%sauthor/(?P<username>.*)/feeds/(?P<format>.*)%s$" % _slashes,
        "event_post_feed", name="event_post_feed_author"),
    url("^%sauthor/(?P<username>.*)%s$" % _slashes,
        "event_post_list", name="event_post_list_author"),
    url("^%sarchive/(?P<year>\d{4})/(?P<month>\d{1,2})%s$" % _slashes,
        "event_post_list", name="event_post_list_month"),
    url("^%sarchive/(?P<year>.*)%s$" % _slashes,
        "event_post_list", name="event_post_list_year"),
    url("^%s(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/"
        "(?P<slug>.*)%s$" % _slashes,
        "event_post_detail", name="event_post_detail_date"),
    url("^%s(?P<slug>.*)%s$" % _slashes, "event_post_detail",
        name="event_post_detail"),
    url("^%s$" % _slashes[1], "event_post_list", name="event_post_list"),
)