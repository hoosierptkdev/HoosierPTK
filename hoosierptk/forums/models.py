from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse


# Get the default User model
User = get_user_model()


# Profile Model (extends User model)
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=40, blank=True)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    bio = HTMLField()
    role = models.CharField(max_length=40, blank=True, default="User")
    points = models.IntegerField(default=0)
    profile_pic = ResizedImageField(size=[100, 100], quality=100, upload_to='profiles', default=None, null=True, blank=True)

    # show model in the admin window
    def __str__(self):
        return self.fullname

    # custom save function (get slug)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.fullname)
        super(Profile, self).save(*args, **kwargs)

    # number of posts for a user (property)
    @property
    def num_posts(self):
        return Post.objects.filter(user=self).count()


# Forum Model
class Forum(models.Model):
    title = models.CharField(max_length=50)

    # show model in the admin window
    def __str__(self):
        return self.title


# Topic (Subforum) Model
class Topic(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField(default="description")
    icon = models.CharField(max_length=25)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)

    # show model in the admin window
    def __str__(self):
        return self.title

    # custom save function (get slug)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)

    # reverse/get topic url
    def get_url(self):
        return reverse("forums:posts", kwargs={
            "slug":self.slug,
        })

    # number of posts in a category (property)
    @property
    def num_posts(self):
        return Post.objects.filter(topic=self).count()
         
    # get the last post of a category (property)
    @property
    def last_post(self):
        return Post.objects.filter(topic=self).latest("date")


"""
    All work and no play makes Jack a dull boy
    All work and no play makes Jack a dull boy
    All work and no play mmakes Jack a dull boy
  v All work and no PLay ma es Jack a dull boy
    All work and no play makes Jake a dull boy
    Alll work and no play makes Jack a dul boy
    All wwork and no pl y makes Jack a dull boy

"""


# Reply Model
class Reply(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "replies"

    # display the first 100 characters of content
    def __str__(self):
        return self.content[:100]


# Comment Model
class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)

    # display the first 100 characters of content
    def __str__(self):
        return self.content[:100]


# Post Model
class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = HTMLField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    tags = TaggableManager()
    comments = models.ManyToManyField(Comment, blank=True)
    closed = models.BooleanField(default=False)
    state = models.CharField(max_length=20, default="zero")
    icon = models.CharField(max_length=25, default="fa fa-frown")

    # show model in the admin window
    def __str__(self):
        return self.title

    # custom save function (get slug)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    # reverse/get post url
    def get_url(self):
        return reverse("forums:detail", kwargs={
            "slug":self.slug,
        })

    # get number of post comments
    @property
    def num_comments(self):
        return self.comments.count()

    # get post's last reply
    @property
    def last_reply(self):
        return self.comments.latest("date")

    # get post's status
    def get_status(self, *args, **kwargs):
        if self.closed is False:
            if self.num_comments == 0:
                self.state = "zero"
                self.icon = "fa fa-frown"
            elif self.num_comments > 0 and self.num_comments < 2:
                self.state = "low"
                self.icon = "fa fa-book"
            elif self.num_comments >= 2 and self.num_comments < 4:
                self.state = "high"
                self.icon = "fa fa-rocket"
            elif self.num_comments >= 4:
                self.state = "pop"
                self.icon = "fa fa-fire"
        else:
            self.state = "closed"
            self.icon = "fa fa-lock"
        super(Post, self).save(*args, **kwargs)
        return self.icon
