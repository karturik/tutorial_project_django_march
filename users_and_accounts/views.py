from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest

from .models import Profile
from .forms import ProfileEditForm, UserEditForm, ContactForm

# class SignUpView(CreateView):
#     template_name = 'signup.html'
#     form_class = UserCreationForm
#     success_url = reverse_lazy('home') # Укажите ваш URL для перенаправления

#     def form_valid(self, form):
#         valid = super().form_valid(form)
#         login(self.request, self.object)
#         return valid

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("catalog_home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/registration_page.html", context={"register_form": form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect("edit")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/edit.html', {'user_form': user_form, 
                                                     'profile_form': profile_form})
    
# --- Наше AJAX представление ---
def validate_username(request):
    """
    Проверяет, существует ли пользователь с таким именем (регистронезависимо).
    Ожидает GET-параметр 'username'.
    Возвращает JSON: {'is_taken': true/false}.
    """
    # Получаем значение параметра 'username' из GET-запроса.
    # request.GET - это словарь с параметрами GET-запроса.
    # .get('username', None) - безопасный способ получить значение,
    # вернет None, если параметр отсутствует.
    username = request.GET.get('username', None)

    if username is None:
        # Желательно обрабатывать случай, когда параметр не передан
        return JsonResponse({'error': 'Username parameter missing'}, status=400)

    # Проверяем наличие пользователя в базе данных.
    # User.objects.filter(username__iexact=username) - ищет пользователя.
    # __iexact - регистронезависимое точное совпадение.
    # .exists() - возвращает True, если найден хотя бы один объект, иначе False.
    is_taken = User.objects.filter(username__iexact=username).exists()

    # Формируем данные для ответа
    data = {
        'is_taken': is_taken
    }
    # Возвращаем ответ в формате JSON.
    # JsonResponse автоматически установит правильный Content-Type: application/json.
    return JsonResponse(data)

def contact_form_view(request: HttpRequest):
    # Если запрос НЕ AJAX, просто отображаем пустую форму
    # Метод is_ajax() устарел, проверяем заголовок HTTP_X_REQUESTED_WITH
    # Этот заголовок обычно добавляют JavaScript-библиотеки (как jQuery) или его нужно добавлять вручную при использовании Fetch
    is_ajax_request = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if request.method == 'POST':
        # Создаем экземпляр формы и заполняем его данными из POST-запроса
        form = ContactForm(request.POST)

        if form.is_valid():
            # Данные формы валидны
            instance = form.save() # Сохраняем объект ContactMessage в БД
            # Для AJAX возвращаем JSON с сообщением об успехе и именем пользователя
            if is_ajax_request:
                return JsonResponse({
                    "message": f"Спасибо, {instance.name}! Ваше сообщение получено.",
                    "name": instance.name # Можно вернуть и другие данные при необходимости
                    }, status=200)
            else:
                # Обычный POST-запрос не через AJAX - можем сделать редирект или показать страницу успеха
                # return redirect('success_page_url') # Замените на ваш URL
                messages.success(request, f"Спасибо, {instance.name}! Ваше сообщение получено.")
                return redirect('catalog_page')

        else:
            # Данные формы невалидны
            if is_ajax_request:
                # Для AJAX возвращаем ошибки формы в формате JSON и статус 400 (Bad Request)
                # form.errors.as_json() возвращает строку JSON, ее и передаем
                return JsonResponse({"errors": form.errors}, status=400)
            else:
                messages.error(request, f"errors: {form.errors}")
                # Для обычного POST-запроса просто рендерим форму снова с ошибками
                return redirect('catalog_page')

    # Если это GET-запрос (или любой другой метод, не POST)
    else:
        form = ContactForm() # Создаем пустую форму

    # Отображаем шаблон с формой
    return render(request, 'contact_form.html', {'form': form})

# # --- ВАЖНО: Представление для AJAX на основе класса (альтернатива) ---
# from django.views.generic.edit import FormView

# class ContactFormAjaxView(FormView):
#     template_name = 'contact_form.html' # Тот же шаблон
#     form_class = ContactForm
#     # success_url = reverse_lazy('some-success-url') # Нужен для НЕ-AJAX случаев, если не переопределять form_valid/form_invalid полностью

#     def form_valid(self, form):
#         """ Вызывается, если форма валидна. """
#         instance = form.save()
#         # Проверяем, был ли запрос сделан через AJAX
#         is_ajax_request = self.request.headers.get("X-Requested-With") == "XMLHttpRequest"
#         if is_ajax_request:
#             # Если AJAX, возвращаем JSON
#             return JsonResponse({
#                 "message": f"Спасибо, {instance.name}! Ваше сообщение получено (из CBV).",
#                 "name": instance.name
#                 }, status=200)
#         else:
#              # Если не AJAX, вызываем стандартное поведение (редирект на success_url)
#             return super().form_valid(form)

#     def form_invalid(self, form):
#         """ Вызывается, если форма невалидна. """
#         is_ajax_request = self.request.headers.get("X-Requested-With") == "XMLHttpRequest"
#         if is_ajax_request:
#             # Если AJAX, возвращаем ошибки в JSON
#              return JsonResponse({"errors": form.errors}, status=400)
#         else:
#             # Если не AJAX, вызываем стандартное поведение (повторный рендер шаблона с ошибками)
#             return super().form_invalid(form)
