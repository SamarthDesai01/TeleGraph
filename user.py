import math, datetime, dateinfo
from dateinfo import ActivityInfo

class UserData(object):
    """
    Class used to store all relevant data for each user 
    """
    #Used in the printWeekdayInfo() method to translate numbers to their corresponding strings
    weekdays = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
                4: "Thursday", 5: "Friday", 6: "Saturday"}

    def __init__(self, idNum, name):
        """
        idNum - unique peer_id
        name -  first name + last name
        numMessages - number of messages sent by user
        totalLength - total words sent by user
        totalCharacters - number of characters sent by user
        numResponses - number of times the user has sent a message right after another user
        totalResponseTime - sum of time between user sending a message after another user
        mediaSent - dictionary holding the number of times a type of media was sent
        wordDict - dictionary holding the number of times a certain word was used. Used to keep track of words 
                that user wants to see exp: {"test" : [234, activityInfo()], "hello" : [234, activityInfo()]}
        activity - activityInfo object holding user activity in terms of time 
        searchedMessages - dictionary holding messages and their corresponding time sent that match the parameters given by the user
                            {"hey":UNIXTIMESTAMP}
        """
        self.id = idNum
        self.name = name
        self.numMessages = 0
        self.totalLength = 0
        self.totalCharacters = 0
        self.numResponses = 0
        self.totalResponseTime = 0
        self.mediaSent = {"pics":0, "docs":0, "links":0}
        self.wordDict = dict()
        self.activity = dateinfo.ActivityInfo()
        self.searchedMessages = dict()
    
    def updateData(self, messageData, message, mediaFlag, words, mostRecentMessage):
        """
        Method called to update all relevant stats for a specific person
        messageData - Object containing all info about current sender/receiver/media/time
        message - String containing the message sent by self
        mediaFlag - Set if this message was not a normal text,
                    1 - Picture
                    2 - Document
                    3 - Webpage
        words -  List containing special words to keep track of indicated by the user 
        mostRecentMessage - Dict containing the peerID and time of the last processed message
        """

        self.numMessages += 1
        
        #Update Date Info
        self.processDates(messageData)

        #Calculate Response Time 
        if self.id not in mostRecentMessage: #Ignore concurrent messages sent by the same user
            self.calculateResponseTime(messageData, mostRecentMessage)

        #Keep track of occurences of certain words 
        if len(words) != 0:
            self.checkSpecificWords(message, messageData, words)

        #Increment appropriate Media Counter 
        if mediaFlag == 1:
            self.updateNumPics()
        elif mediaFlag == 2: 
            self.updateNumDocuments()
        elif mediaFlag == 3:
            self.updateNumLinks()
        
        #Update Word and Character Lengths 
        self.updateLength(message)

    def updateNumPics(self):
        """
        Increment number of pictures sent by this user 
        """
        self.mediaSent["pics"] += 1

    def updateNumDocuments(self):
        """
        Increment number of files sent by this user
        """
        self.mediaSent["docs"] += 1
    
    def updateNumLinks(self):
        """
        Increment number of webpages sent by this user 
        """
        self.mediaSent["links"] += 1 

    def updateLength(self, message):
        """
        Update the word/character length variables for this user
        message - string containg only the text of the message 
        """
        messageLength =  len(message.split())
        messageChars = len(message)
        self.totalLength += messageLength
        self.totalCharacters += messageChars

    def checkSpecificWords(self, message, messageData,  words):
        """
        Method used to check and track the presence of certain words. Each word is given a count and their own activityInfo object 
        message - string of only the message
        messageData - full JSON object containing all data of the message
        words - array containing all special words to keep track of 
        """
        message = message.lower()
        for word in words:
            if word not in self.wordDict:
                self.wordDict[word] = [0, ActivityInfo()]
            if word in message:
                numOccurences = message.count(word)
                self.wordDict[word][0] += numOccurences
                self.wordDict[word][1].updateActivity(messageData['date'])

    def processDates(self, messageData):
        """
        Process the time related info for the message
        messageData - JSON Object containing all information for the current object, used for getting timestamp 
        """
        timestamp = messageData['date']
        self.activity.updateActivity(timestamp)

    def calculateResponseTime(self, messageData, mostRecentMessage):
        """
        Updates the response time for the current user 
        messageData - JSON Object containng all information for the current object, used for getting timestamp
        mostRecentMessage - length 2 array containing [id, timeStamp] of the most recently processed message
        """
        for sender in mostRecentMessage:
            #Data is read in backwards, going from most recent to latest, thus the "recentMessage" will have a greater time stamp than our current message
            responseTime = mostRecentMessage[sender] - messageData['date']
            #Check if the time between messages is greater than 5 hours, if so both people are probably asleep so ignore this for responseTime
            if not(responseTime >= 36000):
                self.totalResponseTime+=responseTime
                self.numResponses+=1

    def findMessage(self, messageData, messageText, hourRange, keyWords):
        """
        Method used to find certain messages within conversations, narrowed down by hours and certain keywords
        messageData - json object containing all message data
        hourRange - size 2 tuple with a range of hours from (0,23)
        keyWords - optional array containing strings of desired keywords 
        """
        hourSent = datetime.datetime.fromtimestamp(messageData['date']).hour #Get hour of the day
        daySent = datetime.datetime.fromtimestamp(messageData['date']).isoformat() #Get full ISO format String
        if len(keyWords) == 0: #Only use this method if our keyWords array is empty
            if (hourSent >= hourRange[0]) and (hourSent <= hourRange[1]): #Check if this message is within our hour range
                self.searchedMessages[messageText] = daySent
        else:
            self.findMessageWithKeyword(messageData, messageText, hourRange,keyWords, hourSent) #Must check for keywords as well 
            
    def findMessageWithKeyword(self, messageData, messageText, hourRange, keyWords, hourSent):
        """
        Extension of findMessage(), called if keywords are specified 
        """
        daySent = datetime.datetime.fromtimestamp(messageData['date']).isoformat()
        if(hourSent >= hourRange[0]) and (hourSent <= hourRange[1]):
            for word in keyWords:
                if word in messageText:
                    self.searchedMessages[messageText] = daySent

    def getNumMessages(self):
        """
        Return the total number of messages for this current user 
        """
        return self.numMessages

    def getFirstName(self):
        """
        Return only the first name of this user
        """
        nameList = self.name.split()
        return nameList[0]

    def getFullName(self):
        """
        Return the full name of this user
        """
        return self.name

    def getAveragedMonthActivity(self):
        """
        Refer to getAveragedMonthActivity() in dateinfo.py
        """
        return self.activity.getAveragedMonthActivity()

    def getAverageResponseTime(self):
        """
        Return the average response time for this user in minutes
        """
        return (self.totalResponseTime/self.numResponses)/60

    def getTrackedWords(self):
        """
        Return dictionary with words specified by user to be checked, each word has its own ActivityInfo object 
        """
        return self.wordDict

    def printInfo(self):
        """
        Print all info for the current user 
        """
        print("-------------------" + self.name + "-------------------")
        print("    Peer ID: " + str(self.id))
        print("    Messages Sent: " + str(self.numMessages))
        print("    Pictures Sent: " + str(self.mediaSent["pics"]))
        print("    Files Sent: " + str(self.mediaSent["docs"]))
        print("    Links Sent: " + str(self.mediaSent["links"]))
        print("    Average Message Length (Words): " + str((round(self.totalLength/self.numMessages))))
        print("    Average Characters Per Message: " + str(round(self.totalCharacters/self.numMessages)))
        print("    Average Response Time(Minutes): " + str(self.getAverageResponseTime()))
        for word in sorted(self.wordDict.keys()):
            print("    " + word + " : " + str(self.wordDict[word][0]))
        self.printMonthInfo()
        self.printWeekdayInfo()
        self.printHourInfo()
        self.printSearchedMessages()

    def printMonthInfo(self):
        """
        Print number of messages sent each month, separated by year 
        """
        print("Messages Sent per Month: ")
        monthAct = self.activity.getMonthActivity()
        for year in sorted(monthAct.keys(), reverse = False):
            print(year)
            for monthNum in sorted(monthAct[year]):
                print ("    " + str(monthNum) + ": " + str(monthAct[year][monthNum]))

    def printWeekdayInfo(self):
        """
        Print the average number of messsages sent each weekday 
        """
        print("Average Messages Sent per Week")
        weekAct = self.activity.getWeekdayActivity()
        for weekday in sorted(weekAct.keys()):
            avgMessage = weekAct[weekday][0]/weekAct[weekday][1]
            print("    " + self.weekdays[weekday] + ": " + str(avgMessage))
    

    def printHourInfo(self):
        """
        Print the average number of messages sent each hour 
        """
        print("Average Messages sent for each hour: ")
        weekAct = self.activity.getWeekdayActivity()
        firstAvailableWeekDay = 0

        for weekDay in weekAct:
            firstAvailableWeekDay = weekDay
            break

        numDays = weekAct[firstAvailableWeekDay][1] * 7
        hourAct = self.activity.getHourActivity()
        for hour in sorted(hourAct.keys()): 
            avgMessage = hourAct[hour][0]/numDays
            print("    " + str(hour) + ": " + str(avgMessage))

    def printSearchedMessages(self):
        print ("\n" + "Found " + str(len(self.searchedMessages.keys())) + " message(s) matching your parameters.")
        print()
        for message in self.searchedMessages:
            print("    " + message + "  : " + self.searchedMessages[message])

