from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

"""
MAX_YEARS_TITLES: this value indicates which year can be the maximum for the
publication date of the work (+ 10 years for current year).
Relevant for upcoming movies, books, etc.
"""
MAX_YEARS_TITLES = dt.now().year + 10


class Categorie(models.Model):
    """Model for categories titles: films, books, etc."""

    name = models.CharField(
        _('category name'),
        max_length=128,
        unique=True,
        help_text=_("Please enter category name (it's required)."),
    )
    slug = models.SlugField(
        _('category slug'),
        blank=True,
        max_length=128,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    """Model for genre titles: comedy, fantasy, etc."""

    name = models.CharField(
        _('genre name'),
        max_length=100,
        unique=True,
        help_text=_("Please enter genre name (it's required)."),
    )
    slug = models.SlugField(
        _('genre slug'),
        blank=True,
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Title(models.Model):
    """Model for titles."""

    name = models.CharField(
        _('title name'),
        max_length=128,
        db_index=True,
        help_text=_("Please enter title name (it's required)."),
    )
    year = models.PositiveSmallIntegerField(
        _('title year'),
        null=True,
        blank=True,
        db_index=True,
        validators=(
            MaxValueValidator(
                MAX_YEARS_TITLES,
                (
                    'Expected title year must not be later than '
                    '10 years from the current year.'
                ),
            ),
        ),
    )
    description = models.TextField(
        _('title description'),
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='titles',
        verbose_name=_('title genre'),
    )
    category = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=True,
        related_name='titles',
        verbose_name=_('title category'),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'


class Review(models.Model):
    """ Model for reviews, where users
    can score the title and write their opinion. """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('review title'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('review author'),
    )
    text = models.TextField(
        _('text'),
        help_text=_("Please enter review text (it's required)."),
    )
    score = models.PositiveSmallIntegerField(
        _('review score'),
        null=True,
        validators=(
            MinValueValidator(1, 'Please, rate the title from 1 to 10.'),
            MaxValueValidator(10, 'Please, rate the title from 1 to 10.'),
        ),
    )
    pub_date = models.DateTimeField(
        _('publication date'),
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Comment(models.Model):
    """ Model for comments for review
    where users can discuss the review. """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('comment author'),
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('comment review'),
    )
    text = models.TextField(
        _('text'),
        help_text=_("Please enter comment text (it's required)."),
    )
    pub_date = models.DateTimeField(
        _('publication date'),
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
