from django.conf.urls import url

from msg.views import sms_reg, sms_login

urlpatterns = [
    # url(r'^<uid>', UserView.as_view()),
    url(r'^v1/sms/reg', sms_reg),
    url(r'^v1/sms/login', sms_login),
]