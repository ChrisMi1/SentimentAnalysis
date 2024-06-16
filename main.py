# This is a sample Python script.

import nltk

import pandas as pa
import re
import demoji
import unicodedata as uni
from gensim import corpora
from gensim.models import LdaMulticore
from nltk.corpus import stopwords


def clean_data(text):
    text = re.sub(r"http\S+", "", text)  # remove url
    emojis = demoji.findall(text)  # replace emojis with text
    for emoji in emojis:
        text = text.replace(emoji, " " + emojis[emoji].split(":")[0])
    text = uni.normalize('NFKD', text)  # unicode normalization
    # spell = SpellChecker()
    # corrected_text = []
    # words = text.split()
    # for word in words:
    #   corrected_text.append(str(spell.correction(word)))
    # text = ' '.join(corrected_text)
    return text


def label_review(rating):
    if rating in [1, 2]:
        return 'negative'
    elif rating == 3:
        return 'neutral'
    elif rating in [4, 5]:
        return 'positive'
    else:
        return 'unknown'


def get_document_topics(lda_model, corpus):
    doc_topics = []
    for bow in corpus:
        doc_topics.append(lda_model.get_document_topics(bow))
    return doc_topics


if __name__ == '__main__':
    df = pa.read_csv('C:/Users/xrist/Desktop/ProcessLanguage/tripadvisor_hotel_reviews.csv')
    print(df.info())
    print(df.head())
    for index, reviews in df.iterrows():
        df.at[index, 'Review'] = clean_data(str(df.at[index, 'Review']))

    df['Tokenized_Review'] = df['Review'].apply(nltk.word_tokenize)
    df['Sentiment'] = df['Rating'].apply(label_review)
    data_words = df[
        'Tokenized_Review'].values.tolist()  # Converts the tokenized reviews into a list of lists, where each inner list contains tokens (words) of a single review.
    dictionary = corpora.Dictionary(
        data_words)  # Creates a Gensim dictionary object from the tokenized data. This dictionary maps each word to a unique numeric ID.
    corpus = [dictionary.doc2bow(word) for word in data_words]
    print(corpus[:1][0][:30])
    lda_model = LdaMulticore(corpus, id2word=dictionary, num_topics=5, iterations=400)
    topics = lda_model.print_topics(num_words=10)
    for topic in topics:
        print(topic)

    df['Document_Topics'] = get_document_topics(lda_model, corpus)
    print(df[['Document_Topics']].head())
