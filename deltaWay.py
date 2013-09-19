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

def main():
    """Get the cursor string."""
    access_token = 'eTKE3pt6sBMAAAAAAAAAAcdcs4ikpR9toVVzPXARi9HOdVkFlR5pgOdJk6NzK-Pj'
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
    
    items = cursor.get('entries')
    entryFile = open('entries','w')
    entryFile.write(str(items))
    entryFile.close()

if __name__ == '__main__':
    main()