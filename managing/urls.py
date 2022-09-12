from django.contrib import admin
from django.urls import path
from . import views, RelationsHandle

app_name = "managing"

urlpatterns = [
    path('book-detail/<slug:slug>/', views.BookDetail.as_view(), name="book_detail"),
    path('', views.AddReply.as_view(), name="add_comment"),
    path('set-Action-like/<int:id>/<str:class>/<str:action>/', views.SetCommentsAndRepliesLikeDisLike.as_view(), name="set-action-like"),
    path('add-reply/<int:id>/', views.AddReply.as_view(), name="add_reply"),
    path('add-reply-on/<int:id>/', views.AddReplyOn.as_view(), name="add_reply_on"),
    path('delete-object-model/<int:id>/<str:class>/', views.DeleteObjectModel.as_view(), name="delete_object_model"),
    
]
