# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pa
import re
import demoji
import unicodedata as uni

def clean_data(text):
    text = re.sub(r"http\S+", "", text) #remove url
    emojis = demoji.findall(text) #replace emojis with text
    for emoji in emojis:
        text = text.replace(emoji, " " + emojis[emoji].split(":")[0])
    text = uni.normalize('NFKD', text) #unicode normalization
#    spell = SpellChecker()
#    corrected_text = []
#    words = text.split()
#    for word in words:
#        corrected_text.append(spell.correction(word))
#    text = ' '.join(corrected_text)

    #text = str(TextBlob(text).correct())
    return text


df = pa.read_csv('C:/Users/xrist/Desktop/ProcessLanguage/tripadvisor_hotel_reviews.csv')
print(df.info())
print(df.head())
for index, reviews in df.iterrows():
    df.at[index, 'Review'] = clean_data(str(df.at[index, 'Review']))
