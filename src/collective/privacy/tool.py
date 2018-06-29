# -*- coding: utf-8 -*-
import uuid
import hmac

from App.class_init import InitializeClass
from BTrees.OIBTree import OIBTree
from Products.CMFCore.utils import UniqueObject
from Products.CMFPlone.PloneBaseTool import PloneBaseTool
from OFS.SimpleItem import SimpleItem
from OFS.ObjectManager import IFAwareObjectManager
from OFS.OrderedFolder import OrderedFolder
from zope.interface import implementer
from zope.component import getUtility

from collective.privacy.interfaces import IProcessingReason

EMAIL_NAMESPACE = uuid.UUID('a838b36d-d1d5-477e-8471-c1e2079417cf')
MEMBER_ID_NAMESPACE = uuid.UUID('9d01c079-a268-4e43-81f7-0eecd4c45316')
IP_NAMESPACE = uuid.UUID('45865cac-1e4f-46d3-8e3e-1c277db76f3e')


class ProcessingReason(SimpleItem):

    def __init__(self, *args, **kwargs):
        super(ProcessingReason, self).__init__(*args, **kwargs)
        self.consented = OIBTree()
        self.objected = OIBTree()

InitializeClass(ProcessingReason)


class PrivacyTool(UniqueObject, IFAwareObjectManager, OrderedFolder, PloneBaseTool):
    """ Manage through-the-web signup policies.
    """

    meta_type = 'Plone Privacy Tool'
    _product_interfaces = (IProcessingReason,)
    #security = ClassSecurityInfo()
    toolicon = 'skins/plone_images/pencil_icon.png'
    id = 'portal_privacy'
    plone_tool = 1

    def _setId(self, *args, **kwargs):
        return

    def __init__(self, *args, **kwargs):
        super(PrivacyTool, self).__init__(self, *args, **kwargs)

    def getProcessingReason(self, processing_reason_id):
        return getUtility(IProcessingReason, name=processing_reason_id)

    def processingIsAllowed(self, processing_reason_id, user=None):
        processing_reason = self.getProcessingReason(processing_reason_id)
        return processing_reason.isProcessingAllowed(self.REQUEST, user)

    def objectToProcessing(self, processing_reason_id, user=None):
        processing_reason = self.getProcessingReason(processing_reason_id)
        processing_reason.objectToProcessing(request=self.REQUEST, user=user)

    def consentToProcessing(self, processing_reason_id, user=None):
        processing_reason = self.getProcessingReason(processing_reason_id)
        processing_reason.consentToProcessing(request=self.REQUEST, user=user)

    def requestPorting(self, identifier, topic=None):
        raise NotImplementedError

    def requestDeletion(self, identifier, topic=None):
        raise NotImplementedError


InitializeClass(PrivacyTool)