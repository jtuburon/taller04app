from django.http import HttpResponse
from django.shortcuts import render

from bson.son import SON
from pymongo import MongoClient 

from bson.json_util import dumps
from datetime import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

MONGO_DB_USER= "bigdata7"
MONGO_DB_PASSWD= "bigdata7"

# LOCAL MONGO INSTANCE PARAMS
MONGO_DB_HOST= "127.0.0.1"
MONGO_DB_PORT= 27017
MONGO_DB_NAME= "Grupo07"

# Create your views here.
def index(request):
	context= {}
	return render(request, 'taller04app/index.html', context)


def show_info(request):
	context = {}
	return render(request, 'taller04app/info_main.html', context)

def questions_main(request, page):
	client = MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)
	my_db = client[MONGO_DB_NAME]
	
	questions= my_db.movies_questions.find();
	questions_list=[]
	for q in questions: 
		q['created_date']= datetime.fromtimestamp(q['creation_date']).strftime('%Y-%m-%d %H:%M:%S')	
		questions_list.append(q)


	paginator = Paginator(questions_list, 10) # Show 25 contacts per page

	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		questions = paginator.page(1)
	except EmptyPage:
		questions = paginator.page(paginator.num_pages)
	context = {"questions_list": questions}
	return render(request, 'taller04app/questions_main.html', context)
