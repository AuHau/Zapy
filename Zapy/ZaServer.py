"""
   Zapy ZaServer Class Definition

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

class ZaServer(zapyClass):

   #
   # Class Data and Defaults
   #
   _cfg = {
      "accessType": 		None,
      "appProfileId": 		None,
      "cidr": 			None,
      "coipAddress": 		None,
      "description": 		None,
      "endServerId": 		None,
      "hostname": 		None,
      "inlineDeviceGroupId": 	None,
      "onlineSince": 		None,
      "osVersion": 		None,
      "poolTag": 		None,
      "privateIp": 		None,
      "publicIp": 		None,
      "serverGroupId": 		None,
      "serverId": 		None,
      "serverType": 		None,
      "status": 			None,
      "zlinkVersion": 		None,
      "znsClusterId": 		None,
   }

   keyStore = []

   _Debug = True

   #
   # Used to Retrieve the Attribute Name and Id for a Derived Class
   #

   _className = "zaServerName"
   _classId   = "zaServerId"

   def __init__(self, keyStore, *args):
      """
	 Class Initialization
	    keyStore: A passed keyChain Object
	    args[0]:  The Path to the Configration File to be Loaded

         ZaServer Class Attributes:

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
      if len(args) > 0:
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

   def ZaServer_list(self, *args):
      """
         Zapi Call to $ZaServer.list

	 Returns the list of Access Servers that are Active

	 if a hostname is passed in the args list, returns the serverId of a matching server
      """

      info = None

      cmd = {
         "cmd":"$ZaServer.list",
         "args": {
	    "status": "all"
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))
      
      if args is not None:
         serverActive = False

         for i in range(len(info['data'])):
	    if argv[0] == info['data'][i]['hostname']:
	       serverActive = True

	 if serverActive:
	    return info['data'][i]['serverId']

      return info

   #####################################################################################################

   def ZaServer_setZnsCluster(self):
      """
         ToDo: Zapi Call to ZaServer.setZnsCluster
      """

      info = None

      cmd = {
         "cmd":"$ZaServer_setZnsCluster",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################
