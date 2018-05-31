import math, datetime, dateinfo
from dateinfo import ActivityInfo
"""
Class used to store all relevant data for each user 
"""
class UserData(object):

    #Used in the printWeekdayInfo() method to translate numbers to their corresponding strings
    weekdays = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
                4: "Thursday", 5: "Friday", 6: "Saturday"}

    '''
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
    '''
    def __init__(self, idNum, name):
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
    
    """
    Method called to update all relevant stats for a specific person
    messageData - Object containing all info about current sender/receiver/media/time
    message - String containing the message sent by self
    mediaFlag - Set if this message was not a normal text,
                1 - Picture
                2 - Document
                3 - Webpage
    words -  List containing special words to keep track of indicated by the user 
    mostRecentMessage - 
    """
    def updateData(self, messageData, message, mediaFlag, words, mostRecentMessage):
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

    """
    Increment number of pictures sent by this user 
    """
    def updateNumPics(self):
        self.mediaSent["pics"] += 1

    """
    Increment number of files sent by this user
    """
    def updateNumDocuments(self):
        self.mediaSent["docs"] += 1
    
    """
    Increment number of webpages sent by this user 
    """
    def updateNumLinks(self):
        self.mediaSent["links"] += 1 

    """
    Update the word/character length variables for this user
    message - string containg only the text of the message 
    """
    def updateLength(self, message):
        messageLength =  len(message.split())
        messageChars = len(message)
        self.totalLength += messageLength
        self.totalCharacters += messageChars

    """
    Method used to check and track the presence of certain words. Each word is given a count and their own activityInfo object 
    message - string of only the message
    messageData - full JSON object containing all data of the message
    words - array containing all special words to keep track of 
    """
    def checkSpecificWords(self, message, messageData,  words):
        message = message.lower()
        for word in words:
            if word not in self.wordDict:
                self.wordDict[word] = [0, ActivityInfo()]
            if word in message:
                numOccurences = message.count(word)
                self.wordDict[word][0] += numOccurences
                self.wordDict[word][1].updateActivity(messageData['date'])

    """
    Process the time related info for the message
    messageData - JSON Object containing all information for the current object, used for getting timestamp 
    """
    def processDates(self, messageData):
        timestamp = messageData['date']
        self.activity.updateActivity(timestamp)

    """
    Updates the response time for the current user 
    messageData - JSON Object containng all information for the current object, used for getting timestamp
    mostRecentMessage - length 2 array containing [id, timeStamp] of the most recently processed message
    """
    def calculateResponseTime(self, messageData, mostRecentMessage):
        for sender in mostRecentMessage:
            #Data is read in backwards, going from most recent to latest, thus the "recentMessage" will have a greater time stamp than our current message
            responseTime = mostRecentMessage[sender] - messageData['date']
            #Check if the time between messages is greater than 5 hours, if so both people are probably asleep so ignore this for responseTime
            if not(responseTime >= 36000):
                self.totalResponseTime+=responseTime
                self.numResponses+=1
    """
    Method used to find certain messages within conversations, narrowed down by hours and certain keywords
    messageData - json object containing all message data
    hourRange - size 2 tuple with a range of hours from (0,23)
    keyWords - optional array containing strings of desired keywords 
    """
    def findMessage(self, messageData, messageText, hourRange, keyWords):
        hourSent = datetime.datetime.fromtimestamp(messageData['date']).hour #Get hour of the day
        daySent = datetime.datetime.fromtimestamp(messageData['date']).isoformat() #Get full ISO format String
        if len(keyWords) == 0: #Only use this method if our keyWords array is empty
            if (hourSent >= hourRange[0]) and (hourSent <= hourRange[1]): #Check if this message is within our hour range
                self.searchedMessages[messageText] = daySent
        else:
            self.findMessageWithKeyword(messageData, messageText, hourRange,keyWords, hourSent) #Must check for keywords as well 
            
    """
    Extension of findMessage(), called if keywords are specified 
    """
    def findMessageWithKeyword(self, messageData, messageText, hourRange, keyWords, hourSent):
        daySent = datetime.datetime.fromtimestamp(messageData['date']).isoformat()
        if(hourSent >= hourRange[0]) and (hourSent <= hourRange[1]):
            for word in keyWords:
                if word in messageText:
                    self.searchedMessages[messageText] = daySent

    """
    Return the total number of messages for this current user 
    """
    def getNumMessages(self):
        return self.numMessages

    """
    Return only the first name of this user
    """
    def getFirstName(self):
        nameList = self.name.split()
        return nameList[0]

    """
    Return the full name of this user
    """
    def getFullName(self):
        return self.name

    """
    Refer to getAveragedMonthActivity() in dateinfo.py
    """
    def getAveragedMonthActivity(self):
        return self.activity.getAveragedMonthActivity()

    """
    Return the average response time for this user in minutes
    """
    def getAverageResponseTime(self):
        return (self.totalResponseTime/self.numResponses)/60

    """
    Return dictionary with words specified by user to be checked, each word has its own ActivityInfo object 
    """
    def getTrackedWords(self):
        return self.wordDict

    """
    Print all info for the current user 
    """
    def printInfo(self):
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

    """
    Print number of messages sent each month, separated by year 
    """
    def printMonthInfo(self):
        print("Messages Sent per Month: ")
        monthAct = self.activity.getMonthActivity()
        for year in sorted(monthAct.keys(), reverse = False):
            print(year)
            for monthNum in sorted(monthAct[year]):
                print ("    " + str(monthNum) + ": " + str(monthAct[year][monthNum]))

    """
    Print the average number of messsages sent each weekday 
    """
    def printWeekdayInfo(self):
        print("Average Messages Sent per Week")
        weekAct = self.activity.getWeekdayActivity()
        for weekday in sorted(weekAct.keys()):
            avgMessage = weekAct[weekday][0]/weekAct[weekday][1]
            print("    " + self.weekdays[weekday] + ": " + str(avgMessage))
    
    """
    Print the average number of messages sent each hour 
    """
    def printHourInfo(self):
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

