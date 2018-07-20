import datetime
from datetime import datetime

class ActivityInfo(object):
    """
    Class for holding all time related info for any object. Will keep track of times occurred per month/week/weekday. Unix 
    Timestamp Required 
    """
    
    def __init__(self):
        """
        monthActivity - Number of messages per month, split up by years exp: {2017:{1:234}} Y, M, numMessage
        weekdayActivity - Number of messages for a certain day of the week, not split up by year
                        dict containing an array of 2 integers exp: {0: [123, 5]}, Sunday: [Total Messages, Unique Sundays]
        hourActivity -  Number of messages sent for an hour interval, dict with keys ranging from 0-23 each containing
                        an array of size 2 exp: {0: [53: 2]} {12AM [Total Messages, Number of Unique 12 AMs]} 
        mostRecentDay - Day of the year most recently processed,
                        used for counting how many unique days have 
                        been counted for averaging 
        """
        self.monthActivity = dict()
        self.weekdayActivity = dict()
        self.hourActivity = dict()
        self.mostRecentDay = 0
        self.mostRecentDayHour = 0


    def updateActivity(self, timeStamp):
        """
        Method that takes in a unixtime stamp and updates all appropriate activity 
        instance variables 
        timeStamp - unix time stamp 
        """
        self.updateMonth(timeStamp)
        self.updateWeekday(timeStamp)
        self.updateHours(timeStamp)
    
    def updateMonth(self, timeStamp):
        month = datetime.fromtimestamp(timeStamp).month
        year = datetime.fromtimestamp(timeStamp).year
        #If this year doesn't exist in monthActivity add it as a key and store a dict containing 
        #the month and 1 message
        if year not in self.monthActivity:
            self.monthActivity[year] = {month:1}
        else:
            if month not in self.monthActivity[year]:
                self.monthActivity[year][month] = 1 #New month found in an existing year
            else:
                self.monthActivity[year][month]+=1  #Existing year and month found, increment message count
        pass
    
    def updateWeekday(self, timeStamp):
        weekday = datetime.fromtimestamp(timeStamp).weekday()
        dayofYear = datetime.fromtimestamp(timeStamp).timetuple()[6] #Integer of the day of the year from 1-365
        if weekday not in self.weekdayActivity:
            self.weekdayActivity[weekday] = [1, 1]    #First occurence of a weekday initialize array
        else:
            if dayofYear != self.mostRecentDay:
                self.weekdayActivity[weekday][1] += 1 #Encountered a new occurence of this weekday, increment count
            self.weekdayActivity[weekday][0] += 1     #Update total messages for that weekday
        self.mostRecentDay = dayofYear
    
    def updateHours(self, timeStamp):
        hour = datetime.fromtimestamp(timeStamp).hour
        currDay = datetime.fromtimestamp(timeStamp).timetuple()[6]
        if hour not in self.hourActivity:
            self.hourActivity[hour] = [1,1]
        else: 
            if currDay != self.mostRecentDayHour:
                self.hourActivity[hour][1] += 1
            self.hourActivity[hour][0] += 1
        self.mostRecentDayHour = currDay
    

    def getMonthActivity(self):
        """
        Return the month activity dictionary
        """
        return self.monthActivity


    def getMonthActivityByYear(self):
        """
        Returns a dictionary with the total message activity per month separated by year 
        {2017:[1234, 1200 ... 2345]}
        """
        monthActByYear = dict() 
        for year in self.monthActivity:
            if year not in monthActByYear:
                monthList = [0,0,0,0,0,0,0,0,0,0,0,0]
                for month in self.monthActivity[year]:
                    monthList[month-1] = self.monthActivity[year][month]
                monthActByYear[year] = monthList

        return monthActByYear


    def getAveragedMonthActivity(self):
        """
        Return an array with average number of messages per month, index refers to months in order
        0 - January , 11 - December
        """
        monthAct = self.monthActivity
        monthTotalsTemp = dict() #Store a local dictionary with each month holding an array with total messages and unique months
        monthAveraged = [0,0,0,0,0,0,0,0,0,0,0,0] #Final array to return with only the averages
        for year in monthAct: 
            for month in monthAct[year]: 
                if month not in monthTotalsTemp: #Found a new month
                    monthTotalsTemp[month] = [monthAct[year][month], 1] #for this month: [number of messages: 1]
                else: #Found another occurence of this month in a different year
                    monthTotalsTemp[month][0] += monthAct[year][month]  #Add the number of messages from that month
                    monthTotalsTemp[month][1] += 1 #Found this month in a new year, increment number of unique occurences 
        
        for month in sorted(monthTotalsTemp.keys(), reverse = False):
            monthAveraged[month-1]=(round(monthTotalsTemp[month][0]/monthTotalsTemp[month][1]))
         
        return monthAveraged

    def getWeekdayActivity(self):
        return self.weekdayActivity
    
    def getHourActivity(self):
        return self.hourActivity

    def getAveragedHourActivity(self):
        """
        Return an array with the average number of messages sent for a particular hour for a day. Returned array will be of length 24 with 
        each index referring to the particular hour the average corresponds to
        """
        averagedHourActivity = [0] * 24
        weekAct = self.weekdayActivity
        firstAvailableWeekDay = 0

        for weekDay in weekAct:
            firstAvailableWeekDay = weekDay
            break

        numDays = weekAct[firstAvailableWeekDay][1] * 7
        hourAct = self.hourActivity
        for hour in sorted(hourAct.keys()): 
            avgMessage = hourAct[hour][0]/numDays
            averagedHourActivity[hour] = avgMessage
        
        return averagedHourActivity