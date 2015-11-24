from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from bson.son import SON
from pymongo import MongoClient 

from bson.json_util import dumps
from datetime import datetime

from helpers import *
import re

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

MONGO_DB_USER= "bigdata7"
MONGO_DB_PASSWD= "bigdata7"

# LOCAL MONGO INSTANCE PARAMS
MONGO_DB_HOST= "127.0.0.1"
MONGO_DB_PORT= 27017
MONGO_DB_NAME= "Grupo07"

colors = {
	'LOCATION': 'red', 
	'PERSON':'blue', 
	'ORGANIZATION':'yellow', 
	'MONEY':'cyan', 
	'PERCENT':'green',
	'DATE':'magenta',
	'TIME':'violet',
}

# Create your views here.
def index(request):
	context= {}
	return render(request, 'taller04app/index.html', context)


def show_info(request):
	context = {}
	return render(request, 'taller04app/info_main.html', context)

def questions_main(request):
	context = {}
	return render(request, 'taller04app/questions_main.html', context)

@csrf_exempt
def questions_filter(request):
	filter_type= int(request.POST.get('filter_type', '0'))
	filter_text= request.POST.get('filter_text', '')
	page= int(request.POST.get('page', '1'))

    #0"All
    #1"Place
    #2"Person
    #3"Organization
    #4"Tags

	filter_p={}
	if filter_type!=0:
		pattern= re.compile(filter_text, re.IGNORECASE)
		filters_list=[]
		if filter_type==1:
			filter_field="title_entities.LOCATION"
			filters_list.append({filter_field: pattern})
			filter_field="body_entities.LOCATION"
			filters_list.append({filter_field: pattern})
		elif filter_type==2:
			filter_field="title_entities.PERSON"
			filters_list.append({filter_field: pattern})
			filter_field="body_entities.PERSON"
			filters_list.append({filter_field: pattern})
		
		elif filter_type==3:
			filter_field="title_entities.ORGANIZATION"
			filters_list.append({filter_field: pattern})
			filter_field="body_entities.ORGANIZATION"
			filters_list.append({filter_field: pattern})
		elif filter_type==4:
			filter_field="tags"
			filters_list.append({filter_field: pattern})

		filter_p= {"$or": filters_list}
		
	questions= get_questions_with_filter(filter_type, filter_p, page)

	context = {"questions_list": questions}
	return render(request, 'taller04app/questions_list.html', context)

def question_detail(request, question_id, ner_id):	
	question= retrieve_question_info(question_id, ner_id)
	context = {"question": question}
	return render(request, 'taller04app/question_detail.html', context)

def question_detail_info(request, question_id, ner_id):	
	question= retrieve_question_info(question_id, ner_id)
	context = {"question": question}
	return render(request, 'taller04app/question_detail_info.html', context)

def resource_info(request, uri):	
	print uri
	client = MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)
	my_db = client[MONGO_DB_NAME]
	r = my_db.dbpedia_resources.find_one({"uri": uri})
	if r!=None:
		rels=[]
		for t in r["tuples"]:
			r_t= {"p": t["p"]["value"]}
			print uri
			print t["s"]["value"]
			print "$$$$$$"

			if t["s"]["value"]== uri:
				r_t["o"]= t["o"]["value"]
			else:
				r_t["o"]= t["s"]["value"]
			rels.append(r_t)
		res= {
			"label": r["label"],
			"uri": r["uri"],
			"tuples": rels
		}
	else:
		res= None
	context = {"resource": res}
	return render(request, 'taller04app/resource_info.html', context)


@csrf_exempt
def list_trending_topics_tags(request):
	count= 250
	topics_list= get_trending_topics(count)
	response = HttpResponse(dumps(topics_list))
	response['content_type'] = 'application/json; charset=utf-8'
	return response

@csrf_exempt
def tagcloud_index(request):
	count= 250
	topics_list= get_trending_topics(count)
	context = {}
	return render(request, 'taller04app/tagcloud_main.html', context)

@csrf_exempt
def list_geo_places(request):
	geo_tweets_list= get_places_in_questions()
	response = HttpResponse(dumps(geo_tweets_list))
	response['content_type'] = 'application/json; charset=utf-8'
	return response

@csrf_exempt
def geoplaces_index(request):
	count= 250
	topics_list= get_trending_topics(count)
	context = {}
	return render(request, 'taller04app/geoplaces_main.html', context)
