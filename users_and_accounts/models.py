from django.db import models
from django.conf import settings
from catalog.models import Book

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    # blank=True означает, что у пользователя может не быть понравившихся книг
    liked_books = models.ManyToManyField(Book, related_name='liked_by_users', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Дата и время создания

    def __str__(self):
        return f"Сообщение от {self.name} ({self.email})"

    class Meta:
        verbose_name = "Контактное сообщение"
        verbose_name_plural = "Контактные сообщения"
        ordering = ['-created_at']
        