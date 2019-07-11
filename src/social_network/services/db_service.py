from social_network.models import SocialNetworkSite
from news.models import NewsGroup, News, NewsAttach
from datetime import datetime, timedelta, time
from django.db import transaction

class DBServiceSocialNetwork:

    def try_create_or_update_social_network_access_token(self, name, access_token):
        try:
            network_model = SocialNetworkSite.objects.get(name=name)
        except SocialNetworkSite.DoesNotExist:
            raise ValueError('yammer network model not found')

        network_model.token = access_token
        network_model.save()

    def try_get_social_network_site(self, name):

        try:
            network_model = SocialNetworkSite.objects.get(name=name)
        except SocialNetworkSite.DoesNotExist:
            network_model = None

        return network_model

    @transaction.atomic
    def try_save_or_update_groups(self, groups_dict, type):

        try:
            groups = groups_dict['groups']
        except:
            return

        for group in groups:
            try:
                group_id = group['id']
                name = group['name']
                description = group['description']

                try:
                    group_db = NewsGroup.objects.get(group_id=group_id)
                except NewsGroup.DoesNotExist:
                    group_db = NewsGroup.objects.create(group_id=group_id, name=name, type=type)

                group_db.description = description
                group_db.name = name
                group_db.save()

            except Exception as ex:
                print(ex)
                continue

    def gel_all_groups(self):
        groups = NewsGroup.objects.all()
        return groups

    def get_newest_news(self, group):
        try:
            news_list = News.objects.order_by('date_created').filter(group=group)
        except Exception as ex:
            return None

        return news_list.last()

    def get_oldest_news(self, group):
        try:
            news_list = News.objects.order_by('date_created').filter(group=group)
        except Exception as ex:
            return None

        return news_list.first()


    def get_all_news_list(self,
                          start_date=None,
                          end_date=None,
                          count=None):

        try:
            if start_date != None and end_date != None:
                news_list = News.objects.extra(where={"date_created > " + str(start_date) +" AND date_created < "+ str(end_date)}).order_by('date_created')
            elif start_date != None:
                news_list = News.objects.extra(where={"date_created > " + str(start_date)}).order_by('date_created')
            elif end_date != None:
                news_list = News.objects.extra(where={"date_created < " + str(end_date)}).order_by('date_created')
            else:
                news_list = News.objects.all()

            if count != None:
                result = news_list.reverse()[:count]
            else:
                result = news_list

            return result


        except Exception as ex:
            return []


    def get_news_list_selected_groups(self,
                                      groups_id_list:list,
                                      start_date=None,
                                      end_date=None,
                                      count=None):

        groups_query_str = ''

        for (index,group_id) in enumerate(groups_id_list):
            groups_query_str += ' group_id=' + str(group_id)
            if index < groups_id_list.__len__() - 1:
                groups_query_str += ' OR '

        try:
            if start_date != None and end_date != None:
                news_list = News.objects.extra(where={"date_created > " + str(start_date) +" AND date_created < "+ str(end_date) + ' AND' + groups_query_str}).order_by('date_created')
            elif start_date != None:
                news_list = News.objects.extra(where={"date_created > " + str(start_date) + ' AND' + groups_query_str}).order_by('date_created')
            elif end_date != None:
                news_list = News.objects.extra(where={"date_created < " + str(end_date) + ' AND' + groups_query_str}).order_by('date_created')
            else:
                news_list = News.objects.extra(where={groups_query_str}).order_by('date_created')

            if count != None:
                result = news_list.reverse()[:count]
            else:
                result = news_list.reverse()

            return result


        except Exception as ex:
            return []


    def get_news_list_except_groups(self,
                                    groups_id_list:list,
                                    start_date=None,
                                    end_date=None,
                                    count=None):

        groups_query_str = ''

        for (index,group_id) in enumerate(groups_id_list):
            groups_query_str += ' group_id !=' + str(group_id)
            if index < groups_id_list.__len__() - 1:
                groups_query_str += ' AND '

        try:
            if start_date != None and end_date != None:
                news_list = News.objects.extra(where={"date_created > " + str(start_date) +" AND date_created < "+ str(end_date) + ' AND' + groups_query_str}).order_by('date_created')
            elif start_date != None:
                news_list = News.objects.extra(where={"date_created > " + str(start_date) + ' AND' + groups_query_str}).order_by('date_created')
            elif end_date != None:
                news_list = News.objects.extra(where={"date_created < " + str(end_date) + ' AND' + groups_query_str}).order_by('date_created')
            else:
                news_list = News.objects.extra(where={groups_query_str}).order_by('date_created')

            if count != None:
                result = news_list.reverse()[:count]
            else:
                result = news_list.reverse()

            return result


        except Exception as ex:
            return []

    def get_all_attaches(self, news_db):
        return  NewsAttach.objects.filter(news=news_db)


    @transaction.atomic
    def try_save_or_update_news(self, news_dict, group_id):
        try:
            news:list = news_dict['messages']
        except:
            return

        if news.__len__() == 0:
            return

        try:
            group_db = NewsGroup.objects.get(group_id=group_id)
        except NewsGroup.DoesNotExist:
            return

        for new in news:
            try:
                message_id = new['id']
                sender_id = new['sender_id']
                date_created = new['date_created']
                group_id = new['group_id']
                body = new['body']
                date_created_timestamp = datetime.strptime(date_created, '%Y/%m/%d %H:%M:%S %z').timestamp().__round__()

                try:
                    news_db = News.objects.get(news_id=message_id, group=group_db)
                except News.DoesNotExist:
                    news_db = News.objects.create(news_id=message_id,
                                                  sender_id=sender_id,
                                                  group=group_db,
                                                  date_created=date_created_timestamp,
                                                  body=body)

                try:
                    attachments = new['attachments']

                    try:
                        images = attachments['images']

                        for image_dict in images:
                            self.create_or_update_attach(image_dict, news_db)
                    except Exception as ex:
                        pass

                    try:
                        files = attachments['files']

                        for file_dict in files:
                            self.create_or_update_attach(file_dict, news_db)
                    except Exception as ex:
                        pass

                except:
                    pass

                news_db.body = body
                news_db.save()
                group_db.save()

            except Exception as ex:
                print(ex)
                continue

    def create_or_update_attach(self, attach_dict, news_db):

        try:
            id = attach_dict['id']
            url = attach_dict['url']
            type = attach_dict['type']
            content_type = attach_dict['content_type']
            name = attach_dict['name']
            date_created = attach_dict['date_created']
            size = attach_dict['size']
            date_created_timestamp = datetime.strptime(date_created, '%Y/%m/%d %H:%M:%S %z').timestamp().__round__()
        except:
            return

        try:
            large_icon_url = attach_dict['large_icon_url']
            small_icon_url = attach_dict['small_icon_url']
            preview_url = attach_dict['preview_url']
            content_class = attach_dict['content_class']

        except:
            pass

        try:
            attach_db = NewsAttach.objects.get(attach_id=id, news=news_db)
        except NewsAttach.DoesNotExist:
            attach_db = NewsAttach.objects.create(attach_id=id,
                                                  name=name,
                                                  type=type,
                                                  url=url,
                                                  content_type=content_type,
                                                  date_created=date_created_timestamp,
                                                  size=size,
                                                  news=news_db)

        attach_db.large_icon_url = large_icon_url
        attach_db.small_icon_url = small_icon_url
        attach_db.preview_url = preview_url
        attach_db.content_class = content_class
        attach_db.save()
