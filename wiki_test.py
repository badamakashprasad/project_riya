import nltk
sentence = 'switch off the lights. turn the volume down of the tv. change the channel'
sentence = nltk.sent_tokenize(sentence)
for i in range(3):
    words = nltk.word_tokenize(sentence[i])
    tag = nltk.ne_chunk(nltk.pos_tag(words))
    print(tag)

