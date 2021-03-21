# the code shown here can be used to clean text, tag words with parts of speech tags and
# select specific tags to extract, according to tasks at hand. I was looking at verbs specifically

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag


def preprocess(sent):
    '''
    This function takes in a string and tokenizes according to NLTK's tokenizing function which tokenizes the word semantically and not based on space.  the tokenized string then gets tagged with parts of speech tags
    '''
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent


def punctremove(sent):
    '''
    this function takes in a string and outputs a string without any email addresses, urls, or punctuation. The punctuation regex has been customized to include numbers and apostrophes so context is left intact for POS tagging.
    '''
    # remove html tags that contain hyperlinks
    notag = re.sub(r'<[^>]+>', '', sent)
    # remove email addresses from email body
    noemail = re.sub(
        r'(<)?[a-zA-Z0-9_.+-]+@[a-zA-z0-9]*.[a-zA-z0-9]*.(com|net|ca)(>)?', '', notag)
    noemail
    # remove url
    nourl = re.sub(
        r'\s*(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?', '', noemail)
    # remove num and punctuations from email body, a space is included to seperate different words and prevent them from being smushed together. #numbers not removed, apostrohe not removed, special curly quotations added
    alphnm = re.sub(r'[!""#$%&''()*+,.\-/:?;<=>@[\]^_`{|}~“”]', '', nourl)
    return alphnm

# Lemmatizing function for strings, need to create a different one for lists


def lemstring(sent):
    import nltk
    from nltk.stem import WordNetLemmatizer
    lm = WordNetLemmatizer()
    elemstring = ""
    elist = sent.split()  # this is done to tokenize the email body string of e1
    for i in range(len(elist)):  # for each word in the list
        word = elist[i]
        word = lm.lemmatize(word, pos='v')
        word = word.strip()
        elemstring += " "+word
    return elemstring


# chunking thing together
# Create parser and pattern for verb phrases
# all forms of verbs, nouns, and prepositions
patternV = 'VP: {<VB>*<VBD>*<VBG>*<VBP>*<VBN>*<VBZ>*<MD>*<NN>*<JJ>*}'
# all forms of verbs, nouns, and prepositions
patternV2 = 'VP: {<VB.?>*<MD.?>*<NN>*<JJ>*}'
# chinking
patternVC = r'''
VP: {<.*>+}          # Chunk everything
   }<NNP|CD>+{       #chink only proper nouns and cardinal digits
'''
# predefine a pattern as variable before inputting into function


def phraseparse(sent, pattern):
    '''
    this function has 2 inputs, a string and a predefined pattern
    using different parts of speech tags, regex style patterns are created to only include or exclude certain tags based on the use chinking or chunking. those patterns determine which tags and their words are outputted
    '''
    listvb = []
    cp = nltk.RegexpParser(pattern)
    cs = cp.parse(sent)
    for subtree in cs.subtrees():
        lbtree = subtree.label()
        if lbtree == 'VP':
            listvb.append(subtree)
    return listvb


def treeparse(x):
    '''
    Parses the POS tagged word tree that is returned by a tagging function and only returns the words without the tags. returns a list of words with stop words removed
    '''
    #from nltk.corpus import stopwords
    # stop_words = list(stopwords.words('english'))#get rid of stopwords from filtered wordlist
    smple = []
    words = []
    for i in range(len(x)):
        list1 = x[i][:]
        smple.append(list1)
    for j in range(len(smple)):
        object = smple[j]
        for tup in object:
            word = tup[0].lower()  # lowering the cases here
            # if word not in stop_words:
            words.append(word)
    return words
