from urllib import request
from bs4 import BeautifulSoup as bs
import re
import nltk
import heapq



url  = "https://en.wikipedia.org/wiki/Automatic_summarization"
htmlDoc= request.urlopen(url)
soupobject= bs(htmlDoc, 'html.parser')
paragraphContents= soupobject.findAll('p')
  #print(paragraphContents)
allparagraphcontent=""
for paragraphcontent in paragraphContents:
    allparagraphcontent += paragraphcontent.text
# print(allparagraphcontent)

allparagraphcontent_cleanerData= re.sub(r'\[[0-9]*\]', ' ', allparagraphcontent)
allparagraphcontent_cleanedData=re.sub(r'\s+', ' ', allparagraphcontent_cleanerData)
sentences_tokens = nltk.sent_tokenize(allparagraphcontent_cleanedData)

  #print(allparagraphcontent_cleanerData)

allparagraphcontent_cleanerData= re.sub(r'[a-zA-Z]', ' ', allparagraphcontent_cleanerData)
allparagraphcontent_cleanerData= re.sub(r'\s+', ' ', allparagraphcontent_cleanerData)


# crating sentence tokens




#print(sentences_tokens)
word_tokens    = nltk.word_tokenize(allparagraphcontent_cleanedData)
#print(sentences_tokens)
#print(word_tokens)

#calculate the frequency

stopwords = nltk.corpus.stopwords.words('english')
word_frequencies = {}

for word in word_tokens:
    if word not in stopwords:
        if word not in word_frequencies:
            word_frequencies[word]= 1
        else:
            word_frequencies[word]+= 1

#print(word_frequencies)
# calculate weighted frequency

maximum_frequency_word= max(word_frequencies.values())

#print(maximum_frequency_word)

for word in word_frequencies.keys():
    word_frequencies[word]= (word_frequencies[word]/maximum_frequency_word)


#print(word_frequencies)

#calculate sentencess score with each word weighted frequency

sentences_score={}


for sentence in sentences_tokens:
    for word in nltk.word_tokenize(sentence.lower()):
        if word in word_frequencies.keys():
            if(len(sentence.split(' ')))<30 :
                if sentence not in sentences_score.keys():
                    sentences_score[sentence]=word_frequencies[word]
                else:
                    sentences_score[sentence]+= word_frequencies[word]



#print(sentences_score)


summary_textsummarize= heapq.nlargest(2,sentences_score,key=sentences_score.get)
print(summary_textsummarize)



