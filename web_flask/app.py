from flask import Flask, render_template, request, redirect, url_for
from models.user import User
from models.storage import storage
from models.bucket import Bucket
import os
import json

"""Setup flask to make site functional"""

app = Flask(__name__, static_url_path='/static')

file_path = "client_secret_1088266269277-0nijetd5bla0ukdhehem63jcjs1djjfq.apps.googleusercontent.com.json"
pwd = os.getcwd()
new_fp = os.path.join(pwd, file_path)

try:
    print(os.path.exists(new_fp))
    with open(file_path) as f:
        file: dict = json.load(f)
        client_id: str = file.get('client_id')
        redirect_uri: str = file.get('redirect_uri')
        print(redirect_uri)

except FileExistsError as e:
    print(e)

scopes = ['openid', "https://www.googleapis.com/auth/userinfo.profile", 'https://www.googleapis.com/auth/youtube.readonly']

newInstance: object = None
user_url: str
@app.get('/')
def home():
    return render_template('index.html')

# @app.get('/log-on')
# def logme_in():
#     return render_template('login_page.html')

@app.get('/log-on')
def login():
    #global username
    global scopes
    global new_fp
    global newInstance
    global storage
    #username = str(request.form.get("username"))
    #existing_instance = User.get_instance(username)
    #if existing_instance is False:
    newInstance = User("", new_fp, scopes)
    #newInstance.set_storage(storage)
    #storage = storage.set_userclass(newInstance)
    if newInstance.authenticate() is False:
        return render_template('failure.html')
    else:
        existing_instance = User.get_instance(newInstance.username)
        if existing_instance is False:
            newInstance.login()
            User.Instances.append(newInstance)
            return redirect(url_for('user', username=newInstance.username))
        else:
            index = User.Instances.index(newInstance)
            User.Instances.pop(index)
            newInstance = existing_instance
            newInstance.login()
            return redirect(url_for('user', username=newInstance.username))
    # if  is False:
        #     return render_template('failure.html')
        # else:
    #     #     user(newInstance)
    # else:
    #     if existing_instance is not False:
    #         newInstance = existing_instance
    #         newInstance.login()
    #         return redirect(url_for('user', username=username, instance=newInstance))

@app.get('/user/<username>')
def user(username):
    global user_url
    user_url = url_for('user', username=username)
    return render_template('USER.html', username=username, user_url=user_url)

@app.get('/user/<username>/Subscriptions')
def get_subs(username):
    global newInstance
    subscriptions: dict = newInstance.SubscriptionList
    return render_template('SUBSCRIPTIONS.html', subscriptions=subscriptions, username=username)

@app.get('/get_bucket')
def load_bucket():
    global newInstance
    requested = request.args.get('bucket')
    fullVideo= []
    for sub in newInstance.Buckets.BucketList[requested]:
        videos = newInstance.get_recent_videos(sub['snippet']['channelId'])
        for video in videos:
            if 'id' in video and 'videoId' in video['id']:
                fullVideo.append(video['id']['videoId'])
    return render_template('view.html', video_ids=fullVideo, bucket=requested)

@app.get('/user/<username>/Feed')
def recent_feed(username):
    global newInstance
    fullVideo = []
    subscriptions = newInstance.SubscriptionList
    for sub in subscriptions['items']:
        videos = newInstance.get_recent_videos(sub['snippet']['channelId'])
        for video in videos:
            if 'id' in video and 'videoId' in video['id']:
                fullVideo.append(video['id']['videoId'])
    return render_template('view.html', video_ids=fullVideo, bucket='Recent Feed', username=username)

@app.get('/user/<channel>/view')
def channelVideos(channel):
    global newInstance
    fullVideo = []
    title = request.args.get('channel')
    videos = newInstance.get_recent_videos_by_channel_name(title)
    if videos is []:
        return render_template('novideos.html', bucket=title, username=newInstance.username)
    for video in videos:
        if 'id' in video and 'videoId' in video['id']:
            fullVideo.append(video['id']['videoId'])
    return render_template('view.html', video_ids=fullVideo, bucket=title, username=newInstance.username)

@app.get('/user/<username>/Buckets')
def send_Buckets(username):
    global newInstance
    buckets: dict = newInstance.user_buckets()
    return render_template('buckets.html', buckets=buckets, username=username)

@app.post('/create_bucket')
def create_bucket():
    global newInstance
    BucketName = request.form.get('name')
    newInstance.Buckets.create_bucket(BucketName)
    return redirect(url_for('update_bucket', bucket=BucketName))

@app.get('/update_bucket')
def update_bucket():
    global newInstance
    BucketName = request.args.get('bucket')
    subscriptions = newInstance.SubscriptionList
    return render_template('updateBucket.html', buckets=BucketName, subscriptions=subscriptions, username=newInstance.username)

@app.post('/update-form/<bucket>')
def do_update(bucket):
    global newInstance
    updateList = request.form.getlist('subscription_title')
    check = newInstance.Buckets.bucket_update(bucket, updateList)
    return redirect(url_for('send_Buckets'))

if __name__ == '__main__':
    app.run(debug=True)