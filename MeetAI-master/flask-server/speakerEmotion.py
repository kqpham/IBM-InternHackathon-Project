class SpeakerEmotion:
    def __init__(self, sadness, joy, fear, disgust, anger, lineCount, speaker):
        self.sadness = sadness
        self.fear = fear
        self.joy = joy
        self.disgust = disgust
        self.anger = anger
        self.lineCount = lineCount
        self.speaker = speaker

    def updateEmotions(self, sadness, joy, fear, disgust, anger):
        self.sadness += sadness
        self.fear += fear
        self.joy += joy
        self.disgust += disgust
        self.anger += anger
        self.lineCount += 1

    def getAverageDictionary(self):
        output = {}
        output['speaker'] = self.speaker
        output['sadness'] = self.sadness / self.lineCount
        output['fear'] = self.fear / self.lineCount
        output['joy'] = self.joy / self.lineCount
        output['disgust'] = self.disgust / self.lineCount
        output['anger'] = self.anger / self.lineCount
        output['lineCount'] = self.lineCount
        return output


    


