import base64
import os

import pyotp

from apps.auth_service.utils.smsc_api import SMSC


class ConcreteSMSAPI:
    def send_sms(self, phone_number, message, smsc):
        print('Send SMS to %s: %s' % (phone_number, message))
        # status = smsc.send_sms(
        # 		f"+7{phone_number}",
        # 		"1Post тіркелу коды: %s. Тіркеуді аяқтау үшін осы кодты енгізіңіз." % message,
        # 		sender=True
        # )
        # print('SMS status: %s' % status)
        return True

    def send_sms_async(self, phone_number, message):
        # Send SMS async
        pass
        return True


class SMSAPI:
    def __init__(self):
        self._api = None
        self._base_api = None

    def generate_otp(self, phone_number):
        #  Generate OTP for phone number length 4
        totp = pyotp.TOTP(base64.b32encode(os.urandom(16)).decode('utf-8'), digits=6)
        otp = totp.now()
        return otp

    def generate_otp_message(self, phone_number):
        otp = self.generate_otp(phone_number)
        message = "Your verification code is: %s" % otp
        return otp, message

    def send_sms(self, phone_number, ):
        if not self._api:
            self._api = ConcreteSMSAPI()
        if not self._base_api:
            self._base_api = SMSC()
        otp, message = self.generate_otp_message(phone_number)
        if self._api.send_sms(phone_number, otp, self._base_api):
            return otp, message
        return None, "Invalid phone number."

    def send_sms_async(self, phone_number):
        if not self._api:
            self._api = ConcreteSMSAPI()
        otp, message = self.generate_otp_message(phone_number)
        if self._api.send_sms_async(phone_number, message):
            return otp, message
        return None, "Invalid phone number."
