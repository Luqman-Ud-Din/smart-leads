import urllib

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class SearchTerm(models.Model):
    text = models.CharField(_('text'), max_length=2048)
    slug = models.SlugField(_('slug'), max_length=2048, unique=True)

    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.text

    @property
    def encoded_text(self):
        return urllib.parse.quote(self.text)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.text)
        super(SearchTerm, self).save(*args, **kwargs)
