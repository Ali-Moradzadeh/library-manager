from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from managing.models import Book, Popularity
import addresses
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin


