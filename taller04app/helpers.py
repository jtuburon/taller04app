from bson.son import SON
from pymongo import MongoClient 
from bson.json_util import dumps
from datetime import datetime
import re

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

def generate_entities_dict(q):
	client = MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)
	my_db = client[MONGO_DB_NAME]
	q_entities= my_db.movies_questions_entities.find_one({"question_id": q['question_id']})

	words = {}

	if q_entities != None:	
		for key in q_entities["title_entities"].keys():
			for w in q_entities["title_entities"][key]:
				words[w]= key 

		for key in q_entities["body_entities"].keys():
			for w in q_entities["body_entities"][key]:
				words[w]= key 

		for a_o in q_entities["answers_entities"]:
			for key in a_o["entities"]:
				for w in a_o["entities"][key]:
					words[w]= key
		return words
	else:
		return None

def highlight_entities(q, ner_id):
	print ner_id
	if ner_id=="1":
		words = generate_entities_dict(q);
		if words != None:
			regex= generate_pattern(words)
			update_html(q, 'title', regex, words)
			update_html(q, 'body', regex, words)
			update_html(q, 'answers', regex, words)
	elif ner_id=="2":
		print "-"



def update_html(q, attribute, regex, words):
	if attribute=="answers":
		for a in q[attribute]:
			text= a['body']
			a['body']= update_text(text, regex, words)
	else:
		text= q[attribute]
		q[attribute]= update_text(text, regex, words)

def update_text(text, regex, words):
	i = 0; 
	output = ""
	for m in regex.finditer(text):
		output += "".join([text[i:m.start()], "<strong><span style='color: "+ colors[words[text[m.start():m.end()]]] + "'>", text[m.start():m.end()], "</span></strong>"])
		i = m.end()
	output+= text[i:]
	return output

def generate_pattern(words):
	words_list = ["(\\b"+ x+ "\\b)" for x in words.keys()]
	regex= "|".join(words_list)
	return re.compile(regex)

def retrieve_question_info(question_id, ner_id):	
	client = MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)
	my_db = client[MONGO_DB_NAME]
	question= my_db.movies_questions.find_one({"question_id": int(question_id)});
	question['created_date']= datetime.fromtimestamp(question['creation_date']).strftime('%Y-%m-%d %H:%M:%S')	
	question['tags_array']= [x.encode('UTF8') for x in question['tags']] 	
	for a in question['answers']:
		a['created_date']= datetime.fromtimestamp(a['creation_date']).strftime('%Y-%m-%d %H:%M:%S')	
	highlight_entities(question, ner_id)
	return question