from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', views.create_user_form, name='create_user_form'),
    path('create_user/', views.create_user, name='create_user'),
    path('accounts/profile/', views.profile, name='profile'),
]