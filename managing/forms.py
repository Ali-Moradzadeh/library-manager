from django import forms
from .models import Comment, Reply

class AddCommentForm(forms.ModelForm) :
    class Meta :
        model = Comment 
        fields = ("body", )

class AddReplyForm(forms.ModelForm) :
    class Meta :
        model = Reply 
        fields = ("body", )

