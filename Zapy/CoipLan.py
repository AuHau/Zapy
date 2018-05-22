"""
   Zapy CoipLan Class Definition

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

class CoipLan(zapyClass):

   #
   # Class Data and Defaults
   #
   _cfg = {
      "appProfileId": 	None,
      "coipLanId": 	None,
      "coipLanName": 	None,
      "components": 	None,
      "protocol": 	None,
   }

   keyStore = []

   _Debug = True

   #
   # Used to Retrieve the Attribute Name and Id for a Derived Class
   #

   _className = "coipLanName"
   _classId   = "coipLanId"

   def __init__(self, keyStore, *args):
      """
	 Class Initialization
	    keyStore: A passed keyChain Object
	    args[0]:  The Path to the Configration File to be Loaded

         CoipLan Class Attributes:

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

   def syncWithController(self, ap, cp1, cp2):
      """
         If the CoipLan described by the config file exists, synchronize the data structure to the controller
	 If it doesn't exist, create it.
	 
	 Caveat: There isn't an "AppProfile.listCoipLan" function in the API

	 Thus this route will simply try to create the CoipLan and will return 'CoipLanAlreadyExists'

	 ToDo: InLineDevices
      """

      # print "Adding a New CoipLan to", ap.get('appProfileName')
      
      self._cfg['appProfileId'] = ap.get('appProfileId')

      #
      # ToDo: - When IP Components are Added, this will require some additional logic before we ask for an Id
      #
      # Allowed CoIPLan Connections Component Id Keys::
      #    ServerGroup -> 'serverGroupId'
      #    IPComponent -> <Undefined>Id
      #

      cp1Id = cp1.getId()
      cp2Id = cp2.getId()

      if cp1Id is "serverGroupId":
         cp1Comp = cp1.get('serverGroupId')
      else:
         # cp1Comp = cp1.get('<Undefined>')	# ToDo: Complete Code Here
	 pass

      if cp2Id is "serverGroupId":
         cp2Comp = cp2.get('serverGroupId')
      else:
         # cp2Comp = cp2.get('<Undefined>')	# ToDo: Complete Code Here
	 pass

      cmd = {
         "cmd":"$AppProfile.addCoipLan",
	 "args":{
	    "appProfileId": self._cfg['appProfileId'],
	    "coipLanName": self._cfg['coipLanName'],
	    "components":{
	       "from": cp1Comp,
	       "to":   cp2Comp
	    },
	    "protocol": self._cfg['protocol']
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      # print "--------->"
      # print info
      # print "--------->"

      if 'Ok' in info['status']:
         self._cfg['coipLanId'] = info['data']['coipLanId']

      return info

   #####################################################################################################

