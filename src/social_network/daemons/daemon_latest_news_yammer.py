from social_network.services.yammer_service import YammerService
from social_network.services.db_service import DBServiceSocialNetwork
from social_network.api.parsers.yammer_parser import YammerParser
from news.models import News
import threading
import datetime
import os
import time


class DaemonLatestNewsYammer:

    def __init__(self,
                 yammer_service:YammerService,
                 yammer_parser:YammerParser,
                 db_service:DBServiceSocialNetwork):

        self.yammer_service = yammer_service
        self.yammer_parser = yammer_parser
        self.db_service = db_service
        self.worker:threading.Thread = None
        self.lock = threading.Lock()
        self.runnable = False


    def is_run(self):
        if self.worker != None and self.runnable == True:
            return True
        else:
            return False

    def try_start(self):

        if self.yammer_service.is_auth() == False:
            return Exception('yammer not authorized')

        if self.is_run():
            return  Exception('worker is running')

        self.worker = threading.Thread(target=self.worker_handler, args=(), kwargs={})
        self.runnable = True
        self.worker.start()

    def stop(self):
        self.lock.acquire(1)
        self.runnable = False
        self.lock.release()


    def worker_handler(self):
        while self.runnable:

            if self.yammer_service.is_auth() == False:
                return

            try:
                groups = self.yammer_service.try_get_groups()
            except:
                time.sleep(15)

            convert_yammer_groups = self.yammer_parser.convert_groups(yammer_groups=groups)
            if convert_yammer_groups != None:
                self.db_service.try_save_or_update_groups(convert_yammer_groups, type='yammer')

            self.load_new_messages_from_all_groups()
            time.sleep(300)

    def load_new_messages_from_all_groups(self):
        all_groups = self.db_service.gel_all_groups()
        for group_db in all_groups:

            newest_news:News = self.db_service.get_newest_news(group_db)

            try:
                if newest_news != None:
                    messages_yammer = self.yammer_service.try_get_messages(group_id=str(group_db.group_id),
                                                                           newest_message_id=str(newest_news.news_id))
                else:
                    messages_yammer = self.yammer_service.try_get_messages(group_id=str(group_db.group_id))
            except:
                time.sleep(10)

            convert_yammer_messages = self.yammer_parser.convert_messages(messages_yammer)
            self.db_service.try_save_or_update_news(convert_yammer_messages, group_db.group_id)
            time.sleep(8)

