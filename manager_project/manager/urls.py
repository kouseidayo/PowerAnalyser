from django.urls import path
from . import views


urlpatterns = [
    path('post_ajax', views.AjaxAPI.as_view(), name='post_ajax'),
    path('main', views.main_page, name='main_page'),
    path('main_kaiouken', views.main_page_kaiouken, name='main_page_kaiouken'),
    path('reason', views.reason_page, name='reason_page'),
]