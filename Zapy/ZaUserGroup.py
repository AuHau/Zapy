"""
   Zapy ZaUserGroup Class Definition

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

class ZaUserGroup(zapyClass):

   #
   # Class Data and Defaults
   #
   _cfg = {
      "groupName": 	None,
      "description": 	None,
      "clientCheck": 	None,
      "whiteListedIps": 	None,
   }

   keyStore = []

   _Debug = True

   #
   # Used to Retrieve the Attribute Name and Id for a Derived Class
   #

   _className = "zaUserGroupName"
   _classId   = "zaUserGroupId"

   def __init__(self, keyStore, *args):
      """
	 Class Initialization
	    keyStore: A passed keyChain Object
	    args[0]:  The Path to the Configration File to be Loaded

         ZaUserGroup Class Attributes:

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
         If the ZaUserGroup described by the config file exists, synchronize the data structure to the controller
	 If it doesn't exist, create it.
      """

      info = self.ZaUserGroup_list()

      userGroupExists = False

      if info != None:
	 for i in range(len(info['data'])):
	    if info['data'][i]['groupName'] == self._cfg['groupName']:
	       # print "Found >", self._cfg['groupName']
	       userGroupExists = True

      if not userGroupExists:
         # print "Creating New ZaUserGroup"
	 info = self.ZaUserGroup_create()

	 for key, val in info['data'].items():
	    self._cfg[key] = val

   #####################################################################################################

   def ZaUserGroup_addAcl(self, hostname):
      """
         Zapi Call to $ZaUserGroup.addAcl

	 Hostname argument is used to retrieve the serverId of that machine

      """

      esId = None
      esId = 'cf30544604424671b8b3f83ad2b4898c'

      if True == False:
	 #
	 # Find the serverId of the hostname
	 #
	 cmd = {
	    "cmd":"$ZaServer.list",
	    "args": {
	       "status": "active"
	    }
	 }

	 # print "***********", cmd

	 # info = self.makeZapyRequest(json.dumps(cmd))

	 serverActive = False

	 for i in range(len(info['data'])):
	    if hostname == info['data'][i]['hostname']:
	       serverActive = True

	    if serverActive:
	       esId = info['data'][i]['serverId']
	    else:
	       print "No Server named", hostname, "found"
	       return None

      info = None
	 
      cmd = {
	 "cmd":"$ZaUserGroup.addAcl",
	 "args": {
	    "groupName":   self._cfg["groupName"],
	    "serverId":    'cf30544604424671b8b3f83ad2b4898c',
	    "connectView": True
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ZaUserGroup_addUser(self, newUser):
      """
         Zapi Call to $ZaUserGroup.addUser
      """

      info = None
      
      cmd = {
         "cmd":"$ZaUserGroup.addUser",
         "args": {
	    "groupName": self._cfg["groupName"]
	 }
      }

      cmd['args'].update(newUser._cfg)

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ZaUserGroup_create(self):
      """
         Zapi Call to $ZaUserGroup.create
      """

      info = None

      cmd = {
         "cmd":"$ZaUserGroup.create",
         "args": {
	    "groupName":      self._cfg["groupName"],
	    "description":    self._cfg["description"],
	    "clientCheck":    self._cfg["clientCheck"],
	    "whiteListedIps": self._cfg["whiteListedIps"]
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ZaUserGroup_delete(self):
      """
         Zapi Call to $ZaUserGroup.delete
      """

      info = None

      cmd = {
         "cmd":"$ZaUserGroup.delete",
         "args": {
	    "groupName": self._cfg["groupName"]
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ZaUserGroup_list(self):
      """
         Zapi Call to $ZaUserGroup.list
      """

      info = None

      cmd = {
         "cmd":"$ZaUserGroup.list",
         "args": None
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ZaUserGroup_listAcl(self):
      """
         Zapi Call to $ZaUserGroup.listAcl
      """

      info = None

      cmd = {
         "cmd":"$ZaUserGroup.listAcl",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ZaUserGroup_listUsers(self):
      """
         Zapi Call to $ZaUserGroup.listUsers
      """

      info = None

      cmd = {
         "cmd":"$ZaUserGroup.listUsers",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ZaUserGroup_removeUser(self, account):
      """
         Zapi Call to $ZaUserGroup.removeUser
      """

      info = None

      cmd = {
         "cmd":"$ZaUserGroup.removeUser",
         "args": {
	    "groupName": self._cfg["groupName"],
	    "account": account
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################
