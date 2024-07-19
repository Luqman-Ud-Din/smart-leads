from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Job(models.Model):
    FIXED = 'fixed'
    HOURLY = 'hourly'
    HOURLY_RANGE = 'hourly_range'
    NOT_SPECIFIED = 'not_specified'

    BUDGET_TYPE_CHOICES = [
        (FIXED, 'Fixed'),
        (HOURLY, 'Hourly'),
        (HOURLY_RANGE, 'Hourly Range'),
        (NOT_SPECIFIED, 'Not Specified'),
    ]

    job_id = models.CharField(
        _('job id'),
        max_length=4000,
        unique=True
    )
    url = models.CharField(_('url'), max_length=4000)
    published_date = models.DateTimeField(_('published date'))
    description = models.TextField(
        _('description'),
        default=''
    )

    budget_type = models.CharField(
        _('budget type'),
        max_length=50,
        choices=BUDGET_TYPE_CHOICES,
        default=NOT_SPECIFIED
    )
    budget_amount = models.FloatField(
        _('budget amount'),
        blank=True,
        null=True
    )
    budget_min_rate = models.FloatField(
        _('budget min rate'),
        blank=True,
        null=True
    )
    budget_max_rate = models.FloatField(
        _('budget max rate'),
        blank=True,
        null=True
    )

    skills = models.ManyToManyField(
        'skills.Skill',
        through='JobSkill',
        related_name='jobs'
    )
    search_terms = models.ManyToManyField(
        'search_terms.SearchTerm',
        through='JobSearchTerm',
        related_name='jobs'
    )

    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f'{self.published_date} / {self.url}'


class JobSkill(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='job_skills'
    )
    skill = models.ForeignKey(
        'skills.Skill',
        on_delete=models.CASCADE,
        related_name='job_skills'
    )

    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f'{self.job} / {self.skill.name}'


class JobSearchTerm(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='job_search_terms'
    )
    search_term = models.ForeignKey(
        'search_terms.SearchTerm',
        on_delete=models.CASCADE,
        related_name='job_search_terms'
    )

    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f'{self.job} / {self.search_term}'
