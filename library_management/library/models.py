from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth import get_user_model
from datetime import timedelta, date

class CustomUser(AbstractUser):
    ROLES = [('admin', 'Admin'), ('member', 'Member')]
    role = models.CharField(max_length=10, choices=ROLES, default='member')


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set on creation (not on updates)
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def borrow(self):
        """Decrease available copies when a book is borrowed."""
        if self.available_copies > 0:
            self.available_copies -= 1
            self.save()
        else:
            raise ValueError("No copies available to borrow.")

    def return_book(self):
        """Increase available copies when a book is returned."""
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            self.save()
        else:
            raise ValueError("All copies are already returned.")
    


class BorrowedBook(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    @property
    def deadline(self):
        return self.borrow_date + timedelta(days=14)

    @property
    def fine(self):
        if not self.return_date:
            return 0
        if self.return_date > self.deadline:
            overdue_days = (self.return_date - self.deadline).days
            return overdue_days * 5
        return 0
