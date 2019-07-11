
class ServiceSmsDeliveryException(Exception):
    pass

class ServiceSmsDelivery:

     def try_send_sms(self, phone, sms):
         print(10)