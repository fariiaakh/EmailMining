# The dataframe names mentioned here are all arbitrary
#
#  to convert time from a string object to datetime object
# converting to datetime
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk
import re
from datetime import datetime as dt


def converttime(dataset):
    for i in range(len(dataset)):
        datecol = dataset.loc[i]["Date"]
        date = datecol[:25]
        date = date.strip()
        date = dt.strptime(date, "%a, %d %b %Y %H:%M:%S")
        dataset.iloc[:, 2][i] = date
    return dataset


# The entire email contains many duplicate emails with duplicate time stamps. Get rid of the duplicates
data = data.drop_duplicates(subset=["Date"])
# Selecting specific time period, based on the date
# Enron Scandal begin more during 2001 (this was the main focus of our report)


data2a = data2[(data2["Date"] > dt(2000, 1, 1, 0, 0)) &
               (data2['Date'] <= dt(2001, 1, 1, 0, 0))]

# email subjects can contain very relevant information for email categorization but the prefixes like 're' or 'fwd' can confuse algorithms
# This function gets rid of any prefixes that may exist in an email subject line


def cleansub(dataset, column):
    junk = ["re:", "fwd:", "fw:"]
    dataset["CleanSubject"] = ""  # create empty column
    vocab = ""
    for index in range(len(dataset[column])):
        vstring = str(dataset.iloc[index][column])
        vstring1 = vstring.lower()
        vlist = vstring1.split()
        vlist2 = vlist.copy()
        ind = 0
        for index1 in range(len(vlist2)):
            while ind <= (len(junk)-1):  # iterate through junkword list
                aword = junk[ind]
                bword = vlist2[index1].strip()
                if aword == bword:  # if word from junkword list is found in word from clean word list
                    # find the index of the matching word
                    num = vlist2.index(bword)
                    # remove that word from the clean word list
                    vlist2.pop(num)
                    # add empty space to keep list from getting shorter
                    vlist2.insert(num, "")
                ind += 1
            ind = 0
        vlist3 = vlist2.copy()  # create copy of new cleaner list of words
        # print(vlist3)
        # for each word in vlist3, if it is not an empty space, stem it and add it to a string
        for item in range(len(vlist3)):
            thing = vlist3[item]
            if thing != '':
                vocab = vocab+" "+thing
        # add new clean string to the appropriate cell
        dataset.at[index, "CleanSubject"] = vocab
        vocab = ""

    return dataset

# label emails with the same sender,reciver and subject as threads


def thread(datasub):
    ThreadID = 0
    assigned_indices = []
    for i in range(len(datasub)):
        if datasub.at[i, 'ThreadID'] == 0:
            # until j reaches 100
            ThreadID += 1
            j = i+1
            datasub.at[i, 'ThreadID'] = ThreadID
            assigned_indices.append(i)
            while j <= (len(datasub)-1):
                if datasub.at[i, 'CleanSubject'] == datasub.at[j, 'CleanSubject'] and j not in assigned_indices:
                    # if the columns match, threadID is provided
                    datasub.at[j, 'ThreadID'] = ThreadID
                    assigned_indices.append(j)
                j += 1
    return datasub


# use quotations when inputting column name
# change function to give back new strings instead of threads, also to change the dataframe cell in place
# get rid of stop words
# stem words
ps = PorterStemmer()
junkwords = ["day", "houect", "pm", "am", "cc", "bcc", "or", "subject", "fw", "forward", "original", "phil", "allen", "john", "keith", "holt", "mike", "grigsby",
             "steve", "hunter", "shiv", "martin", "arnold", "janie", "lavor", "tom", "ermis", "chris", "deb", "neal", "smith", "mark", "jan", "feb",
             "march", "april", "may", "june", "july", "aug", "sept", "oct", "nov", "dec", "from", "www", "http", "lucy", "gonzal", "randy", "zarin", "imam", "scott", "richard", "paula",
             "enron", "nancy", "brenda", "george", "claud", "larry", "jim", "mich", "lewter", "jeff", "hotmail", "msn", "nowak", "holst",
             "outlook", "teamenron", "migration", "monique", "sanchez", "brandon", "amir", "charles", "dave", "donald", "kathryn", "felicia", "joe",
             "leon", "milton", "rick", "ann", "laquitta", "charlotte", "gary", "jen", "andr", "wesley", "natali", "joseph", "william", "randall", "kendall",
             "meredith", "shanna", "tamara", "tracy", "jack", "kathy", "lisa", "amgusa", "ruth", "sid", "camille", "doe", "mailbox", "ina", "rangel",
             "greg", "piper", "jean", "rober", "sean", "tim", "kevin", "cooper", "jay", "evans", "arthur", "danny", "matt", "tori", "brad",
             "alan", "paul", "dale", "leticia", "frank", "lance", "edgar", "gabriel", "brian", "delaney", "david", "lyndel", "allison", "joan",
             "cynthia", "jess", "kell", "craig", "kris", "lian", "allan", "bruce", "jake", "shekar"]


def onlywords(dataset, column):
    dataset["CleanContent"] = ""  # create empty column
    vocab = ""
    vlist2 = []
    stop_words = list(stopwords.words('english'))
    for index in range(len(dataset[column])):
        vstring = str(dataset.iloc[index][column])
        vlist = vstring.split()
        for i in range(len(vlist)):  # for each word in the list
            word = vlist[i]
            if word not in stop_words:  # if the word is not in the stop_words list, then make it lowercase and run it through regex stuff
                word = word.lower().strip()
                # remove email addresses from email body
                word = re.sub(
                    r'(<)?[a-zA-Z0-9_.+-]+@[a-zA-z0-9]*.[a-zA-z0-9]*.(com|net)(>)?', '', word)
                # remove num and punctuations from email body
                word = re.sub(
                    r'[!""#$%&''()*+,\'-./:;<=>?@[\]^_`{|}~\d+]', '', word)
            vlist2.append(word)  # append clean word to a new list
        # print(vlist2)
        ind = 0
        for index1 in range(len(vlist2)):
            while ind <= (len(junkwords)-1):  # iterate through junkword list
                # for ind in range(len(vlist2)):
                aword = junkwords[ind].strip()
                bword = vlist2[index1].strip()
                if aword in bword:  # if word from junkword list is found in word from clean word list
                    # find the index of the matching word
                    num = vlist2.index(bword)
                    # remove that word from the clean word list
                    vlist2.pop(num)
                    # add empty space to keep list from getting shorter
                    vlist2.insert(num, "")
                ind += 1
            ind = 0
        vlist3 = vlist2.copy()  # create copy of new cleaner list of words
        # print(vlist3)
        # for each word in vlist3, if it is not an empty space, stem it and add it to a string
        for item in range(len(vlist3)):
            thing = vlist3[item]
            if thing != '':
                # thing=ps.stem(thing)
                vocab = vocab+" "+thing
        # add new clean string to the appropriate cell
        dataset.at[index, "CleanContent"] = vocab
        vocab = ""
        vlist2 = []

    return dataset
