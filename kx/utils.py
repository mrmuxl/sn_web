#_*_coding:utf-8_*_
from django.core.validators import email_re

def get_client_ip(request):
    pass
    
def is_valid_email(email):
    if email_re.match(email):
        return True
    return False
