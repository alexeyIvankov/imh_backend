

class ParserUserInfo:

    def __init__(self, json):
        self.json = json


    def try_get_value(self, dict, key):

        if dict is None:
            return None

        try:
            value = dict[key]
        except KeyError:
            value = None

        return value

    def is_authorization(self):
        return self.try_get_value(self.json, 'AuthorizationSuccess')

    def get_name_person(self):
        info = self.try_get_value(self.json, 'Info')
        return  self.try_get_value(info, 'ФИО')

    def get_person_position_title(self):
        info = self.try_get_value(self.json, 'Info')
        positions = self.try_get_value(info, 'Должности')
        return  positions['JobTitle']

    def get_person_position_sub_title(self):
        info = self.try_get_value(self.json, 'Info')
        positions = self.try_get_value(info, 'Должности')
        return positions['OrganizationUnit']

    def get_person_position_date_receipt(self):
        info = self.try_get_value(self.json, 'Info')
        positions = self.try_get_value(info, 'Должности')
        return positions['DateOfReceipt']

    def get_organisation_name(self):
        info = self.try_get_value(self.json, 'Info')
        positions = self.try_get_value(info, 'Должности')
        return positions['Organization']

    def get_organization_comment(self):
        return self.try_get_value(self.json, 'AuthorizationComment')


