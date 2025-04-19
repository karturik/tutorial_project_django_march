from django.shortcuts import render
from django.contrib import messages
from .models import Book, Author, BookInstance, Genre    
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import RenewBookForm
    

@login_required
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

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

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
            'num_genres': num_genres,
            'num_visits': num_visits
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


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'books/book_page.html'
    
    def get(self, request, *args, **kwargs):
        # Получаем книгу
        book = self.get_object()
        
        # Получаем или инициализируем счетчик посещений книг в сессии
        if not request.session.get('visited_books'):
            request.session['visited_books'] = {}
        
        # Ключ для записи посещений - id книги в виде строки
        book_id = str(book.id)
        
        # Увеличиваем счетчик для данной книги
        if book_id in request.session['visited_books']:
            request.session['visited_books'][book_id] += 1
        else:
            request.session['visited_books'][book_id] = 1
        
        # Сохраняем изменения в сессии
        request.session.modified = True
        
        # Передаем информацию о посещениях в контекст
        self.extra_context = {
            'num_visits': request.session['visited_books'].get(book_id, 0)
        }
        
        # Продолжаем стандартную обработку запроса
        return super().get(request, *args, **kwargs)

    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='books/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            #(здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('all-borrowed') )

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'books/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'authors/all_authors_page.html'
    paginate_by = 10
    context_object_name = 'all_authors_list'

    def get_queryset(self):
        return super().get_queryset()

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = 'authors/author_page.html'


class AuthorCreate(CreateView, SuccessMessageMixin):
    model = Author
    fields = '__all__'
    # exclude = ['date_of_birth', 'date_of_death']
    initial = {'date_of_birth': '12/10/1900',}
    template_name = 'authors/author_form.html'
    success_message = "Автор успешно создан"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    template_name = 'authors/author_form.html'

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'authors/author_confirm_delete.html'