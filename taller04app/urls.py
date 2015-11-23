from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^info/main$', views.show_info),
    url(r'^questions/main/(?P<page>[0-9]+)$', views.questions_main, name='questions_main'),
    url(r'^questions/filter$', views.questions_filter, name='questions_filter'),
    url(r'^question/detail/(?P<question_id>[0-9]+)/(?P<ner_id>[0-9]+)$', views.question_detail, name='question_detail'),
    url(r'^question/detail/info/(?P<question_id>[0-9]+)/(?P<ner_id>[0-9]+)$', views.question_detail_info, name='question_detail_info'),
    url(r'^resource/info/(?P<uri>.+)$', views.resource_info, name='resource_info'),
    url(r'^tagcloud/index$', views.tagcloud_index, name='tagcloud_index'),
    url(r'^get_trending_topics$', views.list_trending_topics_tags, name='list_trending_topics_tags'),
    url(r'^geoplaces/list$', views.list_geo_places, name='list_geo_places'),
    url(r'^geoplaces/index$', views.geoplaces_index, name='geoplaces_index'),
]