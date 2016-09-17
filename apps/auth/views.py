#_*_coding:utf-8_*_

import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from apps.auth.serializers import AuthTokenSerializer
from apps.kx.models import KxUser,KxUserlogin
from hashlib import md5
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        email = request.POST.get('email','')
        appMac = request.POST.get('appMac','')
        lanIp = request.POST.get('lanIp','')
        wlanIp = request.META['REMOTE_ADDR']
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            token, created = Token.objects.get_or_create(user = serializer.object['user'])

            #为了多点登录，需要返回本人的其他ip和mac信息
            loginUserList = []

            #多点登录的话在appMac最后加一个字母来标识
            resultMac = appMac
            suffix = chr(ord('A')-1)
            for loginUser in KxUserlogin.objects.filter(email__exact=email).values('mac','lan_ip', 'wlan_ip'):
              suffix = chr(ord(suffix)+1)
              resultMac = appMac[0:-1]+suffix
              loginUserList.append(loginUser)
              if appMac[0:-1] == loginUser['mac'][0:-1]:
                resultMac = appMac
                break

            logger.info("===appMac:"+appMac+"====resultMac:"+resultMac+"====len:"+str(len(loginUserList)))
             
            if resultMac != appMac or len(loginUserList) == 0:
              KxUserlogin.objects.create(email=email, mac=resultMac, lan_ip=lanIp, wlan_ip=wlanIp)

            return Response({'token': token.key, 'ip':wlanIp, 'email':user.email, 'nick':user.nick, 'loginList':loginUserList, 'appMac':resultMac})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


obtain_auth_token = ObtainAuthToken.as_view()



class Register(ObtainAuthToken):

    def post(self, request):
       email = strip_tags(request.POST.get("email").strip().lower())
       nick = email
       password = request.POST.get("password").strip() 
       count = KxUser.objects.filter(email=email).count()
       if count >0:
            return Response({'status': '-1'})

       uid = md5(email).hexdigest()
       create_user=KxUser.objects.create_user(uuid=uid,email=email,nick=nick,password=password,status=0)
       create_user.save()

       return super(Register,self).post(request);


api_register = Register.as_view() 

