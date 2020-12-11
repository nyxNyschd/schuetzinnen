#Code von Frau Mihaljevic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
nlp = spacy.load('en_core_web_sm')
corpus = ["I'd like an apple",
          "An apple a day keeps the doctor away",
          "Never compare an apple to an orange",
          "I prefer scikit-learn to Orange",
          "The scikit-learn docs are Orange and Blue"]
def spacy_tokenizer(doc):
    nlp.vocab["!"].is_punct = False
    return [token.lemma_ for token in nlp(doc) if not (token.is_punct or token.is_stop)]
# Probieren SIe hier verschiedene Optionen für den TfidfVectorizer aus
# es macht Sinn, in die Doku zu gucken
# Vergleichen SIe die Ergebnisse mit denen für den default tokenizer, also TfidfVectorizer()
vectorizer = TfidfVectorizer(tokenizer=spacy_tokenizer)#(stop_words='english')
X = vectorizer.fit_transform(corpus)
X.toarray()
print(vectorizer.get_feature_names())
query = ['the first database document']
query_t = vectorizer.transform(query)
query_t.toarray()
cosine_similarity(X, query_t)
cosine_similarity(X,X)