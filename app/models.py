from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import math
from cloudinary.models import CloudinaryField


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,  on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    slug = models.SlugField(max_length=120)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    restrict_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id, self.slug])

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "s."

            else:
                return str(seconds) + " s."

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " m."

            else:
                return str(minutes) + " m."

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hr."

            else:
                return str(hours) + " hrs."

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day"

            else:
                return str(days) + " days"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " yr"

            else:
                return str(years) + " years ago"


@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].author)
    kwargs['instance'].slug = slug


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = CloudinaryField('image')

    class Meta:
        verbose_name_plural = "Images"

    def __str__(self):
        return self.post.body + ' Image'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return "Profile of User {}".format(self.user.username)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True,
                              related_name='replies', on_delete=models.CASCADE)
    content = models.TextField(max_length=160)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(str(self.user.username))
