from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login, name='login'),
    path('api/q/generalstat/', views.generalstat, name='generalstat'),
    path('api/q/book/edit/', views.edit_book, name='editbook'),
    path('api/q/book/add/', views.submit_book, name='submitbook'),
    path('api/q/book/', views.query_book, name="querybook"),
    path('api/whoami/', views.whoami, name='whoami'),
    path('accounts/logout/', views.logout_url, name="logout"),
    path('api/news/', views.news, name="new"),
]
