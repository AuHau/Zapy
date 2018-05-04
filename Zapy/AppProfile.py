"""
   Zapy AppProfile Class Definition

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

class AppProfile(zapyClass):

   #
   # Class Data and Defaults
   #
   _cfg = {
      "appProfileName":  None,
      "appProfileId":    None,
      "description":     None,
      "coipAssignment":  "dynamic",
      "coipLanPort":     None,
      "enableSSL":       False,
      "cloudProjectId":  None,
      "cfgFileName":     None,
   }

   keyStore = []

   _Debug = True

   #
   # Used to Retrieve the Attribute Name and Id for a Derived Class
   #

   _className = "appProfileName"
   _classId   = "appProfileId"

   def __init__(self, keyStore, *args):
      """
	 Class Initialization
	    keyStore: A passed keyChain Object
	    args[0]:  The Path to the Configration File to be Loaded

         AppProfile Class Attributes:

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

   def syncWithController(self):
      """
         If the App Profile described by the config file exists, synchronize the data structure to the controller
	 If it doesn't exist, create it.
      """

      info = self.listAppProfileByName(self._cfg['appProfileName'])

      if info != None:
	 # print "Found >", self._cfg['appProfileName']
	 for key, val in info.items():
	    self._cfg[key] = val
      else:
         # print "Creating New App Profile"
	 info = self.AppProfile_create()

	 self._cfg['appProfileId'] = info['data']['appProfileId']

   #####################################################################################################

   def AppProfile_activate(self):
      """
         Zapi Call to AppProfile.activate
      """

      cmd = {
         "cmd":"$AppProfile.create",
	 "args": {
	    "appProfileId": self._cfg['appProfileId']
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def AppProfile_addCoipLan(self):
      """
         Zapi Call to AppProfile.addCoipLan
      """

      cmd = {
         "cmd":"$AppProfile.addCoipLan",
	 "args": {
	    'appProfileId': self._cfg['appProfileId'],
	    'coipLanName': self._cfg['lName'],
	    'components':{
	       'from': self._cfg['frId,'],
	       'to': self._cfg['toId'],
	    },
	    "protocol": {
	       self._cfg['protocol']
	    }
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      print info

      return info

   #####################################################################################################

   def AppProfile_addCoipWanTypeOne(self):
      """
         Zapi Call to AppProfile.addCoipWanTypeOne
      """
      cmd = {
         "cmd":"$AppProfile.addCoipWanTypeOne",
	 "args": self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def AppProfile_addCoipWanTypeThree(self):
      """
         ToDo: Zapi Call to AppProfile.addCoipWanTypeThree
      """

      info = None

      cmd = {
         "cmd":"$AppProfile_addCoipWanTypeThree",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def AppProfile_addCoipWanTypeTwo(self):
      """
         ToDo: Zapi Call to AppProfile.addCoipWanTypeTwo
      """

      info = None

      cmd = {
         "cmd":"$AppProfile_addCoipWanTypeTwo",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def AppProfile_addInlineDeviceGroup(self):
      """
         ToDo: Zapi Call to AppProfile.addInlineDeviceGroup
      """

      info = None

      cmd = {
         "cmd":"$AppProfile_addInlineDeviceGroup",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def AppProfile_addServerGroup(self, sg):
      """
	 Zapi Call to add a Server Group to an Application Profile
      """

      cmd = {
	 'cmd':'$AppProfile.addServerGroup',
	 'args':{
	    'appProfileId': self._cfg['appProfileId'],
	    'poolTag': sg.get('poolTag'),
	    'serverGroupName': sg.get('serverGroupName'),
	    'coipSubnet': sg.get('coipSubnet')
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return(info)

   #####################################################################################################

   def AppProfile_create(self):
      """
         Zapi Call to AppProfile.create
      """
      cmd = {
         "cmd":"$AppProfile.create",
	 "args": self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def AppProfile_deactivate(self):
      """
         ToDo: Zapi Call to AppProfile.deactivate
      """

      info = None

      cmd = {
         "cmd":"$AppProfile_deactivate",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def AppProfile_delete(self):
      """
         Zapi Call to AppProfile.delete
      """

      info = None

      if self._cfg['appProfileId'] != None:
	 cmd = {
	    "cmd":"$AppProfile.delete",
	    "args": { "appProfileId": self._cfg['appProfileId'] }
	 }

	 info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def AppProfile_listCoipWans(self):
      """
         Zapi Call to AppProfile.listCoipWans
      """

      info = None

      cmd = {
         "cmd":"$AppProfile.listCoipWans",
         "args":{
	    "appProfileId": self._cfg["appProfileId"]
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def AppProfile_listInlineDeviceGroups(self):
      """
         ToDo: Zapi Call to AppProfile.listInlineDeviceGroups
      """

      info = None

      cmd = {
         "cmd":"$AppProfile_listInlineDeviceGroups",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def AppProfile_listServerGroups(self):
      """
         Zapi Call to AppProfile.listServerGroups
      """

      info = None

      cmd = {
         "cmd":"$AppProfile.listServerGroups",
         "args":{
	    "appProfileId": self._cfg["appProfileId"]
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def AppProfile_listServerGroupByName(self, name):
      """
         Zapi Call to AppProfile.listServerGroups

	 Returns the Named Server Group if Found, Otherwise Returns None
      """

      cmd = {
         "cmd":"$AppProfile.listServerGroups",
         "args":{
	    "appProfileId": self._cfg["appProfileId"]
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      for i in range(len(info['data'])):
         if name == info['data'][i]['serverGroupName']:
	    return info['data'][i]

      return None

   #####################################################################################################
