##What is delta-dropbox?
As they say, *Neccesity is the mother of Invention!*. Story behind `delta-dropbox.py` is, I had a shared folder in dropbox with few friends for a project. All of them  used to add many files, directories to these folder. Now when these files used to get sync with my local Dropbox directory, Dropbox used to notify me.

![dropbox-notify](https://raw.github.com/sagarrakshe/delta-dropbox/master/_assets/dropbox-notify.png)

But dropbox specifies the total no. of files added to dropbox but it doesn't specifies which files and where they were added. I need to figure out which files were added and where. Consider a case where 100 files are changed in your dropbox folder! It would be tedious.<br>

So `delta-dropbox.py` is a hack that marks (adds `status-icon`) these newly added files. On subsequent execution unmarks the previously marked files and then mark newly added, modified files if any. <br>
The star on **Temp** denotes it was recently added. To guide to the changed file, all files or directories are marked in the path. In this case the path is **Dropbox/Experiment/Temp** so *Dropbox*, *Experiment* and *Temp* will be marked. So user is guided when he enters in Dropbox folder. 

![dropbox-mark](https://raw.github.com/sagarrakshe/delta-dropbox/master/_assets/dropbox-mark.png)

I have used the [/delta](https://www.dropbox.com/static/developers/dropbox-python-sdk-1.6-docs/#dropbox.client.DropboxClient.delta) api of dropbox to get the list of changed files. And to set status-icon the `gvfs-set-attribute` command is used.

##Test
Basically, the code will work only if the command `gvfs-set-attribute` works on your machine because this command sets the file attribute. So to test whether it works or not follow the steps: 

    $ git clone https://github.com/sagarrakshe/delta-dropbox
    $ cd delta-dropbox
    $ sh test.sh

Nautilus will open, if a status-icon is added to the `test.sh`(*star* or *plus* icon depending upon the version of gnome-shell) then it's fine. See the image below. Else try refreshing the nautilus even if it doesn't set then the code won't work for you.

![dropbox-test](https://raw.github.com/sagarrakshe/delta-dropbox/master/_assets/dropbox-test.png)

##Installation

##Prerequisite

    dropbox
You can install using pip:

    $ sudo pip install dropbox

##Dropbox App Setup

Follow these steps to setup Dropbox app:

1. You will need to create Dropbox app. Create an app here [dropbox app](https://www.dropbox.com/developers/apps). Follow the steps and set the permission type of the app.
2. On successful creation of app, Dropbox will provide with `app_key` and `app_secret`. Do not publicize these app credentials.
3. Insert the `app_key` and `app_secret` in the `client.json` file.

##Setup

* Run the `setup.py` file. <br>
* It will open a link in browser. 
* Click **Allow** to give access to that app. Copy the given code and paste in the terminal.
* On successful execution of `setup.py`, it will print `access_token`and `user_id`.
* Add `access_token` and `user_id` to `client.json`.
* Two new files will be created by `setup.py`, `cursor` and `entries`. (don't delete them!)
* Add your Dropbox directory path to `path.json` file.(like mine is /home/sagar/Dropbox)
* Now run the file `delta-dropbox.py`. It will take time to execute, depending on the total files in your dropbox folder.

##Usage
Now add few files to your dropbox directory, let it sync with the cloud or add files to cloud and let it sync with local directory. On complete sync run `delta-dropbox.py`

    $ python delta-dropbox.py

Open nautilus or refresh it. Check if the added files got marked or not.

##Issues
* Tested only on Ubuntu, (will work where `gvfs-set attribute` works).
* Execute `delta-dropbox.py` only when Dropbox has sync all files or Dropbox folder status is Idle or else some files which are syncrhonizing may not be marked.
* Need to execute the code manually.
* Effects visible only in file browser(nautilus) and not through command-line.
