from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import urllib.request as ur

# Create your views here.

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

count=8
minus=False
answer=False
angry=""
weather_key=settings.WEATHER_KEY
class Tainan:
    pass
def tainan_weather():
    web='http://opendata.cwb.gov.tw/opendataapi?dataid=F-C0032-001&authorizationkey='+weather_key
    filehandler=ur.urlopen(web)
    for line in filehandler:
        line=str(line,"utf8")
        line=line.strip()
        angry+=line
        #return line
        #line = str(line,"utf8")
        #return "kkkkkk"
        if '臺北市' in str(line,"utf8"):
            answer=True
            return "aaaaaaaa"
        elif answer==True:
            return "ssssssss"
            if 'parameterName' in str(line,"utf8"):
                weatherlist=line.split('>')
                weatherfinal=weatherlist[1].split('<')
                #print(weatherfinal[0])
                answer=False
                return "GGGGGGGGG"
    return angry
def test():
    return "rrrrrrr"
#return weatherfinal[0]
#break
#print(line)
#print(s)

#print (web)
#print (weather_key)
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        #weather=Tainan()
        #print (weather)
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    if event.message.text == '今天天氣？':
                        str_weather=tainan_weather()
                        #str_weather=test()
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='臺南'+str_weather)
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=event.message.text)
                        )


        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()