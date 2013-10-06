###What is delta-dropbox?

###Prerequisite
dropbox
    sudo pip install dropbox

### Dropbox-setup

Follow these steps to setup Dropbox app:

1. You will need to create Dropbox app. Go to this url [dropbox app](https://www.dropbox.com/developers/apps)
    Follow the steps and set the permission type of the app.

2. On successful creation of app, Dropbox will provide with `app_key` and `app_secret`. 
    Do not publicize these app credentials.

3. Insert the `app_key` and `app_secret` in the `client.json` file.

Execute the `setup.py` file.

Now insert the `access_token` and `user_id` in the `client.json` displayed by the setup.py file.

Add your dropbox path to `path.json` file.

Now execute the file `delta-dropbox.py`
It will talk time to complete it's execution depending upon the total files in dropbox folder.
