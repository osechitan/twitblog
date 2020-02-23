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
    context = get_user_tweets(request.user.id)
    return render(request,'user_auth/top.html',context)


def get_user_tweets(user_id):
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    env = environ.Env(DEBUG=(bool, False))
    env.read_env('.env')

    params = {
        'exclude_replies': True,
        'include_rts': False,
        'count': 50,
        'trim_user': False,
        'tweet_mode': 'extended',
    }
    user = UserSocialAuth.objects.get(user_id)
    # oauth認証開始
    twitter = OAuth1Session(
        env.get_value('SOCIAL_AUTH_TWITTER_KEY', str),
        env.get_value('SOCIAL_AUTH_TWITTER_SECRET', str),
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
    else:
        print('通信失敗')

    context = {'tweets':tweets_text, 'name':results[0]['user']['name']}

    return context