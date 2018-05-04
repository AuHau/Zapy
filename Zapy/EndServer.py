"""
   Zapy EndServer Class Definition

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

class EndServer(zapyClass):

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

   _className = "endServerName"
   _classId   = "endServerId"

   def __init__(self, keyStore, *args):
      """
	 Class Initialization
	    keyStore: A passed keyChain Object
	    args[0]:  The Path to the Configration File to be Loaded

         EndServer Class Attributes:

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

   def EndServer_addInlinePolicy(self):
      """
         ToDo: Zapi Call to EndServer.addInlinePolicy
      """

      info = None

      cmd = {
         "cmd":"$EndServer_addInlinePolicy",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def EndServer_deleteInlinePolicy(self):
      """
         ToDo: Zapi Call to EndServer.deleteInlinePolicy
      """

      info = None

      cmd = {
         "cmd":"$EndServer_deleteInlinePolicy",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def EndServer_getDetails(self):
      """
         Zapi Call to EndServer.getDetails
      """
      cmd = {
         "cmd":"$EndServer.getDetails",
	 "args": {
	    "endServerId": self._cfg['endServerId'],
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      # print info

      return info

   #####################################################################################################

   def EndServer_getZlinkHostFileDownloadUrl(self):
      """
         ToDo: Zapi Call to EndServer.getZlinkHostFileDownloadUrl
      """

      info = None

      cmd = {
         "cmd":"$EndServer_getZlinkHostFileDownloadUrl",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def EndServer_getZlinkLogDownloadUrl(self):
      """
         ToDo: Zapi Call to EndServer.getZlinkLogDownloadUrl
      """

      info = None

      cmd = {
         "cmd":"$EndServer_getZlinkLogDownloadUrl",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def EndServer_getDisconnectedInlineDevices(self):
      """
         ToDo: Zapi Call to EndServer.getDisconnectedInlineDevices
      """

      info = None

      cmd = {
         "cmd":"$EndServer_getDisconnectedInlineDevices",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def EndServer_listInlinePolicies(self):
      """
         ToDo: Zapi Call to EndServer.listInlinePolicies
      """

      info = None

      cmd = {
         "cmd":"$EndServer_listInlinePolicies",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def EndServer_queryRegistrationStatus(self):
      """
         ToDo: Zapi Call to EndServer.queryRegistrationStatus
      """

      info = None

      cmd = {
         "cmd":"$EndServer_queryRegistrationStatus",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def EndServer_register(self):
      """
         Zapi Call to EndServer.register

	 This function behaves both like a noraml method but also like syncWithController.

	 That is, it registers an EndServer but also fills itself with the returned data from that operation.
      """
      cmd = {
         "cmd":"$EndServer.register",
	 "args": {
	    "poolTag":       self._cfg['poolTag'],
	    "hostname":      self._cfg['hostname'],
	    "sshId":         self._cfg['sshId'],
	    "sshPassword":   self._cfg['sshPassword'],
	    "sshPort":       self._cfg['sshPort']
	 }
      }
      
      # "sshPrivateKey": self._cfg['sshPrivateKey'],

      info = self.makeZapyRequest(json.dumps(cmd))

      # print info

      jobId = info["data"]["jobId"]

      query = {
         "cmd":"$EndServer.queryRegistrationStatus",
	 "args": {
	    "jobId": jobId
	 }
      }

      notRegistered = True

      #
      # This is a Problem - It blocks until done potentially jamming up the entire Developer's script
      #
      sys.stdout.write('      Registering EndServer for Edge Gateway Duty ')

      while notRegistered:
         #
	 # Don't Abuse the Internet - Check once per second for job completion
	 #
	 sys.stdout.write('.')
	 sys.stdout.flush()

         time.sleep(1)

	 jobStatus = self.makeZapyRequest(json.dumps(query))
	 
	 # print "      ", jobStatus

	 if 'done' in jobStatus['data']['jobStatus']:
	    notRegistered = False

	    self._cfg['endServerId'] = jobStatus['data']['endServerId']

	    endServerDetails = self.EndServer_getDetails()

	    for key, val in endServerDetails['data'].items():
	       # print '   {:<25} = {:<25}'.format(key, val)
	       self._cfg[key] = val

	    print
	    print "      Edge Gateway EndServerId == ", self._cfg['endServerId']

	    return jobStatus['data']['endServerId']

   #####################################################################################################

   def EndServer_unregister(self):
      """
         Zapi Call to EndServer.unregister
      """
      cmd = {
         "cmd":"$EndServer.unregister",
	 "args": {
	    "endServerId": self._cfg['endServerId'],
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def EndServer_upgradeZlink(self):
      """
         ToDo: Zapi Call to EndServer.upgradeZlink
      """

      info = None

      cmd = {
         "cmd":"$EndServer_upgradeZlink",
         "args":self._cfg
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

