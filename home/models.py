from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created', 'body')

    def __str__(self):
        return f'{self.user} -- {self.title} --{self.published}'

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))

    def like_count(self):
        return self.postvotes.count()

    def user_can_like(self, user):
        user_like = user.uservotes.filter(post=self)
        if user_like.exists():
            return True
        else:
            return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='rcomments')
    is_reply = models.BooleanField(default=False)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:25]}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uservotes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postvotes')

    def __str__(self):
        return f'{self.user} like {self.post.slug}'



