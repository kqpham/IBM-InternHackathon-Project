from ibm_watson import SpeechToTextV1, NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from os.path import join, dirname
import json

speech_to_text = SpeechToTextV1(
    iam_apikey='*****',
    url='https://stream.watsonplatform.net/speech-to-text/api')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api',
    iam_apikey='****')

def analyse_text(audio_file):
	result = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/wav',
        speaker_labels='true'
    ).get_result()

	results = result['results']
	timestamps = []

	for res in results:
		current_timestamps = res['alternatives'][0]['timestamps']
		current_timestamps[-1][0] += '.'
		for t in current_timestamps:
			timestamps.append(t)

	start_to_wordMap = {}
	for stamp in timestamps:
		start_to_wordMap[stamp[1]] = stamp[0]


	speaker_labels = result['speaker_labels']
	current_speaker = speaker_labels[0]['speaker']
	speaker_transcript = [{
		'speaker':current_speaker,
		'text':''
	}]
	for label in speaker_labels:
		label['from']
		speaker = label['speaker']
		if speaker != current_speaker:
			speaker_transcript[-1]['text'] = speaker_transcript[-1]['text'][:-1]
			if (speaker_transcript[-1]['text'][-1] != '.'):
				speaker_transcript[-1]['text'] += '.'
			current_speaker = speaker
			speaker_transcript.append({
				'speaker':current_speaker,
				'text':''
			})
		speaker_transcript[-1]['text'] += start_to_wordMap[label['from']] + ' '
	sentences = []
	sentences_to_speaker = {}
	for paragraph in speaker_transcript:
		text = paragraph['text'].replace('%HESITATION', '')
		text = paragraph['text'].replace('  ', ' ')
		lines = text.split('.')
		for line in lines:
			line = line.strip()
			if line != '':
				sentences_to_speaker[line] = paragraph['speaker']
				sentences.append(line)
	return sentences, sentences_to_speaker

def nlu_text(text):
	response = natural_language_understanding.analyze(
    text=text,
    features=Features(
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        keywords=KeywordsOptions(emotion=True, sentiment=True,
                                 limit=2))).get_result()
	return response

with open(join(dirname(__file__), './.', 'en-US_Broadband_sample1.wav'), 'rb') as audio_file:
	sentences, sentences_to_speaker = analyse_text(audio_file)
	print(sentences)
	print(sentences_to_speaker)
