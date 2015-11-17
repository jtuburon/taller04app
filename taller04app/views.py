from django.http import HttpResponse
from django.shortcuts import render

from bson.son import SON
from pymongo import MongoClient 

from bson.json_util import dumps
from datetime import datetime

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

def questions_main(request):
	client = MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)
	my_db = client[MONGO_DB_NAME]
	
	questions= my_db.movies_questions.find();
	questions_list=[]
	for q in questions: 
		q['created_date']= datetime.fromtimestamp(q['creation_date']).strftime('%Y-%m-%d %H:%M:%S')	
		questions_list.append(q)

	context = {"questions_list": questions_list}
	return render(request, 'taller04app/questions_main.html', context)
