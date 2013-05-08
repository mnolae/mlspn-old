from calendar import month_name

from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import EventPost, EventCategory
from event.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import render, paginate
from mezzanine.utils.models import get_user_model

User = get_user_model()


def event_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="event/event_post_list.html"):
    """
    Display a list of event posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``event/event_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    settings.use_editable()
    templates = []
    event_posts = EventPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        event_posts = event_posts.filter(keywords__in=tag.assignments.all())
    if year is not None:
        event_posts = event_posts.filter(publish_date__year=year)
        if month is not None:
            event_posts = event_posts.filter(publish_date__month=month)
            month = month_name[int(month)]
    if category is not None:
        category = get_object_or_404(EventCategory, slug=category)
        event_posts = event_posts.filter(categories=category)
        templates.append(u"event/event_post_list_%s.html" %
                          unicode(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        event_posts = event_posts.filter(user=author)
        templates.append(u"event/event_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    event_posts = event_posts.select_related("user").prefetch_related(*prefetch)
    event_posts = paginate(event_posts, request.GET.get("page", 1),
                          settings.EVENT_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"event_posts": event_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    templates.append(template)
    return render(request, templates, context)


def event_post_detail(request, slug, year=None, month=None, day=None,
                     template="event/event_post_detail.html"):
    """. Custom templates are checked for using the name
    ``event/event_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    event_posts = EventPost.objects.published(
                                     for_user=request.user).select_related()
    event_post = get_object_or_404(event_posts, slug=slug)
    context = {"event_post": event_post, "editable_obj": event_post}
    templates = [u"event/event_post_detail_%s.html" % unicode(slug), template]
    return render(request, templates, context)


def event_post_feed(request, format, **kwargs):
    """
    Event posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()