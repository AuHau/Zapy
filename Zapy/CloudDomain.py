"""
   Zapy CloudDomain Class Definition

   ******
      Note: This file is autogenerated by genClasses. Do not make changes here as they will be overwritten.

      Generated on 29-Jul-2018 06:07:02
   ******

   Copyright (C) 2012-2018 Zentera Systems, Inc. - All Rights Reserved

   This demonstration software is provided by the copyright holders and contributors "as is" and 
   any express or implied warranties, including, but not limited to, the implied warranties of 
   merchantability and fitness for a particular purpose are disclaimed. In no event shall the 
   copyright holder or contributors be liable for any direct, indirect, incidental, special, 
   exemplary, or consequential damages (Including, but not limited to, procurement of substitute 
   goods or services; Loss of use, data, or profits; or business interruption) however caused and 
   on any theory of liability, whether in contract, strict liability, or tort (including negligence 
   or otherwise) arising in any way out of the use of this software, even if advised of the 
   possibility of such damage.

   This software is for demonstration purposes only and is not supported by Zentera Systems, Inc.

"""

import json
from zapyClass import zapyClass
import keyChain
import time
import sys

class CloudDomain(zapyClass):

   #
   # Class Data and Defaults
   #
   _cfg = {
      "cloudDomainId":    None,
      "cloudDomainName":  None,
      "description":      None,
      "monitorInterval":  0,
      "cloudConnector":   None,
   }

   keyStore = []

   _Debug = True

   #
   # Used to Retrieve the Attribute Name and Id for a Derived Class
   #

   _className = "cloudDomainName"
   _classId   = "cloudDomainId"

   def __init__(self, keyStore, *args):
      """
	 Class Initialization
	    keyStore: A passed keyChain Object
	    args[0]:  The Path to the Configration File to be Loaded

         CloudDomain Class Attributes:

	 Class Configuration Attributes
	    cfgFileName		: File Name of the Loaded Configuration
      """

      #
      # Load the API Keys
      #
      self.keyStore = keyStore
      
      #
      # Load a Config File if Passed
      #
      if args[0] is None:
         pass
      else:
	 # print "   Loading Configuration File:", args[0]
         self.loadCfg(args[0])

      # for key, value in kwargs.items():
	 # print("The value of {} is {}".format(key, value))

	 # self._cfg[key] = value

   def getName(self):
      return self._className

   def getId(self):
      return self._classId

   ####################################################################################################
   #
   # Class Member Functions
   #
   ####################################################################################################

   def syncWithController(self):
      """
         If the Cloud Domain described by the config file exists, synchronize the data structure to the controller
	 If it doesn't exist, create it.
      """

      info = self.listCloudDomainByName(self._cfg['cloudDomainName'])

      if info != None:
	 # print "Found >", self._cfg['cloudDomainName']
	 for key, val in info.items():
	    self._cfg[key] = val
      else:
         # print "Creating New Cloud Domain"
	 info = self.CloudDomain_create()

	 self._cfg['cloudDomainId'] = info['data']['cloudDomainId']

   #####################################################################################################

   def CloudDomain_create(self):
      """
         Zapi Call to CloudDomain.create
      """
      cmd = {
         "cmd":"$CloudDomain.create",
	 "args": {
	    "cloudDomainName": self._cfg["cloudDomainName"],
	    "description": self._cfg["description"],
	    "monitorInterval": self._cfg["monitorInterval"]
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def CloudDomain_delete(self):
      """
         Zapi Call to CloudDomain.delete
      """
      cmd = {
         "cmd":"$CloudDomain.delete",
	 "args": {
	    "cloudDomainId": self._cfg["cloudDomainId"]
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      if 'CloudDomainInUse' in info['status']:
         print '   WARN: Cloud Domain', self._cfg['cloudDomainName'], 'is in use. Not deleted'

   #####################################################################################################

   def CloudDomain_listCloudServerPools(self):
      """
         Zapi Call to CloudDomain.listCloudServerPools
      """
      cmd = {
         "cmd":"$CloudDomain.listCloudServerPools",
	 "args": {
	    "cloudDomainId": self._cfg["cloudDomainId"]
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def CloudDomain_listFabricServerPools(self):
      """
         Zapi Call to CloudDomain.listFabricServerPools
      """
      cmd = {
         'cmd':'$CloudDomain.listFabricServerPools',
	 'args': {
	    'cloudDomainId': self._cfg['cloudDomainId'],
	    'fabricServerType': 'inlineStreamingDevice'
	 }
      }
      #self._cfg['fabricServerType']

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

