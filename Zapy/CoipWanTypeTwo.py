"""
   Zapy CoipWanTypeTwo Class Definition

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

class CoipWanTypeTwo(zapyClass):

   #
   # Class Data and Defaults
   #
   _cfg = {
      "appProfileId": 	None,
      "coipWanId": 	None,
      "coipWanName": 	None,
      "coipWanType": 	'typeTwo',
      "components": 	None,
      "direction": 	None,
      "znsClusterId": 	None,
   }

   keyStore = []

   _Debug = True

   #
   # Used to Retrieve the Attribute Name and Id for a Derived Class
   #

   _className = "coipWanTypeTwoName"
   _classId   = "coipWanTypeTwoId"

   def __init__(self, keyStore, *args):
      """
	 Class Initialization
	    keyStore: A passed keyChain Object
	    args[0]:  The Path to the Configration File to be Loaded

         CoipWanTypeTwo Class Attributes:

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

   def syncWithController(self, ap, cp1, cp2):
      """
         It occurs to me that making the arguments to this routine be "AppProfile, From, To" might simplify this
	 thing a lot...

         If the CoipWanTypeTwo described by the config file exists, synchronize the data structure to the controller
	 If it doesn't exist, create it.

	 ToDo: Doesn't Handle multiple ranges for From / To components
      """
      
      self._cfg['appProfileId'] = ap.get('appProfileId')

      #
      # Check to see if this CoipWan already exists
      #
      cwExists = False

      info = ap.AppProfile_listCoipWans()

      if len(info['data']) > 0:
         for i in range(0, len(info['data'])):
	    # print ">>>", info['data'][i]['coipWanName'], "<->", self._cfg['coipWanName']
	    if info['data'][i]['coipWanName'] == self._cfg['coipWanName']:
	       #
	       # CoipWan Exists
	       #
	       print "Found and Existing CoIP Wan>", self._cfg['coipWanName']

	       for key, val in info['data'][i].items():
		  # print ">>>", key, "==", val
		  self._cfg[key] = val
	       
	       cwExists = True
	       break

      if not cwExists:
	 #
	 # Prepare Common API Command Bits
	 #

	 cmd = {
	    'cmd':'$AppProfile.addCoipWanTypeTwo',
	    'args':{
	       'appProfileId': self._cfg['appProfileId'],
	       'coipWanName': self._cfg['coipWanName'],
	       'direction': self._cfg['direction'],
	    }
	 }
	 
	 # print "Adding a New '{}' CoipWan to {}".format(self._cfg['coipWanType'], ap.get('appProfileName'))
	 
	 #
	 # Determine Configuration
	 #
	 # cp1Id cp2Id    Type
	 #   SG    EG     :typeTwo		Config is: SG -> EG
	 #   EG    SG     :typeTwo		Config is: EG -> SG
	 #

	 cp1Id = cp1.getId()
	 cp2Id = cp2.getId()

	 if cp1Id is "serverGroupId": 
	    #
	    # From is ServerGroup, To is EdgeGateway
	    #
	    cmps = {
	       'compId': cp1.get('serverGroupId'),
	       'edgeGateway': cp2.get('toEdgeGateway')
	    }

	    cmps['edgeGateway']['endServerId'] = cp2.get('endServerId')

	 else:
	    #
	    # From is EdgeGateway, To is ServerGroup
	    #
	    cmps = {
	       'edgeGateway': cp1.get('fromEdgeGateway'),
	       'compId': cp2.get('serverGroupId')
	    }
	    
	    cmps['edgeGateway']['endServerId'] = cp1.get('endServerId')

	 #
	 # Make it so
	 #
	 cmd['args'].update(cmps)

	 info = self.makeZapyRequest(json.dumps(cmd))

	 if info['status'] == 'Ok':
	    self._cfg['coipWanId'] = info['data']['coipWanId']

	 return info

      return cwExists

   #####################################################################################################

   def CoipWan_delete(self):
      """
         Zapi Call to CoipWan.delete
      """

      info = None

      if self._cfg['coipWanId'] != None:
	 cmd = {
	    "cmd":"$CoipWan.delete",
	    "args": { "coipWanId": self._cfg['coipWanId'] }
	 }

	 info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################
