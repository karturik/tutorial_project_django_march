from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre    
from django.views import generic


def catalog_homepage_view(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.

    num_genres = Genre.objects.all().count()

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'catalog_homepage.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genres': num_genres
            },
    )


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'all_books_list'
    template_name = 'books/all_books_page.html'
    # queryset = Book.objects.all()

    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = 'This is just some data'
        return context
    

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_page.html'
