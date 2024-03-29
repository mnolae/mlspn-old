from datetime import datetime

from django.db.models import Count, Q

from .forms import EventPostForm
from .models import EventPost, EventCategory
from mezzanine.generic.models import Keyword
from mezzanine import template
from mezzanine.utils.models import get_user_model

User = get_user_model()

register = template.Library()


@register.as_tag
def event_months(*args):
    """
    Put a list of dates for blog posts into the template context.
    """
    dates = EventPost.objects.published().values_list("publish_date", flat=True)
    date_dicts = [{"date": datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for i, date_dict in enumerate(month_dicts):
        month_dicts[i]["post_count"] = date_dicts.count(date_dict)
    return month_dicts


@register.as_tag
def event_categories(*args):
    """
    Put a list of categories for blog posts into the template context.
    """
    posts = EventPost.objects.published()
    categories = EventCategory.objects.filter(eventposts__in=posts)
    return list(categories.annotate(post_count=Count("eventposts")))


@register.as_tag
def event_authors(*args):
    """
    Put a list of authors (users) for blog posts into the template context.
    """
    event_posts = EventPost.objects.published()
    authors = User.objects.filter(eventposts__in=event_posts)
    return list(authors.annotate(post_count=Count("eventposts")))


@register.as_tag
def event_recent_posts(limit=5, tag=None, username=None, category=None):
    """
    Put a list of recently published blog posts into the template
    context. A tag title or slug, category title or slug or author's
    username can also be specified to filter the recent posts returned.

    Usage::

        {% blog_recent_posts 5 as recent_posts %}
        {% blog_recent_posts limit=5 tag="django" as recent_posts %}
        {% blog_recent_posts limit=5 category="python" as recent_posts %}
        {% blog_recent_posts 5 username=admin as recent_posts %}

    """
    event_posts = EventPost.objects.published()
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            event_posts = event_posts.filter(keywords__in=tag.assignments.all())
        except Keyword.DoesNotExist:
            return []
    if category is not None:
        try:
            category = EventCategory.objects.get(title_or_slug(category))
            event_posts = event_posts.filter(categories=category)
        except EventCategory.DoesNotExist:
            return []
    if username is not None:
        try:
            author = User.objects.get(username=username)
            event_posts = event_posts.filter(user=author)
        except User.DoesNotExist:
            return []
    return list(event_posts[:limit])


@register.inclusion_tag("admin/includes/quick_event.html", takes_context=True)
def quick_event(context):
    """
    Admin dashboard tag for the quick blog form.
    """
    context["form"] = EventPostForm()
    return context
