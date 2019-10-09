from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, EmotionOptions
from os.path import join, dirname
from speakerEmotion import SpeakerEmotion
import json

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api',
    iam_apikey='*****')

def get_sentiment(text):
	response = natural_language_understanding.analyze(
    text=text,
    features=Features(
		emotion=EmotionOptions()
    )).get_result()
	return response

def get_sentiment_per_speaker(speaker_dict):
    sentiment_dict = {}
    for text, speaker in speaker_dict.items():

        try:
            sentiments = get_sentiment(text)['emotion']['document']['emotion']
            print(sentiments)
        except:
            continue

        if (speaker in sentiment_dict):
            sentiment_dict[speaker].updateEmotions(sentiments['sadness'], sentiments['joy'], sentiments['fear'], sentiments['disgust'], sentiments['anger'])
        else:
            sentiment_dict[speaker] = SpeakerEmotion(sentiments['sadness'], sentiments['joy'], sentiments['fear'], sentiments['disgust'], sentiments['anger'], 1, speaker)

    output = []
    for spk, spkEmotion in sentiment_dict.items():
        output.append(spkEmotion.getAverageDictionary())

    return json.dumps(output)
