"""
   Zapy ZaUser Class Definition

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

class ZaUser(zapyClass):

   #
   # Class Data and Defaults
   #
   _cfg = {
      "account": 		None,
      "userType": 		None,
      "status": 			None,
      "firstName": 		None,
      "lastName": 		None,
      "email": 			None,
      "expirationDate": 		None,
      "forceChPwdNextLogin": 	None,
      "signonSecurityMac": 	None,
      "signonSecurityHostname": 	None,
   }

   keyStore = []

   _Debug = True

   #
   # Used to Retrieve the Attribute Name and Id for a Derived Class
   #

   _className = "zaUserName"
   _classId   = "zaUserId"

   def __init__(self, keyStore, *args):
      """
	 Class Initialization
	    keyStore: A passed keyChain Object
	    args[0]:  The Path to the Configration File to be Loaded

         ZaUser Class Attributes:

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
         If the ZaUser described by the config file exists, synchronize the data structure to the controller
	 If it doesn't exist, create it.
      """

      info = self.ZaUser_list()

      userExists = False

      if info != None:
	 for i in range(len(info['data'])):
	    if info['data'][i]['account'] == self._cfg['account']:
	       # print "Found >", self._cfg['account']
	       userExists = True

      if not userExists:
         # print "Creating New ZaUser Profile"
	 info = self.ZaUser_create()
	 # print "Created"

	 # print info

	 if 'Ok' in info['status']:
	    for key, val in info['data'].items():
	       self._cfg[key] = val

      return userExists

   #####################################################################################################

   def ZaUser_create(self):
      """
         Zapi Call to $ZaUser.create
      """

      info = None

      cmd = {
         "cmd":"$ZaUser.create",
         "args": {
	    "account": self._cfg["account"],
	    "userType": self._cfg["userType"],
	    "password": self._cfg["password"],
	    "firstName": self._cfg["firstName"],
	    "lastName": self._cfg["lastName"],
	    "email": self._cfg["email"],
	    "forceChpwdNextLogin": False
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ZaUser_delete(self, *args):
      """
         Zapi Call to $ZaUser.delete

	 Optional argument is treated as the account name to delete
      """

      info = None

      cmd = {
         "cmd":"$ZaUser.delete",
         "args": {
	    "account": None
	 }
      }

      if args is not None:
	 cmd['args']['account'] = args[0]
      else:
	 cmd['args']['account'] = self._cfg['account']

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def ZaUser_list(self):
      """
         Zapi Call to $ZaUser.list
      """

      info = None

      cmd = {
         "cmd":"$ZaUser.list",
         "args": {
	    "status": "all"
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################
