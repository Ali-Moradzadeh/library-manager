from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

class MostCommented(models.Manager) :
    def get_queryset(self) :
        return super().get_queryset().annotate(count=Count("comment")).order_by("-count", "date_created")
    
class BookManager(models.Manager) :
    def Recently(self) :
        return self.order_by("date_created")
        
    def mostLiked(self) :
        return self.annotate(count=Count("comment")).order_by("-count", "date_created")
    
    
class PopularityManager(models.Manager) :
    
    def content(self, app, model) :
        return models.Q(app_label=app, model=model)
    
    def likes(self) :
        return self.filter(action="+")
    
    def dislikes(self) :
        return self.filter(action="-")
        
    def bookmarks(self) :
        return self.filter(action="*")
    
    def by(self, user) :
        return self.filter(user=user)

    def onAuthors(self) :
        Author = ContentType.objects.get(app_label="managing", model="author")
        return self.filter(content_type=Author)
    
    def onPublishers(self) :
        Publisher = ContentType.objects.get(app_label="managing", model="publisher")
        return self.filter(content_type=Publisher)
    
    def onBooks(self) :
        Book = ContentType.objects.get(app_label="managing", model="book")
        return self.filter(content_type=Book)
    
    def onComments(self) :
        Comment = ContentType.objects.get(app_label="managing", model="comment")
        return self.filter(content_type=Comment)
        
    def onReplies(self) :
        Reply = ContentType.objects.get(app_label="managing", model="reply")
        return self.filter(content_type=Reply)
    
    def onId(self, Id) :
        return self.filter(object_id=Id)
        
    def On(self, book) :
        self.filter(content_type__model_class__objects__all__0)
    
    