from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    
    # Topics URLs
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/create/', views.topic_create, name='topic_create'),
    path('topics/generate/', views.topic_generate, name='topic_generate'),
    path('topics/<slug:slug>/', views.topic_detail, name='topic_detail'),
    
    # Articles URLs
    path('articles/', views.article_list, name='article_list'),
    path('articles/generate/<int:topic_id>/', views.article_generate, name='article_generate'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    
    # Database management
    path('db/reset/', views.reset_database, name='reset_database'),
    path('db/seed/', views.seed_database, name='seed_database'),
] 