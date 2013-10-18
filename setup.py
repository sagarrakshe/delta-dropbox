import dropbox
import json
import webbrowser

client_data = open("client.json")
credentials = json.load(client_data)
app_key = credentials["app_key"]
app_secret = credentials["app_secret"]

assert (len(app_key)), "Empty 'app_key'."
assert (len(app_secret)), "Empty 'app_secret'."

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()

print '1. Go to: ' + authorize_url
webbrowser.open(authorize_url, new=2)
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorizaion code.'
code = raw_input("Enter the authorization code here: ").strip()

try:
    access_token, user_id = flow.finish(code)

    print '\naccess_token: ', access_token
    print 'user_id: ', user_id
    
    auth_info={'access_token': access_token, 'user_id':user_id}
    
    with open('client.json','r') as c_json:
        app_key=json.load(c_json)
        c_json.close()
    
    with open('client.json','w') as c_json:    
        app_key.update(auth_info)
        c_json.write(json.dumps(app_key))
        c_json.close()
    
    #print '\nAdd the "access_token" and "user_id" to "client.json" file.'

    cursor = open('cursor','w')
    cursor.close()

    entries = open('entries','w')
    entries.close()

except dropbox.rest.ErrorResponse, e:
    print 'Error: %s' % (e)
