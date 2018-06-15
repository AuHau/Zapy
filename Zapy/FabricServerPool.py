"""
   Zapy FabricServerPool Class Definition

   ******
      Note: This file is autogenerated by genClasses. Do not make changes here as they will be overwritten.

      Generated on 15-Jun-2018 11:06:30
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

class FabricServerPool(zapyClass):

   #
   # Class Data and Defaults
   #
   _cfg = {
      "poolTag": 		None,
      "description": 		None,
      "fabricServerType": 	"edgeGateway",
      "os": 			"linux",
   }

   keyStore = []

   _Debug = True

   #
   # Used to Retrieve the Attribute Name and Id for a Derived Class
   #

   _className = "fabricServerPoolName"
   _classId   = "fabricServerPoolId"

   def __init__(self, keyStore, *args):
      """
	 Class Initialization
	    keyStore: A passed keyChain Object
	    args[0]:  The Path to the Configration File to be Loaded

         FabricServerPool Class Attributes:

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

   def syncWithController(self, cd):
      """
         If the Fabric Server Pool described by the config file exists, synchronize the data structure to the controller
	 If it doesn't exist, create it.
      """

      self._cfg['cloudDomainId'] = cd.get('cloudDomainId')

      info = cd.CloudDomain_listFabricServerPools()

      # print ">>>", len(info['data'])
      # print ">>>", info

      fpExists = False

      if len(info['data']) > 0:
         for i in range(0, len(info['data'])):
	    # print ">>>", info['data'][i]['poolTag'], "<->", self._cfg['poolTag']
	    if info['data'][i]['poolTag'] == self._cfg['poolTag']:
	       # print "Found and Existing Server Group>", self._cfg['poolTag']
	       for key, val in info['data'][i].items():
		  # print ">>>", key, "==", val
		  self._cfg[key] = val
	       
	       fpExists = True
	       break

      if not fpExists:
	 # print "Adding a New Fabric Server Pool to", cd.get('cloudDomainName')
	 
	 cmd = {
	    'cmd':'$FabricServerPool.create',
	    'args':{
	       'poolTag': self._cfg['poolTag'],
	       'description': self._cfg['description'],
	       'fabricServerType': self._cfg['fabricServerType'],
	       'cloudDomainId': self._cfg['cloudDomainId']
	    }
	 }


	 info = self.makeZapyRequest(json.dumps(cmd))

	 return info

      return fpExists

   #####################################################################################################

   def FabricServerPool_create(self, cd):
      """
	 Create a FabricServerPool

	 Requires CloudDomain Object
      """
	    
      self._cfg['cloudDomainId'] = cd.get('cloudDomainId')

      cmd = {
	 'cmd':'$FabricServerPool.create',
	 'args':{
	    'poolTag': self._cfg['poolTag'],
	    'description': self._cfg['description'],
	    'fabricServerType': self._cfg['fabricServerType'],
	    'cloudDomain': self._cfg['cloudDomain']
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))
      
      return info

   #####################################################################################################

   def FabricServerPool_delete(self):
      """
	 Delete a FabricServerPool
      """

      cmd = {
	 'cmd':'$FabricServerPool.delete',
	 'args':{
	    'poolTag': self._cfg['poolTag']
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))
      
      return info

   #####################################################################################################

   def FabricServerPool_getZlinkDownloadUrl(self):
      """
	 Gets zLink download URL for the Cloud Server Pool
      """

      req = {
	 'cmd':'$FabricServerPool.getZlinkDownloadUrl',
	 'args':{
	    'poolTag': self._cfg['poolTag'],
	    'os': self._cfg['os']
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return(info['data']['downloadUrl'])

   #####################################################################################################

   def FabricServerPool_listEndServers(self, usable):
      """
	 Lists available Fabric Servers in a Server Pool
      """

      req = {
	 'cmd':'$FabricServerPool.listEndServers',
	 'args':{
	    'poolTag': self._cfg['poolTag'],
	    'usable': usable
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      return info

   #####################################################################################################

   def FabricServerPool_isEndServerRegistered(self, endServer):
      """
	 Determine if an EndServer is Registered in a Fabric Server Pool

	 Argument is a Zapy EndServer Object

	 Returns the EndServer's ID if it is Registered in this Pool, None if Not
      """

      cmd = {
	 'cmd':'$FabricServerPool.listEndServers',
	 'args':{
	    'poolTag': self._cfg['poolTag'],
	    'usable': 'all'
	 }
      }

      info = self.makeZapyRequest(json.dumps(cmd))

      endServerId = None

      hostname = endServer.get('hostname')

      # print '--------'
      # print '   Looking for', hostname
      # print '   >>>', info
      # print '--------'

      if len(info['data']) > 0:
	 for i in range(len(info['data'])):
	    if (hostname == info['data'][i]['hostname']) or (hostname == info['data'][i]['publicIp']):
	       endServerId = info['data'][i]['endServerId']

      return endServerId

   #####################################################################################################

