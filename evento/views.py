from calendar import month_name

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404

from evento.models import EventoPost, EventoCategory
from evento.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import render, paginate
from mezzanine.utils.models import get_user_model

User = get_user_model()

def evento_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="evento/evento_post_list.html"):
    """
    Display a list of evento posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``evento/evento_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    settings.use_editable()
    templates = []
    evento_posts = EventoPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        evento_posts = evento_posts.filter(keywords__in=tag.assignments.all())
    if year is not None:
        evento_posts = evento_posts.filter(publish_date__year=year)
        if month is not None:
            evento_posts = evento_posts.filter(publish_date__month=month)
            month = month_name[int(month)]
    if category is not None:
        category = get_object_or_404(EventoCategory, slug=category)
        evento_posts = evento_posts.filter(categories=category)
        templates.append(u"evento/evento_post_list_%s.html" %
                          unicode(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        evento_posts = evento_posts.filter(user=author)
        templates.append(u"evento/evento_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    evento_posts = evento_posts.select_related("user").prefetch_related(*prefetch)
    evento_posts = paginate(evento_posts, request.GET.get("page", 1),
                          settings.EVENTO_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"evento_posts": evento_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    templates.append(template)
    return render(request, templates, context)


def evento_post_detail(request, slug, year=None, month=None, day=None,
                     template="evento/evento_post_detail.html"):
    """. Custom templates are checked for using the name
    ``evento/evento_post_detail_XXX.html`` where ``XXX`` is the evento
    posts's slug.
    """
    evento_posts = EventoPost.objects.published(
                                     for_user=request.user).select_related()
    evento_post = get_object_or_404(evento_posts, slug=slug)
    context = {"evento_post": evento_post, "editable_obj": evento_post}
    templates = [u"evento/evento_post_detail_%s.html" % unicode(slug), template]
    return render(request, templates, context)


def evento_post_feed(request, format, **kwargs):
    """
    Evento posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()
