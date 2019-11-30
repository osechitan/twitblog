from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
import json
import environ
from requests_oauthlib import OAuth1Session
from blog.models import User
import datetime
from django.http import HttpResponse


def top_page(request):
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    env = environ.Env(DEBUG=(bool,False))
    env.read_env('.env')

    params = {
               #'user_id': user.twitterId,
               'exclude_replies': True,
               'include_rts': False,
               'count': 50,
               'trim_user': False,
               'tweet_mode': 'extended',
    }
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    #oauth認証開始
    twitter = OAuth1Session(
        env.get_value('SOCIAL_AUTH_TWITTER_KEY',str),
        env.get_value('SOCIAL_AUTH_TWITTER_SECRET',str),
        user.access_token['oauth_token'],
        user.access_token['oauth_token_secret'],
    )
    response = twitter.get(url, params=params)
    if response.status_code == 200:
        results = json.loads(response.text)
        tweets_text = []
        count = 0
        #ツイートを20件表示
        for tweet in results:
            tweets_text.append(tweet['full_text'])
            count += 1
            if count == 20:
                break

        response = HttpResponse("Cookie Set")
        set_cookie(response, 'oauth_token', user.access_token['oauth_token'], 365*24*60*60)
        set_cookie(response, 'oauth_token_secret', user.access_token['oauth_token_secret'], 365*24*60*60)
        print(user.access_token['oauth_token'])
        print(request.COOKIES.get('oauth_token'))
        print(request.COOKIES.get('oauth_token_secret'))

    else:
        print('通信失敗')
        print(response.status_code)
        results = 'aaa'
    return render(request,'user_auth/top.html',{'tweets': tweets_text,'name':results[0]['user']['name']})
    #return render(request,'user_auth/login_complete.html')

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

def set_cookie(response, key, value, max_age):

    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires)

def my_page(self, request, slug):
    print(request)
    self.object = self.get_object()
    context = self.get_context_data(object=self.object)
    #print(request.COOKIES.get('oauth_token'))
    #print(request.COOKIES.get('oauth_token_secret'))
    return render(request,'user_auth/top.html',context=context)
