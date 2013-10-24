#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 sagar <sagar@sagar-liquid>
#
# Distributed under terms of the GNU GPL license.

"""
Mark(add status-icon) the changed files in the dropbox folder.
"""

import dropbox
import commands
import subprocess
import os
import json

# PATH = '/home/sagar/Dropbox'
global PATH

def esccape_sequence(path):
    """Insert the escape sequence in the path."""
    chars = {r' ':r'\ ', r'(':r'\(', ')':r'\)', 
            r"[":r"\[", r"]":r"\]", r"{":r"\{", r"}":r"\}", r'"':r"\"", r"'":r"\'"}
    for i in range(len(chars)):
        temp = chars.items()[i]
        path = path.replace(temp[0], temp[1])
    return path

def resolvePath(allPath):
    """Dropbox treats the file names in a case-insensitive. Accepts case-insensitive path 
    and returns case-sensitive path."""
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
    """Generate all paths from the changed file(child) to the dropbox(parent) directory."""
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
                else:
                    command = "gvfs-set-attribute /"+temp+" -t unset metadata::emblems"
                commands.getoutput(command)
            items.pop()

def getpaths(entries):
    """Extract paths"""
    paths = []
    for entry in entries:
        if entry[1]:
            paths.append(entry[0])
    return paths

def deltaway(cursor):
    """Get path of the changed files and add status-icon to them."""
    # cursor_key = cursor.get('cursor')
    # cursor_file = open('cursor','w')
    # cursor_file.write(cursor_key)
    # cursor_file.close()

    items = cursor.get('entries')

    entry_file = open('entries', 'r')
    temp = entry_file.read()
    entry_file.close()
    entry_file = open('entries', 'w')

    if items:
        paths = getpaths(items)
        paths = resolvePath(paths)
        if temp:
            temp = eval(temp)
            paths = paths + temp
        entry_file.write(str(paths))
        generatePath(paths, True)
    
    entry_file.close()

    # subprocess.Popen(["nautilus"])

def main():
    """Unmark previously marked files(if any) and get list of recently changed-files."""

    global PATH

    path_data = open("path.json")
    p = json.load(path_data)
    PATH = p["dropbox"]
    assert(len(PATH)),"Add dropbox path to path.json"

    client_data = open("client.json") 
    credentials = json.load(client_data)
    access_token = credentials["access_token"]
    assert(len(access_token)), "Empty 'access_token'." 

    client = dropbox.client.DropboxClient(access_token)
    try:
        info = client.account_info()
        print "Name: %s\nEmail: %s" % (info.get('display_name'), info.get('email'))
    except Exception as exp:
        if type(exp).__name__ == "RESTSocketError":
            print 'Network Error. Check your Internet connection!'
            exit(0)
    
    previous_entry_file = open('entries', 'r')
    previous_entries = previous_entry_file.read()
    if previous_entries:
        previous_entries = eval(previous_entries)
    previous_entry_file.close()

    if previous_entries:
        paths = previous_entries
        generatePath(paths, False)

    previous_entry_file = open('entries', 'w')
    previous_entry_file.close()

    cursor_file = open('cursor','r')
    cursor = cursor_file.read()
    cursor_file.close()

    count = 0
    flag = 0

    if not(cursor):
        flag = 1

    while(1):
        try:
            cursor = client.delta(cursor)
        except Exception as exp:
            if type(exp).__name__ == "RESTSocketError":
                print 'Network Error. Check your Internet connection!'
            elif type(exp).__name__ == "ErrorResponse":
                print 'Invalid cursor key! Need to generate cursor again.'
                flag = 1
                cursor = ""
                continue
        #write cursor to the cursor-file.
        cursor_key = cursor.get('cursor')
        cursor_file = open('cursor','w')
        cursor_file.write(cursor_key)
        cursor_file.close()
        if flag == 0:
            deltaway(cursor)
        if not(cursor.get('has_more')):
            break
        else:
            cursor = cursor.get('cursor')
        count += 1
        print count

    print 'Refresh nautilus.'

if __name__ == '__main__':
    main()
