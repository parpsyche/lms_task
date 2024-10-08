from django.urls import path
from .views import (
    BookListAPIView, IssueBookAPIView, ReturnBookAPIView, 
    signup, login_view, logout_view, AdminDashboardAPIView, 
    IssuedBooksAPIView, BorrowedBooksAPIView
)

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='book_list'),
    path('books/<int:book_id>/issue/', IssueBookAPIView.as_view(), name='issue_book'),
    path('transactions/<int:transaction_id>/return/', ReturnBookAPIView.as_view(), name='return_book'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin-dashboard/', AdminDashboardAPIView.as_view(), name='admin_dashboard'),
    path('issued-books/', IssuedBooksAPIView.as_view(), name='issued_books'),
    path('borrowed-books/', BorrowedBooksAPIView.as_view(), name='borrowed_books'),
]
