"""
   Zapy EndServer Class Definition

   ******
      Note: This file is autogenerated by genClasses. Do not make changes here as they will be overwritten.

      Generated on 19-Jun-2018 13:06:13
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
      "sshId": 			None,
      "sshPassword": 		None,
      "sshPort": 		None,
      "sshPrivateKey": 		None,
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

   def EndServer_getZlinkHostFileDownloadUrl(self, filePath):
      """
         Zapi Call to EndServer.getZlinkHostFileDownloadUrl
      """
      cmd = {
         "cmd":"$EndServer.getZlinkHostFileDownloadUrl",
	 "args": {
	    "endServerId": self._cfg['endServerId'],
	    "filePath": filePath
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      # print info

      if 'Ok' in info['status']:
	 return info['data']['downloadUrl']
      else:
         return None

   #####################################################################################################

   def EndServer_getZlinkLogDownloadUrl(self):
      """
         Zapi Call to EndServer.getZlinkLogDownloadUrl
      """
      cmd = {
         "cmd":"$EndServer.getZlinkLogDownloadUrl",
	 "args": {
	    "endServerId": self._cfg['endServerId']
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      # print info

      if 'Ok' in info['status']:
	 return info['data']['downloadUrl']
      else:
         return None

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
         Zapi Call to EndServer.queryRegistrationStatus

	 Note: This call is automagically handled in EndServer_register() and
	 FabricServer_register() and usually not needed.
      """

      pass

   #####################################################################################################

   def EndServer_register(self, targetPool):
      """
         Zapi Call to EndServer.register

	 This function behaves both like a normal method but also like syncWithController.

	 That is, it registers an EndServer but also fills itself with the returned data from that operation.
      """
      #
      # Determine if this EndServer is Already Registered
      #

      # targetPool.inspect()

      esRegistered = False

      if 'cloudServerPool' in targetPool.getName():
         #
	 # Look for this EndServer in the Target Cloud Server Pool
	 #
	 # print ">>> Looking in CloudServerPool", targetPool._cfg['poolTag'], "for", self._cfg['hostname']
	 esRegistered = targetPool.CloudServerPool_isEndServerRegistered(self)
      else:
         #
	 # Look for this EndServer in the Target Fabric Server Pool
	 #
	 # print ">>> Looking in FabricServerPool", targetPool._cfg['poolTag'], "for", self._cfg['hostname']
	 esRegistered = targetPool.FabricServerPool_isEndServerRegistered(self)

      if esRegistered is not None:
         print '   EndServer is Already Registered'

	 if 'endServerId' in self._cfg:
	    self._cfg['endServerId'] = esRegistered
         
	 if 'toEdgeGateway' in self._cfg:
	    self._cfg['toEdgeGateway']['endServerId'] = esRegistered
	 
	 if 'fromEdgeGateway' in self._cfg:
	    self._cfg['fromEdgeGateway']['endServerId'] = esRegistered
	 
	 details = self.EndServer_getDetails()

	 # print ">>>"
	 # print details['data']
	 # print "<<<"

	 for key in details['data']:
	    # print '   {:<25} = {:<25}'.format(key, details['data'][key])
	    self._cfg[key] = details['data'][key]
      else:
	 #
	 # Make It So
	 #
         # print '   Registering EndServer', self._cfg['hostname'], 'in', self._cfg['poolTag']

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

	 if 'Ok' in info['status']:
	    jobId = info["data"]["jobId"]
	 else:
	    print "Error in Endserver_register: No jobId returned from API call"
	    return None

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
         print '   Registering a EndServer', self._cfg['hostname'], 'in', self._cfg['poolTag'],

	 while notRegistered:
	    #
	    # Don't Abuse the Internet - Check once per second for job completion
	    #
	    sys.stdout.write('.')
	    sys.stdout.flush()

	    time.sleep(2)

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
	       print "      EndServerId == ", self._cfg['endServerId']

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
         Zapi Call to EndServer.upgradeZlink
      """
      cmd = {
         "cmd":"$EndServer.upgradeZlink",
	 "args": {
	    "endServerId": self._cfg['endServerId'],
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      # print info

      return info

   #####################################################################################################

