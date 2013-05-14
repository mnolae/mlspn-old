from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to


class EventoPost(Displayable, Ownable, RichText, AdminThumbMixin):
    """
    A evento post.
    """

    categories = models.ManyToManyField("EventoCategory",
                                        verbose_name=_("Categories"),
                                        blank=True, related_name="eventoposts")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    comments = CommentsField(verbose_name=_("Comments"))
    rating = RatingField(verbose_name=_("Rating"))
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("evento.EventoPost.featured_image", "evento"),
        format="Image", max_length=255, null=True, blank=True)
    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related posts"), blank=True)

    admin_thumb_field = "featured_image"

    class Meta:
        verbose_name = _("Evento post")
        verbose_name_plural = _("Evento posts")
        ordering = ("-publish_date",)

    @models.permalink
    def get_absolute_url(self):
        url_name = "evento_post_detail"
        kwargs = {"slug": self.slug}
        if settings.EVENTO_URLS_USE_DATE:
            url_name = "evento_post_detail_date"
            month = str(self.publish_date.month)
            if len(month) == 1:
                month = "0" + month
            day = str(self.publish_date.day)
            if len(day) == 1:
                day = "0" + day
            kwargs.update({
                "day": day,
                "month": month,
                "year": self.publish_date.year,
            })
        return (url_name, (), kwargs)

    # These methods are deprecated wrappers for keyword and category
    # access. They existed to support Django 1.3 with prefetch_related
    # not existing, which was therefore manually implemented in the
    # evento list views. All this is gone now, but the access methods
    # still exist for older templates.

    def category_list(self):
        from warnings import warn
        warn("evento_post.category_list in templates is deprecated"
             "use evento_post.categories.all which are prefetched")
        return getattr(self, "_categories", self.categories.all())

    def keyword_list(self):
        from warnings import warn
        warn("evento_post.keyword_list in templates is deprecated"
             "use the keywords_for template tag, as keywords are prefetched")
        try:
            return self._keywords
        except AttributeError:
            keywords = [k.keyword for k in self.keywords.all()]
            setattr(self, "_keywords", keywords)
            return self._keywords


class EventoCategory(Slugged):
    """
    A category for grouping evento posts into a series.
    """

    class Meta:
        verbose_name = _("Evento Category")
        verbose_name_plural = _("Evento Categories")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return ("evento_post_list_category", (), {"category": self.slug})
