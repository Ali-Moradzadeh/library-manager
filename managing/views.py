from django.shortcuts import render, redirect
from django.views import View
from .models import Book, Popularity, Reply, Comment
import addresses
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddCommentForm, AddReplyForm
from django.contrib.contenttypes.models import ContentType
#from .RelationsHandle import SetCommentsAndRepliesLikeDisLike

class BookDetail(View) :
    template_name = addresses.book_detail_template
    form = AddCommentForm()
    
    def setup(self, request, *args, **kwargs) :
        self.book = Book.objects.get(slug=kwargs["slug"])
        super().setup(self, request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs) :
        
        context = {
            "book" : self.book,
            "next" : f"{addresses.book_detail_url}/{kwargs['slug']}",
            "form" : self.form,
        }
        if request.user.is_authenticated :
            context["liked"] = self.book.isLikedBy(request.user)
            context["disliked"] = self.book.isDislikedBy(request.user)
            context["bookmarked"] = self.book.isBookmarkedBy(request.user)
        
        return render(request, self.template_name, context)
    
    
    def post(self, request, *args, **kwargs) :
        form = AddCommentForm(request.POST)
        if form.is_valid() :
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = self.book
            comment.save()
        return redirect(addresses.book_detail_url, kwargs["slug"])


class SetCommentsAndRepliesLikeDisLike(LoginRequiredMixin, View) :
    ACTIONS = {
        "LIKE" : "+",
        "DISLIKE" : "-",
        "BOOKMARK" : "*"
    }
    
    def setup(self, request, *args, **kwargs) :
        self.app_label = kwargs["class"].split("_")[0]
        self.model_name = "_".join(kwargs["class"].split("_")[1:])
        self.content_type = ContentType.objects.get(app_label=self.app_label, model=self.model_name)
        
        self.related_model_obj = self.content_type.model_class().objects.get(pk=kwargs["id"])
        
        return super().setup(self, request, *args, **kwargs)
        
    
    def dispatch(self, request, *args, **kwargs) :
        if "next" not in kwargs :
            kwargs["next"] = addresses.land_url
        
        action = kwargs["action"].upper()
        self.user_requested_action = self.ACTIONS[action]
        
        if action not in self.ACTIONS :
            messages.success(request, "inserted action not found", "alert")
            return redirect(kwargs["next"])
        
        
        if self.related_model_obj.user == request.user :
            return redirect(kwargs["next"])
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs) :
        self.popularity = Popularity(user=request.user, content_type=self.content_type, object_id=self.related_model_obj.id, action=self.user_requested_action)
        self.popularity.save()
        
        return redirect(self.related_model_obj)
        



class AddReply(LoginRequiredMixin, View) :
    form_class = AddReplyForm

    def setup(self, request, *args, **kwargs) :
        self.comment = Comment.objects.get(id=kwargs["id"])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs) :
        form = self.form_class()
        return render(request, "managing/form.html", {"form" : form, "which" : "Reply"})

    def post(self, request, *args, **kwargs) :
        form = self.form_class(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            Reply.objects.create(user=request.user, comment=self.comment, body=cd["body"])

        return redirect(self.comment)
        
        
class AddReplyOn(LoginRequiredMixin, View) :
    form_class = AddReplyForm

    def setup(self, request, *args, **kwargs) :
        self.quote = Reply.objects.get(id=kwargs["id"])
        self.comment = self.quote.comment
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs) :
        form = self.form_class()
        return render(request, "managing/form.html", {"form" : form, "which" : "Reply"})

    def post(self, request, *args, **kwargs) :
        form = self.form_class(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            Reply.objects.create(user=request.user, comment=self.comment, quotes=self.quote, body=cd["body"])

        return redirect(self.comment)


class DeleteObjectModel(LoginRequiredMixin, View) :
    
    def get(self, request, *args, **kwargs) :
        self.app_label = kwargs["class"].split("_")[0]
        self.model_name = "_".join(kwargs["class"].split("_")[1:])
        self.content_type = ContentType.objects.get(app_label=self.app_label, model=self.model_name)
        self.related_model_obj = self.content_type.model_class().objects.get(pk=kwargs["id"])
        self.related_model_obj.delete()
        
        return redirect(kwargs["next"])
    