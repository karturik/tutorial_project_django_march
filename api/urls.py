from django.urls import path, include
from rest_framework.routers import DefaultRouter # Импортируем DefaultRouter
from rest_framework.authtoken import views as authtoken_views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from . import views # Импортируем представления из текущего приложения (api)

# Создаем экземпляр маршрутизатора
# DefaultRouter автоматически создает корневое представление API (API Root)
router = DefaultRouter() 

# Регистрируем наши ViewSets в маршрутизаторе
# router.register(префикс_url, ViewSet_класс, basename)
router.register(r'genres', views.GenreViewSet, basename='genre')
router.register(r'languages', views.LanguageViewSet, basename='language')
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'books', views.BookViewSet, basename='book')

# URL-паттерны теперь генерируются автоматически маршрутизатором.
# Нам нужно только включить сгенерированные URL в наши urlpatterns.
app_name = 'api' # Оставляем для ясности

urlpatterns = [
    path('', include(router.urls)), 

    path('token-auth/', authtoken_views.obtain_auth_token, name='api_token_auth'),


    # # Эндпоинты для Жанров (Genres)
    # path('genres/', views.GenreList.as_view(), name='genre-list'), 
    # path('genres/<int:pk>/', views.GenreDetail.as_view(), name='genre-detail'),

    # # Эндпоинты для Языков (Languages)
    # path('languages/', views.LanguageList.as_view(), name='language-list'),
    # path('languages/<int:pk>/', views.LanguageDetail.as_view(), name='language-detail'),

    # # Эндпоинты для Авторов (Authors)
    # path('authors/', views.AuthorList.as_view(), name='author-list'),
    # path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author-detail'),

    # # Эндпоинты для Книг (Books)
    # path('books/', views.BookList.as_view(), name='book-list'),
    # path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),

    # Можно добавить эндпоинт для корневого API, если нужно (пока пропустим)
    # path('', views.api_root), # Потребуется создать представление api_root
]