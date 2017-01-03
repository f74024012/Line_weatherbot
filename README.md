# Line_weatherbot
weather information and echo
##demo
<img width="732" alt="2016-12-31 6 02 26" src="https://cloud.githubusercontent.com/assets/6111736/21576993/3d5def84-cf84-11e6-8e2a-a8bbe35dad7a.png">

##環境變數
SECRET_KEY

LINE_CHANNEL_ACCESS_TOKEN

LINE_CHANNEL_SECRET

WEATHER_KEY (向中央氣象局開放資料平臺申請為會員後，即可得到)

setup:

`export SECRET_KEY='Your django secret key'`

`export LINE_CHANNEL_ACCESS_TOKEN='Your line channel access token'`

`export LINE_CHANNEL_SECRET='Your line channel secret'`

`export WEATHER_KEY='your weather key'`

##聊天規則

1. 輸入"今天天氣？"，則回答臺南市天氣資訊 ex:臺南多雲
   
   注意：？須用中文輸入法
2. 當輸入內容包括縣市名與天氣，則回答該縣市之天氣資訊  
   注意：？須用中文輸入法
3. 如不吻合以上兩種情況，則echo

##開發環境
python-3.5.2

##套件
Django==1.10.4

future==0.16.0

line-bot-sdk==1.0.2

requests==2.12.4

gunicorn==19.0.0
