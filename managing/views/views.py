from django.shortcuts import render, redirect
from django.views import View
from .models import Book, Popularity
import addresses
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddCommentForm, AddReplyForm
from .RelationsHandle import SetCommentsAndRepliesLikeDisLike as CommentsAndRepliesPopularity


class BookDetail(View) :
    template_name = addresses.book_detail_template
    form = AddCommentForm()
    def get(self, request, *args, **kwargs) :
        book = Book.objects.get(slug=kwargs["slug"])
        comments = book.comment.filter(visible=True)
        comments_count = comments.count()
        replies = dict()
        for comment in comments :
            replies[comment.id] = comment.reply.all()

        return render(request, self.template_name, {"book" : book, "next" : f"{addresses.book_detail_url}/{kwargs['slug']}", "form" : self.form })
    
    def post(self, request, *args, **kwargs) :
        form = AddCommentForm(request.POST)
        if form.is_valid() :
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = Book.objects.get(id=kwargs["id"])
            comment.save()
            return redirect(addresses.book_detail_url, kwargs["id"])

class AddReply(LoginRequiredMixin, View) :
    form_class = AddReplyForm

    def get(self, request, *args, **kwargs) :
        form = self.form_class()
        #render(request, 
    
class SetCommentsAndRepliesLikeDisLike(LoginRequiredMixin, View) :
    CommentsAndRepliesPopularity()