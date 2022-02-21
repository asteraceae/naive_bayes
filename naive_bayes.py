#0 is true, 1 is false
from collections import Counter
import random

class naive_bayes():

    def __init__(self):
        self.features = dict()
        self.features_l = dict()
        self.features_p = dict()
        self.features_wp = dict()
        self.validation = list()
        self.results = open("results.txt", "w+")
    
    def process_data(self, feature_name, wordlist, wordlist2):
        self.create_feature(feature_name, wordlist)
        self.features_l[feature_name] = wordlist2

    def fit(self, validation):
        self.features_p = dict()
        self.features_wp = dict()
        self.validation = validation
        for f in self.features:
            self.features_wp[f] = dict()
            p = self.calc_class_prob(f)
            self.features_p[f] = p
            for word in self.features[f]:
                if word not in self.features_wp[f]:
                    self.features_wp[f][word] = self.calc_prob(f, word)
        print("Validating...\n")
        self.evaluate(validation)

    def evaluate(self, test):
        true = 0
        false = 0
        winning_prob = ["none", 0]
        found = False
        foundc = ""
        for line in test:
            self.results.write(f"{line}")
            found = False
            winning_prob = ["none", 0]
            wordlist = line.split()
            for f in self.features:
                prob = 1 * self.features_p[f]
                for word in wordlist:
                    try:
                        prob = prob * self.features_wp[f][word]
                    except:
                        '''print(f"word {word} wasn't in list of feature {f}... adding it now and reevaluating")
                        for x in self.features:
                            self.features[x].append(word)
                        self.fit(self.validation)'''
                        prob = prob * 1
                self.results.write(f" | {prob}")
                if prob > winning_prob[1]:
                    winning_prob[0] = f
                    winning_prob[1] = prob
            for c in self.features_l:
                if line in self.features_l[c] and winning_prob[0] == c:
                    found = True
                    foundc = c
            if found:
                true += 1
            else:
                false += 1
            self.results.write(f" | Winning prob: {prob}, {winning_prob[0]}, actual:{c} \n\n")
            
        
            
        print(f"\nCorrectly identified: {true} / {len(test)} lines")
        print(f"Incorrectly identified: {false} / {len(test)} lines")
        print(f"Accuracy: {true/len(test)}")

    def create_feature(self, feature, data):
        if feature in self.features:
            print("Can't create new features dict when a dict for that feature already exists! error 0")
            return 1
        else:
            self.features[feature] = data
            return 0

    def print_features(self):
        for x in self.features:
            print(x, "\n")

    def calc_prob(self, feature, word):
        if feature not in self.features:
            print("Can't calculate the P of a word of a feature not in the features dict! error 2.")
            return 1
        else:
            if word not in self.features[feature]:
                print("Can't calculate the P of a word not in the features dict! error 3.")
                return 1
            else:
                counts = Counter(self.features[feature])
                nominator = counts[word]
                denominator = len(self.features[feature])
                return (nominator/denominator)

    def calc_class_prob(self, feature):
        if feature not in self.features:
            print("Can't calculate the P of feature not in the features dict! error 4.")
            return 1    
        else:
            denominator = 0
            for f in self.features:
                denominator += len(f)
            nominator = len(self.features[feature])
            return (nominator/denominator)


def depunc(sentence):
    for char in sentence:
        if char in ".,?/;-:":
            sentence = sentence.replace(char,'')
    return sentence

def clean(file):
    wordlist = list()
    for line in file:
        line = depunc(line)
        wordlist.append(line)
    return wordlist

def make_wordlist(file, stop):
    wordlist = list()
    for line in file:
        line = depunc(line)
        words = line.split()
        for word in words:
            if word in stop:
                words.remove(word)
        wordlist.extend(words)
    return wordlist

def split_sets(file):
    l = []
    random.shuffle(file)
    train_data = file[:int((len(file)+1)*.70)] #Remaining 80% to training set
    train_data = make_wordlist(train_data, stop)
    test_v_data = file[int((len(file)+1)*.70):]
    test_data = test_v_data[int((len(test_v_data)+1)*.50):]
    validation_data = test_v_data[:int((len(test_v_data)+1)*.50)]
    return [train_data, test_data, validation_data]

def count_word(file):
    dict = {}
    for x in file:
        x = depunc(x)
        words = x.split()
        for y in words:
            if y in dict:
                dict[y] += 1
            else:
                dict[y] = 1
    return dict


posfile = open('rt-polarity.pos', 'r+')
negfile = open('rt-polarity.neg', 'r+')
stopfile = open('stop.txt', 'r+')

pos = posfile.readlines()
neg = negfile.readlines()
stop = stopfile.readlines()

posfile.close()
negfile.close()
stopfile.close()

pos = clean(pos)
neg = clean(neg)

pos_lists = split_sets(pos)
neg_lists = split_sets(neg)

test_data = pos_lists[1] + pos_lists[2]
v_data = pos_lists[2] + pos_lists[2]

random.shuffle(test_data)
random.shuffle(v_data)

nb = naive_bayes()

nb.process_data("positive reviews", pos_lists[0], pos)
nb.process_data("negative reviews", neg_lists[0], neg)
nb.fit(v_data)
nb.evaluate(test_data)
