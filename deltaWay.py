#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 sagar <sagar@sagar-liquid>
#
# Distributed under terms of the GNU GPL license.

"""
To get the delta information about the files that get sync in dropbox folder.
"""
import dropbox
import commands

PATH = '/home/sagar/Dropbox'
RELPATH = '/'

def resolvePath(allPath,client):
    newPath=[]
    custom = RELPATH
    for path in allPath[1:]:
        metadata = client.metadata(custom)
        content = metadata.get('contents')
        #Need a logic for change in different locatoins
        if content:
            for relPath in content:
                #print PATH + relPath.get('path'), "-"*4, path
                if PATH.lower() + relPath.get('path').lower() == path.lower():
                    #print "Relative:", relPath.get('path')
                    custom = custom+relPath.get('path').split('/').pop()+'/'
                    #print "custom: ", custom
                    newPath.append(PATH+custom)
                    break
    if not(newPath==[]):
        newPath.append(PATH)
    return newPath

def generatePath(entries,client):
    allPath=[]
    for i in entries:
        if i[1]:    
            path=i[1].get('path')
            splitPath = path.split('/')
            while(splitPath):
                newPath = PATH+"/".join(splitPath)
                if newPath not in allPath:
                    allPath.append(newPath)
                splitPath.pop() 
    if not(allPath==[]):
        allPath.sort()
        print allPath
        allPath = resolvePath(allPath,client)
    return allPath

def setEmblem(allPath):
    for path in allPath:
        command = "gvfs-set-attribute "+path+" -t stringv metadata::emblems new"
        print command
        commands.getoutput(command)

def resetEmblem(allPath):
    for path in allPath:
        command = "gvfs-set-attribute "+path+" -t unset metadata::emblems"
        print command
        commands.getoutput(command)

def main():
    """Get the cursor string."""
    access_token = 'q0Lcd6-SLT0AAAAAAAAAAdjtKTjnvaEYnv5rr77HrssoB9XSEXPdYHcoiQ0RilVT'
    # user_id = '97122634'

    client = dropbox.client.DropboxClient(access_token)
    #print client.account_info()
    
    cursorFile = open('cursor','r')
    cursor = cursorFile.read()
    cursorFile.close()
    
    cursor = client.delta(cursor)

    '''
    count = 0
    while(1):
        cursor = client.delta(cursor)
        if not(cursor.get('has_more')):
            break
        else:
            cursor=cursor.get('cursor')
        count += 1
        print count
    '''
    cursor_key = cursor.get('cursor')
    cursorFile = open('cursor','w')
    cursorFile.write(cursor_key)
    cursorFile.close()
    
    previousEntryFile = open('entries','r')
    previousEntries = previousEntryFile.read()
    previousEntries = eval(previousEntries)
    previousEntryFile.close()

    
    if previousEntries:
        paths = generatePath(previousEntries,client)
        #print paths
        resetEmblem(paths)
    else:
        print "Null"
    
    items = cursor.get('entries')
    entryFile = open('entries','w')
    entryFile.write(str(items))
    entryFile.close()

    if items:
        paths = generatePath(items,client)
        #print paths
        setEmblem(paths)
    else:
        print "No Change"    

if __name__ == '__main__':
    main()