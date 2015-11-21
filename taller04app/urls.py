from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^info/main$', views.show_info),
    url(r'^questions/main/(?P<page>[0-9]+)$', views.questions_main, name='questions_main'),
    url(r'^question/detail/(?P<question_id>[0-9]+)/(?P<ner_id>[0-9]+)$', views.question_detail, name='question_detail'),
    url(r'^question/detail/info/(?P<question_id>[0-9]+)/(?P<ner_id>[0-9]+)$', views.question_detail_info, name='question_detail_info'),
]