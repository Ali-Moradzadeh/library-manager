from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User, AbstractUser
from taggit.models import Tag as T, TaggedItem as TI
from taggit.managers import TaggableManager as TG
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta, date
from authenticate.models import CustomUser
from django.utils.text import slugify
from .managers import BookManager, MostCommented, PopularityManager
import addresses
from django.urls import reverse
# Create your models here.
app_name = 'managing'

def getModelQ(model) :
    return models.Q(app_label=app_name, model=model)

class GenericAbs(models.Model) :
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s", null=True)
    action = models.CharField(max_length=1, null=True)
    date = models.DateTimeField(auto_now=True, null=True)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Action on model", null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()
    
    class Meta :
        abstract = True
        unique_together = ("user", "action", "content_type", "object_id")
        

class Popularity(GenericAbs) :
    ACTION = (('+', 'Like'), ('-', 'DisLike'), ("*", "Bookmark"))
    action = models.CharField(max_length=1, choices=ACTION, null=True)
    foreigns = getModelQ('author') | getModelQ('publisher') | getModelQ('book') | getModelQ('comment') | getModelQ('reply') | models.Q(app_label="taggit", model="tag")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=foreigns, verbose_name="Action on model", null=True)
    
    objects = PopularityManager()
    
    def save(self, *args, **kwargs) :
        opposites = ("+", "-")
        
        def getOpposite(action) :
            if action in opposites :
                return opposites[1 - opposites.index(action)]
            return None
        
        def get_object_with_action(action) :
            pop = Popularity.objects.filter(user=self.user, content_type=self.content_type, object_id = self.object_id, action=action)
            
            if pop.exists() :
                return pop[0]
            return None

        if getOpposite(self.action) :
            this = get_object_with_action(self.action)
            opposite = get_object_with_action(getOpposite(self.action))
            if this:
                return this.delete()

            elif opposite:
                opposite.action = self.action
                self = opposite
                return super().save(*args, **kwargs)
        
        else :
            
            if this := get_object_with_action(self.action) :
                return this.delete()
            
        super().save(*args, **kwargs)
            
    
    
    def __str__(self) :
        return f"{self.content_object} {self.get_action_display()}ed by {self.user}"


class Prevention(GenericAbs) :
    ACTION = (('B', 'Bann'), ('R', 'Report'))
    action = models.CharField(max_length=1, choices=ACTION, null=True)
    foreigns = getModelQ('author') | getModelQ('publisher') | getModelQ('book') | getModelQ('comment') | getModelQ('reply')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=foreigns, verbose_name="Action on model", null=True)
    
    def __str__(self) :
        return f"{self.content_object} {self.get_action_display()}ed by {self.user}"


class FollowUp(GenericAbs) :
    ACTION = (('F', 'Follow'), )
    action = models.CharField(max_length=1, choices=ACTION, null=True)
    foreigns = getModelQ('author') | getModelQ('publisher') | getModelQ('book')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=foreigns, verbose_name="Action on model", null=True)
    
    def __str__(self) :
        return f"{self.content_object} followed by {self.user}"


class Address(models.Model) :
    foreigns = getModelQ(CustomUser) | getModelQ('publisher')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=foreigns, verbose_name="Action on model", null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()
    full_address = models.TextField(null=True)
    
    class Meta :
        unique_together = ("content_type", "object_id")

class Author(models.Model) :
    name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    nationality = models.CharField(max_length=30, null=True)
    
    popularity = GenericRelation(Popularity, related_query_name='author')
    prevention = GenericRelation(Prevention, related_query_name='author')
    follow_up = GenericRelation(FollowUp, related_query_name='author')
    
    @property
    def full_name(self) :
        return f"{self.name} {self.last_name}"
    
    class Meta :
        unique_together = ("name", "last_name", "nationality")
    def __str__(self) :
        return self.full_name


class Publisher(models.Model) :
    name = models.CharField(max_length=30)
    register_code = models.PositiveIntegerField(unique=True, null=True)
    #branches;
    
    popularity = GenericRelation(Popularity, related_query_name="publisher")
    prevention = GenericRelation(Prevention, related_query_name="publisher")
    follow_up = GenericRelation(FollowUp, related_query_name="publisher")
    address = GenericRelation(Address, related_query_name="publisher")
    
    def __str__(self) :
        return self.name


class Book(models.Model) :
    objects = BookManager()
    mostCommented = MostCommented()
    def year_choices():
        return [(r,r) for r in range(1850, date.today().year+1)]
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="created_books", null=True)
    
    title = models.CharField(max_length=100, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="book", null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,related_name="book", null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    year_published = models.PositiveIntegerField(choices=year_choices(), null=True)
    print_num = models.PositiveSmallIntegerField(default=1)
    cover_num = models.PositiveSmallIntegerField(default=1)
    cover_img = models.ImageField(upload_to="forum/images/books_covers", null=True, blank=True)
    pages = models.PositiveIntegerField(null=True)
    in_store = models.PositiveSmallIntegerField(null=True)
    cost = models.PositiveIntegerField(null=True)
    tag = TG()
    slug = models.SlugField(null=True)
    
    popularity = GenericRelation(Popularity, related_query_name="book")
    prevention = GenericRelation(Prevention, related_query_name="book")
    follow_up = GenericRelation(FollowUp, related_query_name="book")
    
    def isBookmarkedBy(self, user) :
        return bool(self.popularity.bookmarks().filter(user=user))
    
    def isLikedBy(self, user) :
        return bool(self.popularity.likes().filter(user=user))
    
    def isDislikedBy(self, user) :
        return bool(self.popularity.dislikes().filter(user=user))
    
    
    def get_absolute_url(self) :
        return reverse(addresses.book_detail_url, args=[self.slug])


    def save(self, *args, **kwargs) :
        self.slug = '-'.join([slugify(self.title), slugify(self.author), slugify(self.publisher), slugify(self.user)])
        super().save(*args, **kwargs)
    
    
    def __str__(self) :
        return self.title


class Comment(models.Model):
    STATUS = (("V", "VISIBLE"), ("I", "INVISIBLE"))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comment", null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comment", null=True)
    body = models.TextField(null=True)
    date_published = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    visible = models.BooleanField(default=True)
    
    popularity = GenericRelation(Popularity, related_query_name="comment")
    prevention = GenericRelation(Prevention, related_query_name="comment")
    follow_up = GenericRelation(FollowUp, related_query_name="comment")
    
    
    def get_absolute_url(self) :
        return self.book.get_absolute_url()
    
    class Meta :
        ordering = ("date_published", )
    
    def __str__(self) :
        return f"{self.body}"


class Reply(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reply", null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reply", null=True)
    quotes = models.ForeignKey("self", on_delete=models.CASCADE, related_name="on_reply", null=True, blank=True)
    body = models.TextField(null=True)
    date_published = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    visible = models.BooleanField(default=True)
    
    popularity = GenericRelation(Popularity, related_query_name="replay")
    prevention = GenericRelation(Prevention, related_query_name="replay")
    follow_up = GenericRelation(FollowUp, related_query_name="replay")
    
    def get_absolute_url(self) :
        return self.comment.book.get_absolute_url()
    
    def __str__(self) :
        return f"{self.body}"


class Loan(models.Model) :
    STATE = (("R", "Requested"), ("C", "Checking"), ("RC", "request confirmed"), ("S", "Sent"), ("D", "Delivered"))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="req_loan", null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="req_loan", null=True)
    date_requested = models.DateTimeField(auto_now_add=True, null=True)
    date_request_confirmed = models.DateTimeField(null=True, blank=True)
    date_sent = models.DateTimeField(null=True, blank=True)
    date_delivered = models.DateTimeField(null=True, blank=True)
    last_request_state_date = models.DateTimeField(auto_now_add=True, null=True)
    last_extension_date = models.DateTimeField(null=True, blank=True)
    total_extension_day = models.PositiveSmallIntegerField(default=0)
    remain_extention_count = models.PositiveSmallIntegerField(default=5)
    request_state = models.CharField(max_length=2, choices=STATE, null=True)
    serial = models.CharField(max_length=20, blank=True)
    
    @property
    def last_request_detail() :
        return f"{self.get_request_state_display} on {self.last_request_state_date}"

    @property
    def return_date(self) :
        days = 7
        days += (self.book.pages - 200 ) // 50
        days += self.total_extension_day
        return self.date_delivered + timedelta(days=days)
    
    @property
    def loan_fee(self, req_days) :
        if self.remain_extention_count == 3 :
            return req_days * 1000
        return 0


class Suggestion(models.Model) :
    STATE = (("S", "Suggested"), ("C", "Considered"))
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ssuggestions", null=True)
    book = models.CharField(max_length=30, null=True)
    Author = models.CharField(max_length=30, null=True)
    info = models.TextField(null=True)
    state = models.CharField(max_length=1, choices=STATE, default="S")
    date = models.DateTimeField(auto_now_add=True, null=True)
    

