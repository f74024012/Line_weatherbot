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


minus=False

angry=""
weather_key=settings.WEATHER_KEY





class Tainan:
    pass
def tainan_weather(weatherarg):
    answer=0
    web='http://opendata.cwb.gov.tw/opendataapi?dataid=F-C0032-001&authorizationkey='+weather_key
    filehandler=ur.urlopen(web)
    count=0
    for line in filehandler:
        line=str(line,"utf8")
        #line=line.strip()
        #angry+=line
        #return line
        #line = str(line,"utf8")
        #return "kkkkkk"
        if weatherarg in line:
            answer=1
        #return "aaaaaaaa"
        if answer==1:
            #return "ssssssss"
            if 'parameterName' in line:
                weatherlist=line.split('>')
                weatherfinal=weatherlist[1].split('<')
                answer=0
                return weatherfinal[0]
        #return "GGGGGGGGG"
#return "eeeeeeee"
def test():
    web='http://opendata.cwb.gov.tw/opendataapi?dataid=F-C0032-001&authorizationkey='+weather_key
    filehandler=ur.urlopen(web)
    s=filehandler.read()

#return weatherfinal[0]
#break
#print(line)
#print(s)

#print (web)
#print (weather_key)
@csrf_exempt
def callback(request):
    city=["臺北市","新北市","桃園市","臺中市","臺南市",
          "高雄市","基隆市","新竹市","嘉義市","新竹縣","苗栗縣",
          "彰化縣","南投縣","雲林縣","嘉義縣","屏東縣","宜蘭縣",
          "花蓮縣","臺東縣","臺東市","澎湖縣","金門縣","連江縣"]
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
                        str_weather=tainan_weather('臺南市')
                        #str_weather=test()
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='臺南'+str_weather)
                        )
                    if '天氣如何？' in event.message.text:
                        citylist=event.message.text.split('天')
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=citylist[0])
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=event.message.text)
                        )


        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()