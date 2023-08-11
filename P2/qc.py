import sys
import re
import random

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV

geography = '^(GEOGRAPHY)'
music = '^(MUSIC)'
literature = '^(LITERATURE)'
history = '^(HISTORY)'
science = '^(SCIENCE)'

stopWords = ["?", ".", ",", "'", "to", "the", "a", "an", "i", "yours", "our", "ours", "their", "theirs", "her", "his", "herself", "himself", "she", "they", "it", "such", "into", 
             "of", "itself", "other", "is", "s", "am", "as", "from", "him", "each", "themselves", "until", "below", "are", "we",  "through", "those", "after", "few", "t", "being", 
             "if", "my", "against", "doing", "how", "further", "here", "than", "ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "during", "out", "very", 
             "having", "own", "some", "its", "been", "have", "does", "yourselves", "then", "because", "over", "so", "can", "now", "under", "has", "just", "too", "only", "myself", 
             "nor", "more", "should", "while", "above", "both", "up", "all", "no", "at", "before", "them", "same", "'s", "'t"]

def lemmatize(line, lemmatizer):
    lemmatizedQuestion = []
    question = line.split()
    
    for w in question:
        lemmatizedQuestion.append(lemmatizer.lemmatize(w))
    
    lemmatizedQuestionString = ""
    for w in lemmatizedQuestion:
        lemmatizedQuestionString += w + " "
    
    return lemmatizedQuestionString[:len(lemmatizedQuestionString) - 1]

def eliminateStopWords(line):
    wordTokens = word_tokenize(line)
    
    filteredQuestion = ""
    for token in wordTokens:
        w = token.lower()
        if w not in stopWords:
            filteredQuestion += w + " "
    
    return filteredQuestion[:len(filteredQuestion) - 1]

def preProcessQuestion(line, lemmatizer):
    question = eliminateStopWords(line)
    question = re.sub(r'\W', ' ', question)    
    question = question.lower()
           
    return lemmatize(question, lemmatizer)

def preProcessTrainFile(trainFile, trainQuestionsList, trainTopicsList, lemmatizer):
    for line in trainFile:
        splitedLine = line.split("\t")
        answer = splitedLine[2].strip('\n')
        qa = splitedLine[1] + " " + answer
        question = preProcessQuestion(qa, lemmatizer)
        topic = splitedLine[0]
        
        trainQuestionsList.append(question)
        trainTopicsList.append(topic)
    
def preProcessTestFile(testFile, testQuestionsList, lemmatizer):
    for line in testFile:
        splitedLine = line.split("\t")
        if (re.match(geography, line) or re.match(music, line) or re.match(literature, line) or re.match(history, line) or re.match(science, line)):
            answer = splitedLine[2].strip('\n')
            qa = splitedLine[1] + " " + answer
            question = preProcessQuestion(qa, lemmatizer)
            testQuestionsList.append(question)
        else:
            answer = splitedLine[1].strip('\n')
            qa = splitedLine[0] + " " + answer
            question = preProcessQuestion(qa, lemmatizer)
            testQuestionsList.append(question)

def jaccard_similarity_score(q1, q2):
    
    set1 = set(q1.split())
    set2 = set(q2.split())
    
    intersection = len(list(set1.intersection(set2)))
    union = len(list(set1.union(set2)))
    
    return float(intersection/union)

def jaccardModel(trainQuestionsList, trainTopicsList, testQuestionsList):
    for testQuestion in testQuestionsList:
        topic = ""
        jss = 0
        for i in range(len(trainQuestionsList)):
            jssAux = jaccard_similarity_score(testQuestion, trainQuestionsList[i])
            if(jssAux > jss):
                jss = jssAux
                topic = trainTopicsList[i]
        print(topic)

def printResults(results):
    for i in range(len(results)):
        result = results[i]
        if(i != len(results) - 1):
            print(result)
        else:
            print(result, end='')

def naiveBayes_countVectorizerModel(trainQuestionsList, trainTopicsList, testQuestionsList):    
    countVectorizer = CountVectorizer()
    tfidfTransformer = TfidfTransformer()
    naiveBayesClassifier = MultinomialNB()    
    
    pipelineParams = [('countVector', countVectorizer), ('tf-idf', tfidfTransformer), ('naive-bayes-clf', naiveBayesClassifier)]
    
    printResults(Pipeline(pipelineParams).fit(trainQuestionsList, trainTopicsList).predict(testQuestionsList))

def naiveBayes_countVectorizer_gridSearchModel(trainQuestionsList, trainTopicsList, testQuestionsList):
    countVectorizer = CountVectorizer()
    tfidfTransformer = TfidfTransformer()
    naiveBayesClassifier = MultinomialNB()    
    
    pipelineParams = [('countVector', countVectorizer), ('tf-idf', tfidfTransformer), ('naive-bayes-clf', naiveBayesClassifier)]  
    
    gridSearchParams = {'countVector__ngram_range': [(1, 1), (1, 2), (1, 3)], 'tf-idf__use_idf': (True, False), 'naive-bayes-clf__alpha': (1e-2, 1e-3)}
        
    printResults(GridSearchCV(Pipeline(pipelineParams), gridSearchParams, n_jobs= -1).fit(trainQuestionsList, trainTopicsList).predict(testQuestionsList))
    
def main(argv):
    
    if len(argv) != 4:
        print("Expected Arguments:\n \t-test test_file -train train_file")
        exit(1)
            
    lemmatizer = WordNetLemmatizer()
    
    test_file = open(argv[1], "r", encoding="utf8")
    train_file = open(argv[3], "r", encoding="utf8")
    
    trainQuestionsList = []
    trainTopicsList = []    
    preProcessTrainFile(train_file, trainQuestionsList, trainTopicsList, lemmatizer)
           
    testQuestionsList = []
    preProcessTestFile(test_file, testQuestionsList, lemmatizer)
    
    #jaccardModel(trainQuestionsList, trainTopicsList, testQuestionsList)
    #naiveBayes_countVectorizerModel(trainQuestionsList, trainTopicsList, testQuestionsList)
    naiveBayes_countVectorizer_gridSearchModel(trainQuestionsList, trainTopicsList, testQuestionsList)
        
    test_file.close()
    train_file.close()    
    
    
if __name__ == "__main__":
    main(sys.argv[1:])