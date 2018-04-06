"""
   Zapy Base Object Class Definition

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

   This software is for demonstrations purposes only and is not supported by Zentera Systems, Inc.

"""

import sys
import os
import hashlib
import hmac
import base64
import json
import requests
import httplib
import urllib3
import time
import re

class zapyClass(object):

   #
   # Class Data and Defaults
   #
   _cfg = {
   }

   _ZapyDEBUG = True
   _ZapyDEBUG = False

   _ZapyKey = None
   _ZapyUrl = None

   #
   # Disable InsecureRequestWarning
   #
   # Note: This requires more work to add Cert Verification to the System
   # See:  https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
   #
   urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

   def __init__(self):
      """
	 Class Configuration Attributes
	    cfgFileName		: File Name of the Loaded Configuration
      """

      print "zapyClass.__init__()"

   ####################################################################################################
   #
   # Class Member Functions
   #
   ####################################################################################################

   def __str__(self):
      return 'zapyClass'

   ####################################################################################################

   def loadCfg(self, fileName):
      """
	 Load Configuration from a JSON File
      """
      with open(fileName, 'r') as fin:
         self._cfg = json.load(fin)
	 self._cfg["cfgFileName"] = fileName

   ####################################################################################################

   def saveCfg(self, fileName):
      """
      Save Configuration to a JSON File
      """
      with open(fileName, 'w') as fot:
	 json.dump(self._cfg, fot)

   ####################################################################################################

   def set(self, attr, val):
      """
	 Set a Class Attribute
      """
      self._cfg[attr] = val

   ####################################################################################################

   def get(self, attr):
      """
	 Get a Class Attribute
      """
      return self._cfg[attr]

   ####################################################################################################

   def inspect(self):
      """
	 Inspect the Contents of an Instance
      """

      print 
      
      keys = self._cfg.keys()
      keys.sort()
      for key in keys:
	 print '   {:<25} = {:<25}'.format(key, self._cfg[key])
      
      print

   ####################################################################################################
   #
   # API Keys and API Url
   #
   ####################################################################################################

   def loadKeys(self, keyFileName, apiUrl):
      if self._ZapyDEBUG:
	 print 'keyFile  == ', keyFileName
      with open(keyFileName, 'r') as f:
	 keyStore = json.load(f)
	 if self._ZapyDEBUG:
	    # print 'keyStore == ', keyStore
	    print 'keyStore loaded'
	 global _ZENTERA_API_SKEY
	 global _ZENTERA_KID_SKEY
	 self._ZENTERA_API_SKEY = keyStore['apiSecretKeyBase64']
	 self._ZENTERA_KID_SKEY = keyStore['apiKeyId']

	 # print "_ZENTERA_API_SKEY = ", _ZENTERA_API_SKEY
	 # print "_ZENTERA_KID_SKEY = ", _ZENTERA_KID_SKEY

      self._ZapyUrl = apiUrl

   ####################################################################################################
   #
   # Routines to Hide the Complexity of the API Requests
   #
   ####################################################################################################

   def makeZapyRequest(self, command):
      "Craft a zCenter API Request"

      secret  = base64.standard_b64decode(self._ZENTERA_API_SKEY)

      #
      # Calculate the HMAC signature = Base64( HMAC-SHA1( SecretKey, UTF8-Encoding-Of( RequestPayload ) ) )
      #
      hmacKey = hmac.new(secret, command.encode('UTF-8'), hashlib.sha1)
      hmacKey = hmacKey.digest().encode('base64').strip()

      #
      # Assemble the API Request
      #
      request = '{"request":' + command + ',"kid":"' + self._ZENTERA_KID_SKEY + '","hmac":"' + hmacKey + '"}'

      if self._ZapyDEBUG:
	 print
	 print ">>> Zapy Request  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
	 print request
	 print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
	 print

      #
      # Make the API Request and Return the JSON Respons
      #
      headers = {'content-type': 'application/json'}
      Post = requests.post(self._ZapyUrl, verify=False, data=request, headers=headers)
      info = json.loads(Post.content)

      if self._ZapyDEBUG:
	 print
	 print "<<< Zapy Response <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
	 print info
	 print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
	 print

      #
      # Error Checking
      #
      # checkZapyStatus(info)

      return(info)
   
   ####################################################################################################
   #
   # Customer Functions - Note: These are in the base class because of their near universal use
   #
   ####################################################################################################

   def getControllerCertificate(self):
      """
         Returns the Controller Appliance's Public Cert
      """
      cmd = {"cmd":"$Customer.getControllerCertificate", "args": None}
      info = self.makeZapyRequest(json.dumps(cmd))
      return info['data']
   
   ####################################################################################################

   def getControllerLogDownloadUrl(self):
      """
         Returns a URL for the Controller Appliance's Log File
      """
      cmd = {"cmd":"$Customer.getControllerLogDownloadUrl", "args": None}
      info = self.makeZapyRequest(json.dumps(cmd))
      return info['data']

   ####################################################################################################

   def getControllerSoftwareVersions(self):
      """
         Returns a Controller Appliance's Version Numbers
      """
      cmd = {"cmd":"$Customer.getControllerSoftwareVersions", "args": None}
      info = self.makeZapyRequest(json.dumps(cmd))
      return info['data']

   ####################################################################################################

   def listAppProfiles(self):
      """
         Returns a JSON List of App Profiles
      """
      cmd = {"cmd":"$Customer.listAppProfiles", "args":{"active":"yes"}}
      info = self.makeZapyRequest(json.dumps(cmd))
      return info

   ####################################################################################################

   def listAppProfileByName(self, name):
      """
         Returns JSON Information of a App Profile by Name
      """
      cmd = {"cmd":"$Customer.listAppProfiles", "args":{"active":"yes"}}

      info = self.makeZapyRequest(json.dumps(cmd))

      for i in range(len(info['data'])):
	 if name == info['data'][i]['appProfileName']:
	    return info['data'][i]

      return None
   
   ####################################################################################################

   def listCloudDomains(self):
      """
         Returns a JSON List of Cloud Domains
      """
      cmd = {"cmd":"$Customer.listCloudDomains", "args": None}
      info = self.makeZapyRequest(json.dumps(cmd))
      return info
   
   ####################################################################################################

   def listCloudDomainByName(self, name):
      """
         Returns JSON Information of a Cloud Domain by Name
      """
      cmd = {"cmd":"$Customer.listCloudDomains", "args": None}

      info = self.makeZapyRequest(json.dumps(cmd))

      for i in range(len(info['data'])):
	 if name == info['data'][i]['cloudDomainName']:
	    return info['data'][i]

      return None
   
   ####################################################################################################
   #
   # Functions to Validate IP Addresses
   #
   ####################################################################################################

   def validateIpAddr(self, Ip):
      """
         Validates the WFF of an IP Address

         Rough BNF of the Rules Used:

	    Q     ::= [0-255]
	    C     ::= [1-32]
	    Valid ::= Q.Q.Q.Q | Q.Q.Q.Q/C
      """
      valid = 0

      toks = re.split("\.|/", Ip)

      if len(toks) == 4 or len(toks) == 5:
	 for i in range(4):
	    if int(toks[i]) in range(0, 254):
	       valid += 1

	 if len(toks) == 5:
	    if int(toks[4]) in range(0, 32):
	       valid += 1

      if valid == 4 or valid == 5:
	 return True
      else:
	 return False

   ####################################################################################################

   def distIpAddr(self, Ip1, Ip2):
      """
         Converts two IP Addresses into 32-bit Numbers and Returns the "distance" between them

	 Does Not Work on CIDR!
      """

      toks1 = []
      toks2 = []

      if self.validateIpRange(Ip1, Ip2):
	 toks1 = re.split("\.|/", Ip1)
	 toks2 = re.split("\.|/", Ip2)
      else:
	 toks1 = re.split("\.|/", Ip2)
	 toks2 = re.split("\.|/", Ip1)

      bin1 = (int(toks1[0]) << 24) + (int(toks1[1]) << 16) + (int(toks1[2]) << 8) + int(toks1[3])
      bin2 = (int(toks2[0]) << 24) + (int(toks2[1]) << 16) + (int(toks2[2]) << 8) + int(toks2[3])

      return abs(bin1 - bin2)
   
   ####################################################################################################

   def validateIpRange(self, Ip1, Ip2):
      """
         Checks that Ip1 is the lower boundry of an IP Range

	 Return True if so, True if the range is zero (Ip1 == Ip2), False if not
      """

      toks1 = re.split("\.|/", Ip1)
      toks2 = re.split("\.|/", Ip2)

      bin1 = (int(toks1[0]) << 24) + (int(toks1[1]) << 16) + (int(toks1[2]) << 8) + int(toks1[3])
      bin2 = (int(toks2[0]) << 24) + (int(toks2[1]) << 16) + (int(toks2[2]) << 8) + int(toks2[3])

      dist = bin2 - bin1
      
      if dist > 0:
         return True
      elif dist == 0:
         return True
      else:
         return False

   ####################################################################################################

   def validatePort(self, port):
      """
         Checks that a Port Number is Properly Formed
      """

      valid = False

      if int(port) in range(1, 65535):
         valid = 1

      return valid
