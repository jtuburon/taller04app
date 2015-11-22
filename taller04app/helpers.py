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
	'MOVIE':'brown',
	'OTHER':'gray',
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
		get_spotlight_recognized_resources(q)



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



def get_spotlight_recognized_resources(q):
	client = MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)
	my_db = client[MONGO_DB_NAME]
	q_res= my_db.questions_spotlight_resources.find_one({"question_id": q['question_id']})
	update_html_with_spotlight_resources(q, 'title', q_res)
	update_html_with_spotlight_resources(q, 'body', q_res)
	update_html_with_spotlight_resources(q, 'answers', q_res)
	

def update_html_with_spotlight_resources(q, attribute, res):
	if attribute in res.keys():
		if attribute =="answers":
			for a in res[attribute]:
				answ= find_answer_object(q, a["answer_id"])
				print answ
				answ["body"]=generate_html_from_spotlight(answ, attribute, a)
		else:
			if 'Resources' in res[attribute].keys():
				q[attribute]=generate_html_from_spotlight(q, attribute, res)

def find_answer_object(q, answer_id):
	for a in q["answers"]:
		if a["answer_id"]== answer_id:
			return a
	return None


def generate_html_from_spotlight(obj, attribute, res):
	sources=None
	if attribute=="answers":
		text= obj["body"]
		sources= res['Resources']
	else:
		text= obj[attribute]
		sources= res[attribute]['Resources']
	
	offset_increase = 0
	if sources != None:
		for r in sources:			
			entity= r["@surfaceForm"]
			offset= int(r["@offset"]) + offset_increase
			entity_uri= r["@URI"]
			extract_entity_type(r)

			start= text[0:offset]
			header_s="<strong><span style='color: "+ colors[extract_entity_type(r)] +"'>"
			header_e="</span></strong>"
			middle=header_s+  entity + header_e
			end= text[offset+ len(entity):]
			offset_increase += len(header_s) + len(header_e)
			text = start + middle + end
	return text

def extract_entity_type(res):
	kind = ""
	types= res["@types"].lower()
	for k in colors.keys():
		if k.lower() in types:
			kind = k
	if kind== "":
		return "OTHER"
	return kind
