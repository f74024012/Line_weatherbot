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

weather_key=settings.WEATHER_KEY

#print (weather_key)

class Weather:
    pass
def city_weather(weatherarg):#find out the weather in "weatherarg" city
    answer=0 #after the query city be found,the value changes to 1
    web='http://opendata.cwb.gov.tw/opendataapi?dataid=F-C0032-001&authorizationkey='+weather_key
    filehandler=ur.urlopen(web)
    for line in filehandler:
        line=str(line,"utf8")
        if weatherarg in line: #search the query city's name
            answer=1
        if answer==1:
            if 'parameterName' in line: #search the query city's weather information
                weatherlist=line.split('>') #parsing xml
                weatherfinal=weatherlist[1].split('<') #parsing xml
                answer=0
                return weatherfinal[0] #final weather information

@csrf_exempt
def callback(request):
    city=["臺北市","新北市","桃園市","臺中市","臺南市",
          "高雄市","基隆市","新竹市","嘉義市","新竹縣","苗栗縣",
          "彰化縣","南投縣","雲林縣","嘉義縣","屏東縣","宜蘭縣",
          "花蓮縣","臺東縣","澎湖縣","金門縣","連江縣"]
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    if event.message.text == '今天天氣？':  #answer ex: 臺南多雲
                        str_weather=city_weather('臺南市') #search Tainan weather
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='臺南'+str_weather)
                        )
                    elif '天氣' in event.message.text: #answer ex: 臺北市多雲
                        #citylist=event.message.text.split('天')
                        cityrequest=' '
                        word_set=set(city)
                        phrade_set=set(event.message.text.split())
                        if word_set.intersection(phrade_set):
                            last_weather=city_weather(word_set)
                            line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text=word_set+lastweather)
                            )
                        else:#city not exist,echo
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=event.message.text)
                            )
                    else:#echo
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=event.message.text)
                        )


        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()