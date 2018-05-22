"""
   Zapy ServerGroup Class Definition

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

class ServerGroup(zapyClass):

   #
   # Class Data and Defaults
   #
   _cfg = {
      "serverGroupId": 		None,
      "serverGroupName": 	None,
      "poolTag": 		None,
      "description": 		None,
      "siloMode": 		None,
      "coipSubnet": 		None,
      "failClose": 		None,
      "cloudDomainId": 		None,
   }

   keyStore = []

   _Debug = True

   #
   # Used to Retrieve the Attribute Name and Id for a Derived Class
   #

   _className = "serverGroupName"
   _classId   = "serverGroupId"

   def __init__(self, keyStore, *args):
      """
	 Class Initialization
	    keyStore: A passed keyChain Object
	    args[0]:  The Path to the Configration File to be Loaded

         ServerGroup Class Attributes:

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

   def syncWithController(self, ap, cd, sg):
      """
         If the Server Group described by the config file exists, synchronize the data structure to the controller
	 If it doesn't exist, create it.
      """

      info = ap.AppProfile_listServerGroups()

      # print ">>>", len(info['data'])
      # print ">>>", info

      self._cfg['appProfileId'] = ap.get('appProfileId')
      self._cfg['cloudDomainId'] = cd.get('cloudDomainId')

      sgExists = False

      if len(info['data']) > 0:
         for i in range(0, len(info['data'])):
	    # print ">>>", info['data'][i]['serverGroupName'], "<->", self._cfg['serverGroupName']
	    if info['data'][i]['serverGroupName'] == self._cfg['serverGroupName']:
	       # print "Found and Existing Server Group>", self._cfg['serverGroupName']
	       for key, val in info['data'][i].items():
		  # print ">>>", key, "==", val
		  self._cfg[key] = val
	       
	       sgExists = True
	       break

      if not sgExists:
	 # print "Adding a New Server Group to", ap.get('appProfileName')

	 info = ap.AppProfile_addServerGroup(self)

	 # print ">>>"
	 # print info
	 # print self._cfg['serverGroupName']
	 # print "<<<"

	 self._cfg['serverGroupId'] = info['data']['serverGroupId']

      return sgExists

   #####################################################################################################

   def ServerGroup_addInlinePolicy(self):
      """
         ToDo: Zapi Call to ServerGroup.addInlinePolicy
      """

      info = None

      cmd = {
         "cmd":"$ServerGroup_addInlinePolicy",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ServerGroup_autoAddEndServers(self, esCount):
      """
         Zapi Call to ServerGroup.autoAddEndServers

	 Adds the 'esCount' of endServerIds to this ServerGroup
      """

      cmd = {
         "cmd": "$ServerGroup.autoAddEndServers",
	 "args": {
	    "serverGroupId": self._cfg['serverGroupId'],
	    "endServers": esCount
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))


   #####################################################################################################

   def ServerGroup_configureFailClose(self):
      """
         Zapi Call to ServerGroup.configureFailClose
      """

      cmd = {
         "cmd": "$ServerGroup.configureFailClose",
	 "args": {
	    "serverGroupId": self._cfg['serverGroupId'],
	    "failClose":     self._cfg['failClose']
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))


   #####################################################################################################

   def ServerGroup_deleteInlinePolicy(self):
      """
         ToDo: Zapi Call to ServerGroup.deleteInlinePolicy
      """

      info = None

      cmd = {
         "cmd":"$ServerGroup_deleteInlinePolicy",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ServerGroup_manualAddEndServers(self, esList):
      """
         Zapi Call to ServerGroup.manualAddEndServers

	 Adds the 'esList' of endServerIds to this ServerGroup

	    sg.ServerGroup_manualAddEndServers([<sgId1>, <sgId2>, ...])
      """

      cmd = {
         "cmd": "$ServerGroup.manualAddEndServers",
	 "args": {
	    "serverGroupId": self._cfg['serverGroupId'],
	    "endServers":    esList
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))


   #####################################################################################################

   def ServerGroup_listEndServers(self):
      """
         Zapi Call to $ServerGroup.listEndServers
      """

      cmd = {
         "cmd":"$ServerGroup.listEndServers",
         "args": {
	    "serverGroupId": self._cfg["serverGroupId"]
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ServerGroup_listInlinePolicies(self):
      """
         ToDo: Zapi Call to ServerGroup.listInlinePolicies
      """

      info = None

      cmd = {
         "cmd":"$ServerGroup_listInlinePolicies",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ServerGroup_removeEndServers(self, esList):
      """
         Zapi Call to ServerGroup.removeEndServers

	 Removes the 'esList' of endServerIds from this ServerGroup

	    sg.ServerGroup_removeEndServers([<sgId1>, <sgId2>, ...])
      """

      cmd = {
         "cmd": "$ServerGroup.removeEndServers",
	 "args": {
	    "serverGroupId": self._cfg['serverGroupId'],
	    "endServers":    esList
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))


   #####################################################################################################

