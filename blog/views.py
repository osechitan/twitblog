from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
import json
import environ
from requests_oauthlib import OAuth1Session
from blog.models import User

@login_required
def top_page(request):
    print(request)
    #user = UserSocialAuth.objects.get(user_id=request.user.id)
    #oauth_token = user.access_token['oauth_token']
    #oauth_token_secret = user.access_token['oauth_token_secret']
    user = createNewUser(request)
    #user = User.objects.filter(twitterId)
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    env = environ.Env(DEBUG=(bool,False))
    env.read_env('.env')

    params = {
               #'user_id': user.twitterId,
               'exclude_replies': True,
               'include_rts': False,
               'count': 20,
               'trim_user': False,
               'tweet_mode': 'extended',
    }
    twitter = OAuth1Session(
        env.get_value('SOCIAL_AUTH_TWITTER_KEY',str),
        env.get_value('SOCIAL_AUTH_TWITTER_SECRET',str),
        user.oauth_token,
        user.oauth_token_secret,
    )
    response = twitter.get(url, params=params)
    if response.status_code == 200:
        #print('status_code：{0}'.format(response.status_code))
        results = json.loads(response.text)
        tweets_text = []

        for tweet in results:
            tweets_text.append(tweet['full_text'])

    else:
        print('通信失敗')
        print(response.status_code)
        results = 'aaa'

    return render(request,'user_auth/top.html',{'tweets': tweets_text})

def createNewUser(request):
    user = UserSocialAuth.objects.get(user_id=request.user.id)

    newUser = User(
                    userId = request.user.id,
                    twitterId = user.access_token['screen_name'],
                    oauth_token = user.access_token['oauth_token'],
                    oauth_token_secret = user.access_token['oauth_token_secret']
                  )
    newUser.save()
    return newUser
