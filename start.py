import os,sys,processFile
'''
Input the name of your .jsonl file, ensure it's in the same directory as this file
'''
fileName = ""

'''
Track the usage of certain words throughout, input phrases or words as strings
''' 
trackWordUsage = []

'''
SEARCH TOOL:
hourRange - Put in a range of hours (0,23) in which you're looking for, keep at (1,0) if you don't want to search for anything
keyWords - Optional, input as many keywords to look for in narrowing down your search 
'''
hourRange = (1,0)
keyWords = []

'''
Exclude certain users from being analyzed and graphed. Useful for removing bots, inactive members, etc. 
You can obtain the Peer ID for each user by running this file and checking the console for their Peer ID.
Peer IDs are passed in as integers 
'''
ignoreByPeerID = []

'''
Only graph users that are specified here by their peerID, useful if you're in a large group and want to isolate
only you and a couple of other people, if you include the same peerID in both the ignore and include list, it will 
be ignored
'''
includeOnlyByPeerID = []

processFile 



