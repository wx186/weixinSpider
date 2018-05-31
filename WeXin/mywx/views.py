from django.shortcuts import render, HttpResponse
from wechatpy.crypto import WeChatCrypto
from wechatpy import parse_message, create_reply
from wechatpy.replies import ImageReply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.exceptions import InvalidAppIdException
import os
from django.views.decorators.csrf import csrf_exempt

TOKEN = "zyr"
APPID = 'wxe85c53c9696262f8'
AppSecret = 'ed626ff1a285bf475670d8cc458820c5'

@csrf_exempt
def index(request):
    if request.method == 'GET':
        return auth(request)
    elif request.method == 'POST':
        print(request.body)
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = create_reply(msg.content, msg)
            return HttpResponse(reply, content_type='application/xml')
        elif msg.type == 'image':

            return HttpResponse('', content_type='application/xml')
        return HttpResponse("")

def auth(request):
    signature = request.GET.get("signature")
    timestamp = request.GET.get("timestamp")
    nonce = request.GET.get("nonce")
    echostr = request.GET.get("echostr")
    check_signature(TOKEN, signature, timestamp, nonce)
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        return HttpResponse("456")
    return HttpResponse(echostr, content_type='application/xml')