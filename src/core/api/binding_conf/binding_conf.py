from authorization.api.controllers.auth import AuthController
from authorization.api.services.token_service import TokenService
from social_network.api.controllers.social_network_controller import SocialNetworkController
from social_network.services.yammer_service import YammerService
from core.api.services.service_interacting_1c import ServiceInteracting1C
from authorization.api.services.db_service_auth import DBServiceAuth
from authorization.api.services.db_service_new_person import DBServiceNewPerson
from core.api.services.service_sms_delivery import ServiceSmsDelivery
from authorization.api.services.check_auth_service import CheckAuthService
from social_network.api.parsers.yammer_parser import YammerParser
from social_network.daemons.daemon_latest_news_yammer import DaemonLatestNewsYammer
from social_network.services.db_service import DBServiceSocialNetwork

import inject


def config(binder):

    db_service_auth = DBServiceAuth()
    db_service_new_person = DBServiceNewPerson()
    db_service_social_network = DBServiceSocialNetwork()

    check_auth_service = CheckAuthService(db_service_auth=db_service_auth)
    yammer_service: YammerService = YammerService()
    yammer_parser: YammerParser = YammerParser()

    social_network_controller: SocialNetworkController = SocialNetworkController(check_auth_service=check_auth_service,
                                                                                 db_service=db_service_social_network,
                                                                                 yammer_service=yammer_service)

    serviceInteracting1C = ServiceInteracting1C()

    token_service: TokenService = TokenService()
    service_sms_delivery = ServiceSmsDelivery()


    yammer_worker = DaemonLatestNewsYammer(yammer_service=yammer_service,
                                           db_service=db_service_social_network,
                                           yammer_parser=yammer_parser)


    auth_controller: AuthController = AuthController(token_service=token_service,
                                                     provider_person=serviceInteracting1C,
                                                     db_service_auth=db_service_auth,
                                                     sms_delivery_service=service_sms_delivery,
                                                     db_service_new_person=db_service_new_person)


    binder.bind(AuthController, auth_controller)
    binder.bind(SocialNetworkController, social_network_controller)
    binder.bind(DaemonLatestNewsYammer, yammer_worker)


if not inject.is_configured():
    inject.configure(config=config)
