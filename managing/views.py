from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, ListView
from .models import Book, Popularity
import addresses
from django.db import models
from django.contrib.contenttypes.models import ContentType


def checkingPopularityExist(user, content, object_id, action) :
    app_label = content.split("_")[0]
    model_name = "_".join(content.split("_")[1:])
    content_type = ContentType.objects.get(app_label=app_label, model=model_name)
    m = Popularity.objects.filter(user=user, content_type=content_type, object_id=object_id, action=action)
    
    return bool(m)




class BookDetail(View) :
    template_name = addresses.book_detail_template
    
    def get(self, request, *args, **kwargs) :
        book = Book.objects.get(id=kwargs["id"])
        comments = book.comment.filter(visible=True)
        comments_count = comments.count()
        replies = dict()
        for comment in comments :
            replies[comment.id] = comment.reply.all()

        
        return render(request, self.template_name, {"book" : book, "popExistFunc" : checkingPopularityExist})


class SetActionLike(View):
    def get(self, request, *args, **kwargs) :
        app_label = kwargs["class"].split("_")[0]
        model_name = "_".join(kwargs["class"].split("_")[1:])
        print(app_label, model_name)
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        m = Popularity.objects.create(user=request.user, content_type=content_type, object_id=kwargs["id"], action="+")
        m.save()
        
        
    
# Create your views here.
