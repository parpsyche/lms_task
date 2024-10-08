from django.db import models
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    class Roles(models.TextChoices):
        LIBRARIAN = 'Librarian', 'Librarian'
        STUDENT = 'Student', 'Student'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=Roles.choices, default='Student', max_length=100)
    
    def save(self, *args, **kwargs):
        if self.role == 'Librarian':
            self.user.is_staff = True
        super().save(*args, **kwargs)
        
    def __str__(self):
        if self.role == 'Librarian':
            return f"LIBRARIAN - {self.user.username}"
        elif self.role == 'Student':
            return self.user.username
        
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    unique_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_by = models.CharField(max_length=200)
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.return_date:
            self.return_date = self.issue_date + datetime.timedelta(days=7)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} issued by {self.issued_by}"

class IssuedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} issued to {self.user.username}"
