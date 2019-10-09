import numpy as np
import pandas as pd
import nltk
nltk.download('punkt') # one time execution
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

vector_size=300
word_embeddings = {}
f = open('glove.6B.300d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

# function to remove stopwords
def remove_stopwords(sen):
	sen_new = " ".join([i for i in sen if i not in stop_words])
	return sen_new

def summarize(sentences, sentencesToUser):

	# remove punctuations, numbers and special characters
	clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

	# make alphabets lowercase
	clean_sentences = [s.lower() for s in clean_sentences]

	# remove stopwords from the sentences
	clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

	sentence_vectors = []
	for i in clean_sentences:
		if len(i) != 0:
			v = sum([word_embeddings.get(w, np.zeros((vector_size,))) for w in i.split()])/(len(i.split())+0.001)
		else:
			v = np.zeros((vector_size,))
		sentence_vectors.append(v)

	sim_mat = np.zeros([len(sentences), len(sentences)])
	for i in range(len(sentences)):
		for j in range(len(sentences)):
			if i != j:
				sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,vector_size), sentence_vectors[j].reshape(1,vector_size))[0,0]

	nx_graph = nx.from_numpy_array(sim_mat)
	scores = nx.pagerank(nx_graph)
	ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
	# Extract top 10 sentences as the summary
	results = [ {'speaker':sentencesToUser[ranked_sentences[i][1]],'line':ranked_sentences[i][1]} for i in range(len(sentences))]
	return results
