from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, BorrowedBook
from .serializers import BookSerializer, BorrowedBookSerializer, UserRegistrationSerializer
from .permissions import IsMember
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import date

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Authenticated users can list or retrieve
            return [IsAuthenticated()]
        return [IsAdminUser()] 

class BorrowedBookViewSet(viewsets.ViewSet):
    permission_classes = [IsMember]

    @action(detail=False, methods=['post'])
    def borrow(self, request):
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)

        if book.available_copies <= 0:
            return Response({'error': 'No copies available'}, status=400)

        if BorrowedBook.objects.filter(user=request.user, book=book, return_date__isnull=True).exists():
            return Response({'error': 'You have already borrowed this book'}, status=400)

        if BorrowedBook.objects.filter(user=request.user, return_date__isnull=True).count() >= 5:
            return Response({'error': 'Borrow limit reached'}, status=400)

        # Borrow the book
        BorrowedBook.objects.create(user=request.user, book=book)
        book.borrow()  # Decrement available copies
        return Response({'message': 'Book borrowed successfully'})

    @action(detail=False, methods=['post'])
    def return_book(self, request):
        borrowed_id = request.data.get('borrowed_id')
        try:
            borrowed_book = BorrowedBook.objects.get(id=borrowed_id, user=request.user)
        except BorrowedBook.DoesNotExist:
            return Response({'error': 'Invalid borrowed book'}, status=404)

        if borrowed_book.return_date is not None:
            return Response({'error': 'This book has already been returned'}, status=400)

        borrowed_book.return_date = date.today()
        borrowed_book.save()

        book = borrowed_book.book
        try:
            book.return_book()
        except ValueError as e:
            return Response({'error': str(e)}, status=400)

        return Response({'message': 'Book returned successfully', 'fine': borrowed_book.fine})
    
    @action(detail=False, methods=['get'], url_path='my-borrowed-books')
    def my_borrowed_books(self, request):
        """
        Retrieve all borrowed books for the logged-in user.
        """
        user = request.user
        borrowed_books = BorrowedBook.objects.filter(user=user)
        serializer = BorrowedBookSerializer(borrowed_books, many=True)
        return Response(serializer.data)

