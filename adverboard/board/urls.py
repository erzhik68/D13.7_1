from django.urls import path
from .views import AdsList, AdDetailView, AdCreateView, AddComment, AdCreate, Add

urlpatterns = [
    # path('', IndexView.as_view()),
    path('', AdsList.as_view(), name='ads_list'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),  # Ссылка на детали поста
    path('add/', Add, name='add'),  # Пример. Ссылка на создание поста
    path('create/', AdCreate, name='ad_create'),  # Пример. Ссылка на создание поста
    # path('create/', AdCreateView.as_view(), name='ad_create'),  # Ссылка на создание поста
    path('review/<int:pk>/', AddComment.as_view(), name='add_comment'),  # Ссылка на создание комментария
]
