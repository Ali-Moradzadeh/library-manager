from django.shortcuts import render
from django.views import View
from managing.models import Book
import addresses

class land(View) :
    template_name = addresses.land_template
    books = Book.objects.all()
    def get(self, request) :
        return render(request, self.template_name, {"books" : self.books})