from flask import Flask, jsonify, request
import os, fnmatch
import json
from flask_cors import CORS, cross_origin
app = Flask(__name__)


cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

audio_path = './audio/'
results_path = './results/'

@app.route('/')
@cross_origin()
def available_files():
	return jsonify(find())

def find():
	pattern = '*.wav'
	result = []
	for root, dirs, files in os.walk(audio_path):
		for name in files:
			if fnmatch.fnmatch(name, pattern):
				result.append(os.path.join(root, name))
	return result

def find_results():
	pattern = '*.json'
	result = []
	for root, dirs, files in os.walk(results_path):
		for name in files:
			if fnmatch.fnmatch(name, pattern):
				result.append(os.path.join(root, name))
	return result

@app.route('/results', methods = ['POST'])
@cross_origin()
def results():
	filename = request.json['filename']
	filename += '.json'
	result = open(results_path+filename,'r+')
	data = json.load(result)
	result.close()
	return jsonify(data)

def start():
	files = find()
	for filename in files:
		from summarize import summarize
		from stt import get_per_user_transcript
		from sentiment_analysis import get_sentiment_per_speaker
		sentences, sentences_to_user, speaker_transcript, speakerAmount = get_per_user_transcript(filename)
		speakers = get_sentiment_per_speaker(sentences_to_user)
		summary = summarize(sentences, sentences_to_user)
		response = {
			'transcript':speaker_transcript,
			'summary':summary,
			'emotions':speakers,
			'participation':speakerAmount
		}
		filename = filename.replace(audio_path, results_path)
		result = open(filename+'.json','w+')
		json.dump(response, result)
		result.close()

def get_one():
	filename = ''
	from summarize import summarize
	from stt import get_per_user_transcript
	from sentiment_analysis import get_sentiment_per_speaker
	sentences, sentences_to_user, speaker_transcript, speakerAmount = get_per_user_transcript(filename)
	speakers = get_sentiment_per_speaker(sentences_to_user)
	summary = summarize(sentences, sentences_to_user)
	response = {
		'transcript':speaker_transcript,
		'summary':summary,
		'emotions':speakers,
		'participation':speakerAmount
	}
	filename = filename.replace(audio_path, results_path)
	result = open(filename+'.json','w+')
	json.dump(response, result)
	result.close()
