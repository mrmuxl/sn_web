from rest_framework.views import APIView
from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from auth.serializers import AuthTokenSerializer
from kx.models import KxUser
from hashlib import md5
from django.utils.html import strip_tags

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])
            return Response({'token': token.key, 'ip':request.META['REMOTE_ADDR']})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


obtain_auth_token = ObtainAuthToken.as_view()

class Register(APIView):

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

