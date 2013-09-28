#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 sagar <sagar@sagar-liquid>
#
# Distributed under terms of the GNU GPL license.

"""
Identify and change the status icon of the files that are newly added in dropbox folder.
"""

import dropbox
import commands
import subprocess
import os

PATH = '/home/sagar/Dropbox'

def esccape_sequence(path):
    """Put escape sequence before."""
    chars = {r' ':r'\ ', r'(':r'\(', ')':r'\)', 
                 r"[":r"\[", r"]":r"\]", r"{":r"\{", r"}":r"\}"}
    for i in range(len(chars)):
        temp = chars.items()[i]
        path = path.replace(temp[0], temp[1])
    return path

def resolvePath(allPath):
    """Dropbox"""
    newPath = []
    for path in allPath:
        path_dir = path.split('/')
        path_dir.reverse()
        path_dir = filter(lambda x: x!='', path_dir)
        custom_path = PATH
        length = len(path_dir)
        for i in range(length):
            item = path_dir.pop()
            dirs = os.listdir(custom_path)
            for d in dirs:
                if d.lower() == item.lower():
                    custom_path += '/' + d
                    break
        newPath.append(custom_path + '/')
    return newPath

def generatePath(allPath, flag):
    """Recursively generate path of the parent folder and set/unset the emblems."""
    sample = []
    for path in allPath:
        items = path.split('/')
        items = filter(lambda x: x!='', items)
        length = len(items)-2
        for i in range(length):
            temp = '/'.join(items)
            temp = esccape_sequence(temp)
            if temp not in sample:
                sample.append(temp)
                if flag:
                    command = "gvfs-set-attribute /"+temp+" -t stringv metadata::emblems new"            
                    # print command
                else:
                    command = "gvfs-set-attribute /"+temp+" -t unset metadata::emblems"
                    # print command
                commands.getoutput(command)
            items.pop()

def getpaths(entries):
    """Doc string"""
    paths = []
    for entry in entries:
        if entry[1]:
            paths.append(entry[0])
    return paths

def deltaway(cursor):
    """Delta-way"""
    cursor_key = cursor.get('cursor')
    cursor_file = open('cursor','w')
    cursor_file.write(cursor_key)
    cursor_file.close()

    previous_entry_file = open('entries', 'r')
    previous_entries = previous_entry_file.read()
    if previous_entries:
        previous_entries = eval(previous_entries)
    previous_entry_file.close()

    if previous_entries:
        paths = getpaths(previous_entries)
        paths = resolvePath(paths)
        generatePath(paths, False)
    
    items = cursor.get('entries')
    entry_file = open('entries', 'w')
    entry_file.write(str(items))
    entry_file.close()

    if items:
        paths = getpaths(items)
        paths = resolvePath(paths)
        generatePath(paths, True)
    
    subprocess.Popen(["nautilus"])

def main():
    """Get the cursor string."""
    access_token = ''
    # user_id = '97122634'

    client = dropbox.client.DropboxClient(access_token)
    try:
        print client.account_info()
    except Exception as exp:
        if type(exp).__name__ == "RESTSocketError":
            print 'Network Error. Check your Internet connection!'
            exit(0)
    
    cursor_file = open('cursor','r')
    cursor = cursor_file.read()
    cursor_file.close()

    count = 0
    # print cursor
    while(1):
        try:
            cursor = client.delta(cursor)
        except Exception as exp:
            if type(exp).__name__ == "RESTSocketError":
                print 'Network Error. Check your Internet connection!'
            else:
                print type(exp).__name__
                print "Continuing from start..."
                cursor = ""
                continue
        if not(cursor.get('has_more')):
            deltaway(cursor)
            break
        else:
            cursor = cursor.get('cursor')
        count += 1
        print count
    # print cursor.get('cursor')

    ''' 
    cursor_key = cursor.get('cursor')
    cursor_file = open('cursor','w')
    cursor_file.write(cursor_key)
    cursor_file.close()

    previous_entry_file = open('entries', 'r')
    previous_entries = previous_entry_file.read()
    if previous_entries:
        previous_entries = eval(previous_entries)
    previous_entry_file.close()

    if previous_entries:
        paths = getpaths(previous_entries)
        paths = resolvePath(paths)
        generatePath(paths, False)
    
    items = cursor.get('entries')
    entry_file = open('entries', 'w')
    entry_file.write(str(items))
    entry_file.close()

    if items:
        paths = getpaths(items)
        paths = resolvePath(paths)
        generatePath(paths, True)
    
    subprocess.Popen(["nautilus"])
    # print 'came here...'
    '''

if __name__ == '__main__':
    main()
