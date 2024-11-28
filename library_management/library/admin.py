from django.contrib import admin
from .models import Book, BorrowedBook, CustomUser

admin.site.register(CustomUser)
admin.site.register(Book)

@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'return_date', 'deadline', 'fine')
    fields = ('user', 'book', 'borrow_date', 'return_date', 'deadline', 'fine')
    readonly_fields = ('borrow_date', 'deadline', 'fine')
    ordering = ['-borrow_date']