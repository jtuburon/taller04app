from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^info/main$', views.show_info),
    url(r'^questions/main/(?P<page>[0-9]+)$', views.questions_main, name='questions_main'),
]