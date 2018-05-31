import user

import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd
import numpy as np
from labellines import labelLine, labelLines

from processFile import checkWordCount, userDict

userList = []
totalMessagesPerUser = []
responseTimePerUser = []
totalUsers = len(userDict.keys())

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
globalColors = mcd.TABLEAU_COLORS
bigGraphThreshold = 5 #If the number of users exceeds this number, switch to the larger graph 
pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")

#Gather totalMessages and AverageResponseTime for all users and trim names if they're too long 
for user in userDict:
    currentUserName = userDict[user].getFullName()
    if len(currentUserName) >= 26:
        currentUserName = currentUserName[:-5] + "..."
    userList.append(currentUserName)
    totalMessagesPerUser.append(userDict[user].getNumMessages())    
    responseTimePerUser.append(userDict[user].getAverageResponseTime())

def graphData():
    if totalUsers >= 1:
        configureGraph()
        graphTotalMessages()
        graphAverageResponeTime()
        graphAverageMessagesPerMonth()
        trackWordUsageGroup()

def configureGraph():
    #Set the defaults for all of our graphs 
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['lines.color'] = 'white'
    
    #Large groups will need more space to fit all of their data 
    if totalUsers >= bigGraphThreshold:
        plt.rcParams['figure.figsize'] = [21,9]
        plt.rcParams['xtick.labelsize'] = 15
        plt.rcParams['ytick.labelsize'] = 15
        plt.rcParams['axes.labelsize'] = 'x-large'




"""
Create a histogram showing the total messages sent for each user and save to the output pdf 
"""
def graphTotalMessages():
    currentFigure = plt.figure()
    totalMessageGraph = plt.subplot()
    barGraph = plt.bar(userList, totalMessagesPerUser, color = globalColors)
    
    if totalUsers <= bigGraphThreshold:
        totalMessageGraph.set_title("Total Messages Sent")
    else:
        totalMessageGraph.set_title("Total Messages Sent", size = 20)

    totalMessageGraph.set_ylabel("Messages Sent")
    totalMessageGraph.set_xlabel("Users")
    currentFigure.autofmt_xdate()

    pdf.savefig(currentFigure)

"""
Create a histogram showing the average response time for each user and save to the output pdf 
"""
def graphAverageResponeTime():
    currentFigure = plt.figure()
    averageResponseTimeGraph = plt.subplot()
    barGraph = plt.bar(userList, responseTimePerUser, color = globalColors)
    currentFigure.autofmt_xdate()

    if totalUsers <= bigGraphThreshold:
        averageResponseTimeGraph.set_title("Average Response Time")
    else:
        averageResponseTimeGraph.set_title("Average Response Time", size = 20)

    averageResponseTimeGraph.set_ylabel("Response Time (Minutes)")
    averageResponseTimeGraph.set_xlabel("Users")

    pdf.savefig(currentFigure)

"""
Create a line graph of every user's average messages sent per month and save to output pdf 
"""
def graphAverageMessagesPerMonth():
    currentFigure = plt.figure()
    averageMessagesPerMonth = plt.subplot()
    
    for user in userDict:
        userName = userDict[user].getFirstName()
        userMonthActivity = userDict[user].getAveragedMonthActivity()
        currentPlot = averageMessagesPerMonth.plot(list(range(0,12)), userMonthActivity, label = userName)

    if totalUsers <= bigGraphThreshold:
        labelLines(plt.gca().get_lines())
        averageMessagesPerMonth.set_title("Average Messages Sent per Month")
        averageMessagesPerMonth.set_xticks(np.arange(12))
        averageMessagesPerMonth.set_xticklabels(months)
    else:
        averageMessagesPerMonth.legend()
        averageMessagesPerMonth.set_title("Average Messages Sent per Month", size = 20)
        averageMessagesPerMonth.set_xticks(np.arange(12))
        averageMessagesPerMonth.set_xticklabels(months, fontsize = 18)

    averageMessagesPerMonth.set_ylabel("Messages Sent")
    averageMessagesPerMonth.set_xlabel("Users")
       
    currentFigure.autofmt_xdate()

    pdf.savefig(currentFigure)

"""
Generate a new figure for each word and plot a line graph for each user's usage of said word over a year 
"""
def trackWordUsageGroup():
    for word in checkWordCount:
        currentFigure = plt.figure()
        trackedWordGraph = plt.subplot()
        
        for user in userDict:
            userName = userDict[user].getFirstName()
            
            userTrackedWordHistory = userDict[user].getTrackedWords()
            currentWordHistory = userTrackedWordHistory[word][1].getAveragedMonthActivity()

            wordUsagePlot = plt.plot(list(range(0,12)), currentWordHistory, label = userName)
        
        if totalUsers <= bigGraphThreshold:
            labelLines(plt.gca().get_lines())
            trackedWordGraph.set_title("Usage of " + "\"" + word + "\"" + " per Month")
            trackedWordGraph.set_ylabel("Times Used")
            trackedWordGraph.set_xticks(np.arange(12))
            trackedWordGraph.set_xticklabels(months)
        else:
            trackedWordGraph.legend()
            trackedWordGraph.set_title("Usage of " + "\"" + word + "\"" + " per Month", size = 22)
            trackedWordGraph.set_ylabel("Times Used")
            trackedWordGraph.set_xticks(np.arange(12))
            trackedWordGraph.set_xticklabels(months, fontsize = 16)
        
        currentFigure.autofmt_xdate()
        pdf.savefig(currentFigure)

graphData()

pdf.close()