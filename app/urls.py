from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('job-list/', views.job_list, name='job_list'),
    #path('job_detail/<int:id>', views.job_detail, name='job_detail'),
    #path('job_details', views.job_details, name='job_details'),
    path('job-search/', views.job_search, name='job_search'),
    path('new_feed/', views.new_feed, name='new_feed'),
    path('parse-rss/', views.parse_rss, name='parse_rss')
]