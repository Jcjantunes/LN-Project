import sys

geography = 'GEOGRAPHY'
music = 'MUSIC'
literature = 'LITERATURE'
history = 'HISTORY'
science = 'SCIENCE'

def main(argv):
    
    devFile = argv[0]
    resultFile = argv[1]
    
    dev_file = open(devFile, "r", encoding="utf8")
    result_file = open(resultFile, "r", encoding="utf8")
    
    devFileTopics = []
    devFileQuestions = []
    for line in dev_file:
        split_string = line.split("\t")
        devFileTopics.append(split_string[0])
        devFileQuestions.append(split_string[1])
    
    resultFileTopics= []
    for line in result_file:
        split_string = line.rstrip("\n")
        resultFileTopics.append(split_string)
    
    geographyCount = 0
    musicCount = 0
    literatureCount = 0
    historyCount = 0
    scienceCount = 0
    
    correctGeographyCount = 0
    correctMusicCount = 0
    correctLiteratureCount = 0
    correctHistoryCount = 0
    correctScienceCount = 0 
           
    TP = 0
    FP = 0
    for i in range(len(resultFileTopics)):
        #print(str(resultFileTopics[i]) + " " + str(devFileTopics[i]))
        
        if(devFileTopics[i] == geography):
            geographyCount += 1
        elif(devFileTopics[i] == music):
            musicCount += 1
        elif(devFileTopics[i] == literature):
            literatureCount += 1
        elif(devFileTopics[i] == history):
            historyCount += 1
        elif(devFileTopics[i] == science):
            scienceCount += 1
            
        if(resultFileTopics[i] == devFileTopics[i]):
            TP += 1
            if(devFileTopics[i] == geography):
                correctGeographyCount += 1
            elif(devFileTopics[i] == music):
                correctMusicCount += 1
            elif(devFileTopics[i] == literature):
                correctLiteratureCount += 1
            elif(devFileTopics[i] == history):
                correctHistoryCount += 1
            elif(devFileTopics[i] == science):
                correctScienceCount += 1            
        else:
            FP += 1
            
            print("resultTopic: " + resultFileTopics[i] + "\t correctTopic: " + devFileTopics[i] + "\t" + devFileQuestions[i])           
    
    precision = TP/(TP + FP)
    
    print()
    print("Accuracy rate: " + str(precision))
    print("Miss rate: " + str(1 - precision))
    print()
    
    geographyProbability = correctGeographyCount/geographyCount
    musicProbability = correctMusicCount/musicCount
    literatureProbability = correctLiteratureCount/literatureCount
    historyProbability = correctHistoryCount/historyCount
    scienceProbability = correctScienceCount/scienceCount
    
    topicProbabilityList = []
    
    topicProbabilityList.append(geographyProbability)
    topicProbabilityList.append(musicProbability)
    topicProbabilityList.append(literatureProbability)
    topicProbabilityList.append(historyProbability)
    topicProbabilityList.append(scienceProbability)
    
    wrongTopicProbabilityList = []
    
    wrongTopicProbabilityList.append(1 - geographyProbability)
    wrongTopicProbabilityList.append(1 - musicProbability)
    wrongTopicProbabilityList.append(1 - literatureProbability)
    wrongTopicProbabilityList.append(1 - historyProbability)
    wrongTopicProbabilityList.append(1 - scienceProbability)    
    
    print("Topic accuracy rate:")
    print("\t" + str([geography, music, literature, history, science]))
    print("\t" + str(topicProbabilityList))
    
    print()
    
    print("Topic miss rate:")
    print("\t" + str([geography, music, literature, history, science]))
    print("\t" + str(wrongTopicProbabilityList))    
    
    dev_file.close()
    result_file.close()    
    
    
if __name__ == "__main__":
    main(sys.argv[1:])