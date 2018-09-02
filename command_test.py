import nltk
from nltk.corpus import wordnet


class Command:
    def __init__(self, command):
        self.command = command
        self.direction = ''
        self.json_data = ''
        pass

    def generateList(self,command):
        if command == '':
            command = self.command
        tags = nltk.word_tokenize(command)
        pos_tag = nltk.PerceptronTagger().tag(tags)
        return pos_tag

    def work_words_extraction(self,pos_tags):
        work_words = []
        for word, tag in pos_tags:
            if tag == 'VB' or tag == 'RP' or tag == 'CD':
                work_words.append(word)
        return work_words

    def noun_extraction(self,pos_tags):
        noun_words = []
        for word, tag in pos_tags:
            if tag[:2] == 'NN':
                noun_words.append(word)
        return noun_words

    def get_synsets(self,word):
        return wordnet.synsets(word)

    def name_entity_recognition(self):
        noun_words = self.noun_extraction(self.generateList(self.command))
        work_words = self.work_words_extraction(self.generateList(self.command))
        for i in noun_words:
            for j in work_words:
                nw = self.get_synsets(i)
                ww = self.get_synsets(j)
                for n in nw:
                    for w in ww:
                        if n.wup_similarity(w) is not None:
                            print("noun word : {}\nDefinition: {}\n\nwork word : {}\nDefinition: {}\n\nSimilarty : {}\n\n-----------------------\n\n".format(n,n.definition(),w,w.definition(),n.wup_similarity(w)))









test_list = ['switch off the lights'
    , 'volume down the tv'
    , 'open the door'
    , 'wake me up at 7:00 am'
    , 'mute the tv'
    , 'who is outside'
    , 'play a music'
    , 'mute all noices'
    , 'change the channel'
    , 'pick up the call'
    , 'talk to her'
    , 'who is in the phone'
    , 'tell him that I will be there in the meeting'
    ,'switch to Fox News'
    ,'play gulabi aankhen']

for i in range(len(test_list)):
    obj = Command(test_list[i])
    print(obj.generateList(''))
    obj.name_entity_recognition()

