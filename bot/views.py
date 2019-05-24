import os
import datetime

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils import timezone

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextMessage, TextSendMessage,
    FlexSendMessage,BubbleContainer, CarouselContainer,
    BoxComponent,TextComponent,ButtonComponent,
    BubbleStyle,BlockStyle
)

from tutbusinfo.models import Station,TableIndex,TableBasic

## LINE MESSAGE PROCESSING
line_bot_api = LineBotApi(
        os.environ['YOUR_CHANNEL_ACCESS_TOKEN']
    )

parser = WebhookParser(
        os.environ['YOUR_CHANNEL_SECRET']
    )


@csrf_exempt
def reply(request):
    ##nowtime
    now = timezone.now() + datetime.timedelta(hours=9)
    yobi = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    day = now.weekday()
    time = now.time()
    
    if request.method != 'POST':
        return HttpResponse('禁止されたアクセスです', status=405)

    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseBadRequest()

    for event in events:
        if day == 6:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="本日、バスは運行しておりません"))
        else:
            station_name = event.message.text
            if station_name == "Hachioji" or station_name == "Minamino" or station_name == "Dormitory":
                if day == 5:
                    table_name = "weekend"
                else:
                    table_name = "basic"
                    
                try:                    
                    s = Station.objects.get(name=station_name)
                    t = s.tableindex_set.get(name=table_name)
                    rows = t.tablebasic_set.filter(arrive_station__gte=time).order_by('left_campus')[:3]
                    #rows = t.tablebasic_set.filter(arrive_station__lte=time).order_by('left_campus')[:3]
                    
                    if len(rows) > 0:
                        bubbles = []
                        
                        for row in rows:
                            bubble = createBubbleContainer(
                                    station_name = station_name,
                                    what_day = yobi[day],
                                    time1 = row.left_campus.strftime("%H:%M"),
                                    time2 = row.arrive_station.strftime("%H:%M"),
                                    time3 = row.arrive_campus.strftime("%H:%M")
                                    )
                            bubbles.append(bubble)
                            
                        flex_message = FlexSendMessage(
                                alt_text="Flex Message",
                                contents = CarouselContainer(
                                        contents = bubbles
                                        )
                                )
                    
                        line_bot_api.reply_message(event.reply_token,flex_message)
                    
                    else:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="本日の運行は終了しました"))
                    
                except LineBotApiError:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="読み込みに失敗しました"))
                        
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="場所を入力してください"))
                
    return HttpResponse(status=200)


def createBubbleContainer(station_name,what_day,time1,time2,time3):
    bubble =  BubbleContainer(
            direction = "ltr",
            header = BoxComponent(
                    layout = "vertical",
                    contents = [
                            BoxComponent(
                                    layout = "horizontal",
                                    contents = [TextComponent(text = station_name,weight = "bold"),TextComponent(text = what_day)]
                                    )
                            ]
                    ),
            body = BoxComponent(
                    layout = "vertical",
                    contents = [
                            BoxComponent(
                                    layout = "horizontal",
                                    contents =[TextComponent(text = "↓Campus"),TextComponent(text = time1)]
                                    ),
                            BoxComponent(
                                    layout = "horizontal",
                                    contents =[TextComponent(text = "↓"+station_name),TextComponent(text = time2)]
                                    ),
                            BoxComponent(
                                    layout = "horizontal",
                                    contents =[TextComponent(text = "↓Campus"),TextComponent(text = time3)]
                                    )
                            ]
                    ),
            styles = BubbleStyle(
                    body = BlockStyle(
                            separator = True
                            )
                    )
            )
    return bubble
