from django.contrib import admin
from .models import Book, Transaction, IssuedBook, UserProfile

admin.site.register(IssuedBook)
admin.site.register(UserProfile)

admin.site.register(Book)
admin.site.register(Transaction)
