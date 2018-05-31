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





