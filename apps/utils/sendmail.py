#_*_coding:utf-8_*_
from django.core.mail import EmailMultiAlternatives
import threading,logging,time,random

logger = logging.getLogger(__name__)



class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        #msg.content_subtype = "html"
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        try:
            time.sleep(random.randint(0,9))
            msg.send(self.fail_silently)
            logger.info("recipient:%s",self.recipient_list)
        except Exception as e:
            logger.debug("Send email error:%s",e)

def send_mail_thread(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()
