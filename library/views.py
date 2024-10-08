from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer
from datetime import date, timedelta
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.forms import UserCreationForm

# Book List API
class BookListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Book.objects.filter(is_available=True)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

# Issue Book API
class IssueBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)

        if not book.is_available:
            return Response({'error': 'Book is not available'}, status=status.HTTP_400_BAD_REQUEST)

        issued_by = request.user.username
        issue_date = date.today()
        return_date = issue_date + timedelta(days=15)

        transaction = Transaction.objects.create(
            book=book,
            issued_by=issued_by,
            issue_date=issue_date,
            return_date=return_date,
            fine_paid=False
        )

        book.is_available = False
        book.save()

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

# Return Book API
class ReturnBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id, issued_by=request.user.username)

        book = transaction.book
        book.is_available = True
        book.save()

        if transaction.return_date < date.today():
            days_overdue = (date.today() - transaction.return_date).days
            fine_amount = days_overdue
            transaction.fine_paid = fine_amount

        transaction.delete()
        return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)

# User Signup API
@api_view(['POST'])
def signup(request):
    form = UserCreationForm(request.data)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login API
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# User Logout API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

# Admin Dashboard API
class AdminDashboardAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

# Issued Books for User API
class IssuedBooksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(issued_by=request.user.username)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

# Borrowed Books API
class BorrowedBooksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(issued_by=request.user.username)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
