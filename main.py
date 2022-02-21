import naive_bayes as nb

def depunc(sentence):
    for char in sentence:
        if char in ".,?/;-:":
            sentence = sentence.replace(char,'')
    return sentence

def make_wordlist(file):
    wordlist = list()
    for line in file:
        line = depunc(line)
        words = line.split()
        wordlist.extend(words)
    return wordlist

posfile = open('rt-polarity.pos', 'r+')
negfile = open('rt-polarity.neg', 'r+')

pos = posfile.readlines()
neg = negfile.readlines()

pos = make_wordlist(pos)
neg = make_wordlist(neg)

nb.process_data("positive reviews", pos)
nb.process_data("negative reviews", neg)

