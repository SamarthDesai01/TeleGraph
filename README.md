# TeleGraph
Powerful Python utility used to gather statistics and track trends of users in Telegram chats and to output this data in easy to read graphs.

### Dependencies
[Python 3.6.5](https://www.python.org/downloads/release/python-365/)

[Matplotlib 2.2.2](https://matplotlib.org/users/installing.html)

[Label Lines](https://github.com/cphyc/matplotlib-label-lines)

### Using TeleGraph
------
Before you get started, you'll need to get a full backup of whatever conversations you'd like to see analyzed. 

To do so, you'll need to install the following to your computer

[telegram-cli](https://github.com/vysheng/tg)

[telegram-history-dump](https://github.com/tvdstaaij/telegram-history-dump)

Once you're done configuring the two and have followed the instructions from telegram-history-dump to get a .jsonl backup of
your conversation(s) you're ready to go.

Simply move your backup file(s) to the same directory as this project and specify which file you'd like to analyze in `start.py`

```python
fileName = "yourConversation.jsonl"
```

Run `start.py` and in a few moments you should see two new files appear in the same directory listed `output.pdf` and `fullStats.txt`

`output.pdf` will contain all the graphs generated from the backup provided whereas `fullStats.txt` will display all the data collected for each user.

### Features 
------
#### Visualize Word Trends 
TeleGraph gives you the ability to track character, word, phrase, or even emoji usage over time within a conversation. TeleGraph will output the total
usage of the items you wanted tracked as well as display their usage over time in comparison to other users inside `output.pdf`

Simply enter each item you want tracked into `start.py` under:

```python
trackWordUsage = ["hey", "/user" , "🤔"]
```

#### Powerful Search
TeleGraph offers a search utility much more powerful and in-depth than Telegram's built in search. Not only does it allow you to search through your entire message history,
but you can also narrow down your search to specific hours of the day. Simply input your paramaters as shown below and the search results will display inside `fullStats.txt`

```python
hourRange = (5,7)
keyWords = ["good morning"]
```

#### Filter Certain Users 
TeleGraph also allows you to filter out certain users from the final output. This is useful if you're trying to focus on certain members of a chat or if you're removing inactive members in order to free up more space in the final graphs.
To do this simply get the peerIDs for the users you want or don't want from `fullStats.txt` and input them into the following locations:

```python
ignoreByPeerID = [12345678] #This will omit this user from showing up in any of the final output files
```

or 

```python
includeOnlyByPeerID = [12345678, 987654321] #Only these users from the conversation will appear in the final output files
```

#### Visualize User Activity

TeleGraph keeps track of each user's average messages sent per hour of day, weekday, and month. While only the activity per month is displayed 
on a graph in `output.pdf` you can see these other statistics easily inside `fullStats.txt`

#### Gather Totals

TeleGraph also keeps track of the total messages you've sent and keeps an individual count for the number of pictures, files, and webpages each user has sent.
All of these statistics are shown inside of `output.pdf` and `fullStats.txt`

### Sample Output 
----

This is what data for a single user in `fullStats.txt` would look like

```
-------------------Samarth Desai-------------------
    Peer ID: 162996295
    Messages Sent: 77939
    Pictures Sent: 2708
    Files Sent: 774
    Links Sent: 209
    Average Message Length (Words): 9
    Average Characters Per Message: 42
    Average Response Time(Minutes): 2.2038821496119483
    awesome : 27 //Occurrences for the word "awesome" - See output.pdf for a visual representation of its usage over time
    good morning : 9 
    whats up : 3
Messages Sent per Month: 
2017
    6: 3834
    7: 6800
    8: 8600
    9: 8496
    10: 6535
    11: 6223
    12: 6476
2018
    1: 8184
    2: 7292
    3: 7518
    4: 5180
    5: 2801
Average Messages Sent per Week
    Sunday: 247.57142857142858
    Monday: 249.41666666666666
    Tuesday: 245.60416666666666
    Wednesday: 228.72916666666666
    Thursday: 194.33333333333334
    Friday: 208.57142857142858
    Saturday: 235.10204081632654
Average Messages sent for each hour: 
    0: 6.326530612244898
    1: 2.323615160349854
    2: 0.8046647230320699
    3: 0.2303206997084548
    4: 0.09329446064139942
    5: 0.008746355685131196
    6: 0.014577259475218658
    7: 0.9212827988338192
    8: 2.110787172011662
    9: 8.32069970845481
    10: 8.323615160349854
    11: 13.034985422740524
    12: 11.56268221574344
    13: 13.28862973760933
    14: 14.25072886297376
    15: 15.982507288629737
    16: 15.720116618075801
    17: 16.481049562682216
    18: 14.568513119533527
    19: 14.201166180758017
    20: 16.932944606413994
    21: 17.985422740524783
    22: 19.548104956268222
    23: 14.192419825072886
```





