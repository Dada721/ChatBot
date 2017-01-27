# -*- coding: utf-8 -*-
from uuid import uuid4
from datetime import datetime, timedelta

from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from pymongo import MongoClient

from flask import Flask, session, url_for, redirect


import os
import aiml
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from geopy.geocoders import Nominatim
import div_difflib
import itertools
from chatterbot.response_selection import get_first_response
from flask import Flask, request
from flask_restful import Resource, Api
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
stop_words = set(stopwords.words("english"))
user_str_ip=0
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sid = str(uuid4())



kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
    kernel.saveBrain("bot_brain.brn")


def get_uip(sentence):
	userinput2 = word_tokenize(sentence)
	# removing punctuations
        userinput2 = filter(lambda x: x not in string.punctuation, userinput2)
	# removing stopwords
        userinput2 = filter(lambda x: x not in stop_words, userinput2)
        userinput2=" ".join(userinput2)
	return userinput2;



if_str=" "

bot = ChatBot(
	"Tranning",
	storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
	logic_adapters=[
	    {
	        'import_path': 'chatterbot.logic.BestMatch'
	    },
	    {
	        'import_path':'chatterbot.logic.LowConfidenceAdapter',
	        'threshold':0.85,
	        'default_response':if_str
	    }
        ],
	filters=[
        	'chatterbot.filters.RepetitiveResponseFilter'
	])
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train(
    "chatterbot.corpus.HDFC_CORPUS.mygreetings",
        "chatterbot.corpus.HDFC_CORPUS.easyhealth_plan",
        "chatterbot.corpus.HDFC_CORPUS.div_synonyms",
        "chatterbot.corpus.HDFC_CORPUS.click2retirehdfc",
        "chatterbot.corpus.HDFC_CORPUS.click2invest_hdfc",
        "chatterbot.corpus.HDFC_CORPUS.click2protect_hdfc",
		"chatterbot.corpus.HDFC_CORPUS.cancercare"
)

chatbot = ChatBot("Synonym",logic_adapters=[

                      {
                          'import_path': 'chatterbot.logic.BestMatch'
                      },

                      {
                          'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                          'threshold': 0.60,
                          'default_response': if_str
                      }

                  ])
chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train(
	"chatterbot.corpus.HDFC_CORPUS.mygreetings",
        "chatterbot.corpus.HDFC_CORPUS.easyhealth_plan",
        "chatterbot.corpus.HDFC_CORPUS.div_synonyms",
        "chatterbot.corpus.HDFC_CORPUS.click2retirehdfc",
        "chatterbot.corpus.HDFC_CORPUS.click2invest_hdfc",
        "chatterbot.corpus.HDFC_CORPUS.click2protect_hdfc",
		"chatterbot.corpus.HDFC_CORPUS.cancercare"
)
chatbot.set_trainer(ListTrainer)

out=" ["
op_list2=[] #for storing bot response in the form of list

#listing  all policies so that later bot compares and knows about which policy the user is talking
p1 = "click 2 protect plus"
p2 = " click 2 retire"
p3 = " easy health plan"
p4 = " click 2 invest ulip"
p7=" cancer care"

p5 = p1 + p2 + p3 + p4 + p7  #concatenating all strings

p6 = p5.lower().split(" ") #converting it to list (to extract individual words


op_list=[]

store_list=[]

#global mymatch
#mymatch = "sdcscscsddcsdccsdcscscsdcsdcsdcsdcsdcsdcsdc"

list4=[]

counter = 0

def incrementcounter():
      global counter
      counter=counter+1
      return counter

def set_counter_to_zero():
    global counter
    counter=0
    return counter



global synonym
def div_synonym():
    synonym = op_list[(len(op_list) - 2)]
    synonym = " ".join(( synonym.text ,"i am synonym of xyz"))
    response = chatbot.get_response(synonym)
    return response.text

def loadVar():
	global mymatch
	mymatch = ""
	print "mymatch Loaded"


def nearby_atm(lat,long):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    location = geolocator.reverse(" ".join((lat,",",long)))
    return location.address

def my_back_track(sentence1,session):
	if(counter<3):

			print sentence1
			message ="Can you please me more specific with your query??"
			incrementcounter()
	else:
		message ="Sorry I am unable to understand your question. I can assist you to know more about HDFC Life's Insurance Policies\n " \
			"Protection \n Investment \n Savings \n Pension \n Health \n \n Please let us know what type of insurance you would be interested in and I could explain the same in detail."

	return message

        # back_on_track()


def find_longest_word(word_list):
    longest_word = ''
    for word in word_list:
        if len(word) > len(longest_word):
            longest_word = word
    return longest_word


flag=0
flag2=0
def backtrack(message,sid,sentence,lat,lon,sentence1):

	print sentence
	print mymatch
	counter1=incrementcounter()
	mystr=" ".join((sentence," ",mymatch))
	with open(
             'spell_correcter.txt') as f:
		lines2 = f.readlines()


	lines2 = " ".join(lines2)

	userinput2 = word_tokenize(lines2)

	# removing punctuations
	userinput2 = filter(lambda x: x not in string.punctuation, userinput2)

	# removig stopwords
	userinput2 = filter(lambda x: x not in stop_words, userinput2)

#	userinput2 = " ".join(userinput2)

	b = str(sentence)
        b1 = b.split(" ")

	myword = str(find_longest_word(b1))
	print myword

	sorted_list = sorted(userinput2, key=lambda x: div_difflib.SequenceMatcher(None, x, myword).ratio(), reverse=True)
	ratio = div_difflib.SequenceMatcher(None, sorted_list[0], myword).ratio()
	response = chatbot.get_response(mystr);
	mymessage=" "
	if (not (not mymatch) and "premium" in sentence1):
		message = "To calculate your premium you have to provide following details, your age please"
		global flag2
		flag2 = 1
		global mymessage
		mymessage=message
	elif (flag2 == 1):
		message = "Enter Sum Assured Policy Amount please?"
		global flag2
		flag2 = 2

		global mymessage
		mymessage = message
	elif (flag2 == 2):
		message = "Finally Enter Policy Term Duration"
		global flag
		flag2 = 3
	elif(flag2==3):
		message="Your Premium amount for this policy will be Rs. 4112/-"
		global mymessage
		mymessage = message
		global flag2
		flag2=0

	else:

		message = response.text;
		global flag2
		flag2 = 0
	print sorted_list[0]
	print (message)
	print ratio

	if(ratio < 0.70 or if_str==message):

		if (not(not mymatch) and "thanks" in sentence1):
			message="Thank You for chatting with me. May I have your name, phone number and email address please?"
			global flag
			flag=1
			user_name = "";
			phone = ""
			email_id = ""
		elif (flag == 1):
				sentence2 = sentence1.split(" ");
				#user_name = sentence2[0]
				#phone = sentence2[1]
				#email_id = sentence2[2];
				#message = " ".join(("Thank you ", user_name,
				#					" for the contact details. Our expert would call you within 24 to 48 business hours."))
				message="Thank you for the contact details. Our expert would call you within 24 to 48 business hours."
				global flag
				flag = 0


		elif(not mymessage):
				print 'backTrack'
				message = my_back_track(sentence1,sid)
				global flag
				flag = 0
				global flag2
				flag2 = 0

	else:

		set_counter_to_zero()

	return message;



def get_message(message,session,sentence,lat,long,sentence1):
	global mymatch
	bm = str(message)
        lines = bm.lower().split(" ")
	op_list2=lines
	list3 = list(set(op_list2).intersection(p6))
	list4 = sorted(list3, key=lambda k: p6.index(k))
#	print " ".join((message,"SDCSCSD"))
	if (message!=if_str):
		mymatch = " ".join(list4)
#	else:
#		mymatch=""
	if(message==if_str):
#		if(mymatch==""):
		message = backtrack(message,session,sentence,lat,long,sentence1)

	return message;


class Messages(Resource):
        def get(self):
                sentence = request.args.get("message")
		if not sentence:
				return {'success':0,'message':'Please Provide me the conversation Message'}
		session_id = request.args.get("session");
		if not session_id:
				return {'success':0,'message':'Please Provide me the Conversation Session ID'}
		lat = request.args.get("lat");
		if not lat:
				lat = ""
		long = request.args.get("long");
		if not long:
				long = ""
		sentence1 = sentence
		sentence = get_uip(sentence)
		predicted_sentence = bot.get_response(sentence)
		op_list.append(predicted_sentence)
		predicted_sentence = get_message(predicted_sentence.text,session_id,sentence,lat,long,sentence1);
		print(predicted_sentence);
		return {'success':1,'message':predicted_sentence,'session':session_id};
	def post(self):
		sentence = request.values.get("message")
		if not sentence:
				print('Please Provide me the conversation Message')
				return {'success':0,'message':'Please Provide me the conversation Message'}
		session_id = request.values.get("session");
		if not session_id:
				print('Please Provide me the Conversation Session ID')
				return {'success':0,'message':'Please Provide me the Conversation Session ID'}

		lat = request.values.get("lat");
		if not lat:
				lat=""
#		print(lat)
#		if not lat:
#				print('Please Provide me the latitude')
#				return {'success':0,'message':'Please Provide me the latitude'}
		long = request.values.get("long");
		if not long:
				long=""
#		print(long)
#		if not long:
#				print('Please Provide me the longtitude')
#				return {'success':0,'message':'Please Provide me the longtitude'}
		sentence1 = sentence
		sentence = get_uip(sentence);
		predicted_sentence = bot.get_response(sentence)
		op_list.append(predicted_sentence)
		predicted_sentence = get_message(predicted_sentence.text,session_id,sentence,lat,long,sentence1);
		print(predicted_sentence);
		return {'success':1,'message':predicted_sentence,'session':session_id};


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
api = Api(app)

@app.after_request
def apply_caching(response):
#	response.headers['Server'] = "Gray matrix service"
	return response


loadVar()

api.add_resource(Messages,'/msg')

app.run(host="0.0.0.0")

