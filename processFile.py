import os, sys, json, user
from user import UserData
from start import fileName, trackWordUsage, hourRange, keyWords, ignoreByPeerID, includeOnlyByPeerID

os.chdir(os.path.dirname(sys.argv[0]))
file = open(fileName, encoding = "utf8")
sys.stdout = open("fullStats.txt", "w", encoding = "utf8") #Redirect all print statements to this text file

#Track the usage of certain words throughout, input phrases or words as strings 
checkWordCount = trackWordUsage

userDict =  dict()
firstRunFlag = 1
totalMessageCount = 0
mostRecentMessage = {0:0}

for currentLine in file.readlines(): #Loop through every message in our specified file
    #Load the entire JSON object into a python dictionary 
    messageData = json.loads(currentLine)

    if messageData["event"] == "message":
        totalMessageCount+=1
        mediaFlag = 0
        
        #Data of only the sender of the current message, includes peer_id, name, and phone number 
        currentSenderData = messageData['from']
        
        #Correctly set the first message as the most recent message to set an intial date correctly
        if firstRunFlag == 1:
            mostRecentMessage = {currentSenderData['peer_id']:messageData['date']}
            firstRunFlag = 0

        #Code used to check if a message was sent or a photo/file
        if 'text' not in messageData: 
            if 'media' in messageData:
                mediaDict = messageData['media'] #Store the object containing info about the media sent 
                if 'caption' in mediaDict: #Found a photo
                    messageText = messageData['media']['caption'] #Pass the caption 
                    mediaFlag = 1
                elif mediaDict['type'] == 'document': #Found a file
                    messageText = 'Document' #Pass in a blank string as no message was sent with it 
                    mediaFlag = 2 
            else:
                messageText = ''
        else: #Encountered a normal message 
            messageText = messageData['text']
            if 'media' in messageData: #Links are unique in that they include both text and media fields 
                mediaDict = messageData['media']
                if 'url' in mediaDict: #Double check that it's a link 
                    messageText = '' #ignoring links sent so they don't skew word count 
                    mediaFlag = 3

        currID = messageData['from']['peer_id']
        if 'first_name' in currentSenderData: #set currSender as the sender's full name if available
            currSender = messageData['from']['first_name'] + " " + messageData['from']['last_name']
        else:
            currentSender = currentSenderData['print_name'] + str(currID)

        #Declare a new user if they aren't already in userDict, {ID : UserData()}
        if currID not in userDict: 
            userDict[currID] = user.UserData(currID, currSender)
        
        #Update all relevant info about the current sender of this message 
        userDict[currID].updateData(messageData, messageText, mediaFlag, checkWordCount, mostRecentMessage)
        
        #Run search methods for the current message to see if matches parameters set in start.py 
        if hourRange[0] <= hourRange[1]: #Only look for messages if a valid hour range was provided 
            userDict[currID].findMessage(messageData, messageText, hourRange, keyWords)
        
        #Store the time and user of the message just processed exp:(12345676: UNIX TIME CODE)
        mostRecentMessage = {currID:messageData['date']}

#Remove any users that we don't want to graph. These users were specified in start.py 
for peerID in ignoreByPeerID:
    userDict.pop(peerID, None)

invalidKeys = []

if len(includeOnlyByPeerID) != 0: #Assume an empty list here means we want all users by default, only run if peerIDs were specified
    for peerID in userDict: #Get the list of all peerIDs that we don't want anymore
        if peerID not in includeOnlyByPeerID:
            invalidKeys.append(peerID)

    for invalidKey in invalidKeys: #Remove all unwanted peerIDs 
        userDict.pop(invalidKey, None)

#Print stats for each user in chat
print()
for user in userDict:
    userDict[user].printInfo()

print("\n" + "Total Messages Processed: " + str(totalMessageCount) + "\n")

import graph