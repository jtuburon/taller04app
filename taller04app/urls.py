from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^info/main$', views.show_info),
    url(r'^questions/main$', views.questions_main, name='questions_main'),
]