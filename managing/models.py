from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User
from taggit.models import Tag as T, TaggedItem as TI
from taggit.managers import TaggableManager as TG
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta, date

# Create your models here.
app_name = 'managing'

def getModelQ(model) :
    return models.Q(app_label=app_name, model=model)

class GenericAbs(models.Model) :
    user = models.ForeignKey("MngUser", on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s")
    action = models.CharField(max_length=1)
    date = models.DateTimeField(auto_now=True)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Action on model")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    class Meta :
        abstract = True
        unique_together = ("action", "content_type", "object_id")
        

class Popularity(GenericAbs) :
    ACTION = (('+', 'Like'), ('-', 'DisLike'), ("*", "Bookmark"))
    action = models.CharField(max_length=1, choices=ACTION)
    foreigns = getModelQ('author') | getModelQ('publisher') | getModelQ('book') | getModelQ('comment') | getModelQ('reply') | models.Q(app_label="taggit", model="tag")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=foreigns, verbose_name="Action on model")
    
    def __str__(self) :
        return f"{self.content_object} {self.get_action_display()}ed by {self.user}"


class Prevention(GenericAbs) :
    ACTION = (('B', 'Bann'), ('R', 'Report'))
    action = models.CharField(max_length=1, choices=ACTION)
    foreigns = getModelQ('author') | getModelQ('publisher') | getModelQ('book') | getModelQ('comment') | getModelQ('reply')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=foreigns, verbose_name="Action on model")
    
    def __str__(self) :
        return f"{self.content_object} {self.get_action_display()}ed by {self.user}"


class FollowUp(GenericAbs) :
    ACTION = (('F', 'Follow'), )
    action = models.CharField(max_length=1, choices=ACTION)
    foreigns = getModelQ('author') | getModelQ('publisher') | getModelQ('book')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=foreigns, verbose_name="Action on model")
    
    def __str__(self) :
        return f"{self.content_object} followed by {self.user}"


class Address(models.Model) :
    foreigns = getModelQ('Mnguser') | getModelQ('publisher')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=foreigns, verbose_name="Action on model")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    full_address = models.TextField()
    
    class Meta :
        unique_together = ("content_type", "object_id")
        

class MngUser(AbstractBaseUser) :
    user = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    national_code=models.PositiveIntegerField(unique=True, null=True)
    observer_user=models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)
    loan_remain = models.PositiveSmallIntegerField(default=5)
    profile_img = models.ImageField(upload_to="managing/images/profile_images", null=True, blank=True)
    about = models.TextField(blank=True)
    violations = models.PositiveIntegerField(default=0)
    total_damage_cost = models.PositiveIntegerField(default=0)
    wallet_inventory = models.PositiveIntegerField(default=0)
    
    
    address = GenericRelation(Address, related_query_name="user")
    
    USERNAME_FIELD = "user"
    REQUIRED_FIELDS = ["user", "email", "national_code"]
    

class Author(models.Model) :
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nationality = models.CharField(max_length=30)
    
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
    register_code = models.PositiveIntegerField(unique=True)
    #branches;
    
    popularity = GenericRelation(Popularity, related_query_name="publisher")
    prevention = GenericRelation(Prevention, related_query_name="publisher")
    follow_up = GenericRelation(FollowUp, related_query_name="publisher")
    address = GenericRelation(Address, related_query_name="publisher")
    
    def __str__(self) :
        return self.name


class Book(models.Model) :
    
    def year_choices():
        return [(r,r) for r in range(1850, date.today().year+1)]
    title = models.CharField(max_length=100, unique=True)
    Author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="book")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,related_name="book")
    year_published = models.PositiveIntegerField(choices=year_choices())
    print_num = models.PositiveSmallIntegerField(default=1)
    cover_num = models.PositiveSmallIntegerField(default=1)
    cover_img = models.ImageField(upload_to="forum/images/books_covers", null=True, blank=True)
    pages = models.PositiveIntegerField()
    in_store = models.PositiveSmallIntegerField()
    cost = models.PositiveIntegerField()
    
    tag = TG()
    
    popularity = GenericRelation(Popularity, related_query_name="book")
    prevention = GenericRelation(Prevention, related_query_name="book")
    follow_up = GenericRelation(FollowUp, related_query_name="book")
    
    def __str__(self) :
        return self.title


class Comment(models.Model):
    STATUS = (("V", "VISIBLE"), ("I", "INVISIBLE"))
    user = models.ForeignKey(MngUser, on_delete=models.CASCADE, related_name="comment")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comment")
    body = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)
    
    popularity = GenericRelation(Popularity, related_query_name="comment")
    prevention = GenericRelation(Prevention, related_query_name="comment")
    follow_up = GenericRelation(FollowUp, related_query_name="comment")
    
    def __str__(self) :
        return f"{self.user} on {self.book}"


class Reply(models.Model):
    user = models.ForeignKey(MngUser, on_delete=models.CASCADE, related_name="reply")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reply")
    quotes = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="on_reply", blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)
    
    popularity = GenericRelation(Popularity, related_query_name="replay")
    prevention = GenericRelation(Prevention, related_query_name="replay")
    follow_up = GenericRelation(FollowUp, related_query_name="replay")
    
    def __str__(self) :
        f"{self.user} on {self.comment}"


class Loan(models.Model) :
    STATE = (("R", "Requested"), ("C", "Checking"), ("RC", "request confirmed"), ("S", "Sent"), ("D", "Delivered"))
    user = models.ForeignKey(MngUser, on_delete=models.CASCADE, related_name="req_loan")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="req_loan")
    date_requested = models.DateTimeField(auto_now_add=True)
    date_request_confirmed = models.DateTimeField(null=True, blank=True)
    date_sent = models.DateTimeField(null=True, blank=True)
    date_delivered = models.DateTimeField(null=True, blank=True)
    last_request_state_date = models.DateTimeField(auto_now_add=True)
    last_extension_date = models.DateTimeField(null=True, blank=True)
    total_extension_day = models.PositiveSmallIntegerField(default=0)
    remain_extention_count = models.PositiveSmallIntegerField(default=5)
    request_state = models.CharField(max_length=2, choices=STATE)
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
    
    user = models.ForeignKey(MngUser, on_delete=models.CASCADE, related_name="suggestions")
    book = models.CharField(max_length=30)
    Author = models.CharField(max_length=30)
    info = models.TextField
    state = models.CharField(max_length=1, choices=STATE, default="S")
    

