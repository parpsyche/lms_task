from django.contrib import admin
from .models import Book, Transaction

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'unique_code', 'is_available')
    fields = ('title', 'author', 'unique_code', 'description', 'is_available')

admin.site.register(Book, BookAdmin)
admin.site.register(Transaction)
