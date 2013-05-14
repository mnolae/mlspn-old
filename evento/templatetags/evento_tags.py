from datetime import datetime

from django.db.models import Count, Q

from evento.forms import EventoPostForm
from evento.models import EventoPost, EventoCategory
from mezzanine.generic.models import Keyword
from mezzanine import template
from mezzanine.utils.models import get_user_model

User = get_user_model()

register = template.Library()


@register.as_tag
def evento_months(*args):
    """
    Put a list of dates for evento posts into the template context.
    """
    dates = EventoPost.objects.published().values_list("publish_date", flat=True)
    date_dicts = [{"date": datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for i, date_dict in enumerate(month_dicts):
        month_dicts[i]["post_count"] = date_dicts.count(date_dict)
    return month_dicts


@register.as_tag
def evento_categories(*args):
    """
    Put a list of categories for evento posts into the template context.
    """
    posts = EventoPost.objects.published()
    categories = EventoCategory.objects.filter(eventoposts__in=posts)
    return list(categories.annotate(post_count=Count("eventoposts")))


@register.as_tag
def evento_authors(*args):
    """
    Put a list of authors (users) for evento posts into the template context.
    """
    evento_posts = EventoPost.objects.published()
    authors = User.objects.filter(eventoposts__in=evento_posts)
    return list(authors.annotate(post_count=Count("eventoposts")))


@register.as_tag
def evento_recent_posts(limit=5, tag=None, username=None, category=None):
    """
    Put a list of recently published evento posts into the template
    context. A tag title or slug, category title or slug or author's
    username can also be specified to filter the recent posts returned.

    Usage::

        {% evento_recent_posts 5 as recent_posts %}
        {% evento_recent_posts limit=5 tag="django" as recent_posts %}
        {% evento_recent_posts limit=5 category="python" as recent_posts %}
        {% evento_recent_posts 5 username=admin as recent_posts %}

    """
    evento_posts = EventoPost.objects.published()
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            evento_posts = evento_posts.filter(keywords__in=tag.assignments.all())
        except Keyword.DoesNotExist:
            return []
    if category is not None:
        try:
            category = EventoCategory.objects.get(title_or_slug(category))
            evento_posts = evento_posts.filter(categories=category)
        except EventoCategory.DoesNotExist:
            return []
    if username is not None:
        try:
            author = User.objects.get(username=username)
            evento_posts = evento_posts.filter(user=author)
        except User.DoesNotExist:
            return []
    return list(evento_posts[:limit])


@register.inclusion_tag("admin/includes/quick_evento.html", takes_context=True)
def quick_evento(context):
    """
    Admin dashboard tag for the quick evento form.
    """
    context["form"] = EventoPostForm()
    return context
