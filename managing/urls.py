from django.contrib import admin
from django.urls import path
from . import views

app_name = "managing"

urlpatterns = [
    path('book-detail/book/<int:id>/', views.BookDetail.as_view(), name="book_detail"),
    path('set-Action-like/<int:id>/<str:class>/', views.SetActionLike.as_view(), name="set-action-like")
]
