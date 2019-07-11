

class YammerParser:

    __all__ = ['convert_groups',
               'convert_messages']

    def convert_groups(self, yammer_groups):
        groups = []

        for group in yammer_groups:
            try:
                group_id = group['id']
                name:str = group['full_name']
            except:
                continue

            group_dict = {'id': group_id, 'name': name}

            try:
                group_dict['description'] = group['description']
            except:
                pass

            groups.append(group_dict)


        return {'groups':groups}

    def convert_messages(self, yammer_messages):
        convert_messages = []

        try:
            messages = yammer_messages['messages']
        except KeyError:
            return None

        for message in messages:

            convert_message = self.try_parse_message(message)
            if convert_message != None:

                attachments_images_list = []
                attachments_files_list = []

                try:
                    attachments_dict = message['attachments']

                    for attach_dict in attachments_dict:
                        attach = self.try_parse_attach(attach_dict)

                        if attach != None:
                            if attach['type'] == 'image':
                                attachments_images_list.append(attach)
                            elif attach['type'] == 'file':
                                attachments_files_list.append(attach)

                except:
                    attachments = None

                if attachments_files_list.__len__() > 0:
                    convert_message['attachments'] = {'files':attachments_files_list}

                if attachments_images_list.__len__() > 0:
                    convert_message['attachments'] = {'images': attachments_images_list}

                convert_messages.append(convert_message)

        return {'messages':convert_messages}

    def try_parse_message(self, message):

        try:
            message_id = message['id']
            sender_id = message['sender_id']
            date_created = message['created_at']
            group_id = message['group_id']
            system_message = message['system_message']
            body:str = message['body']['parsed']
        except:
            return None

        if body.__len__() < 100:
            return None

        if system_message == True:
            return None

        convert_message = {'id': message_id,
                           'sender_id': sender_id,
                           'date_created': date_created,
                           'group_id': group_id,
                           'body': body}

        return convert_message


    def try_parse_attach(self, attach):

        try:
            attach_id = attach['id']
            attach_download_url = attach['download_url']
            attach_content_type = attach['content_type']
            attach_type = attach['type']
            attach_name = attach['name']
            attach_date_created = attach['created_at']
            attach_size = attach['size']
        except:
            return None

        try:
            attach_small_icon_url = attach['small_icon_url']
            attach_large_icon_url = attach['large_icon_url']
            attach_content_class = attach['content_class']
            attach_preview_url = attach['preview_url']
        except:
            pass

        attach_dict = {'id': attach_id,
                       'url': attach_download_url,
                       'type': attach_type,
                       'content_type':attach_content_type,
                       'name': attach_name,
                       'date_created': attach_date_created,
                       'size': attach_size}

        if attach_large_icon_url != None:
            attach_dict['large_icon_url'] = attach_large_icon_url

        if attach_small_icon_url != None:
            attach_dict['small_icon_url'] = attach_small_icon_url

        if attach_preview_url != None:
            attach_dict['preview_url'] = attach_preview_url

        if attach_content_class != None:
            attach_dict['content_class'] = attach_content_class

        return attach_dict