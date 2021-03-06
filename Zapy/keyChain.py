"""
   Zapy Key Chain Object Class Definition

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

class keyChain:
   """
      Zapy Object to Manage API Keys and Controller Urls 
   """

   #
   # Class Data and Defaults
   #

   _ZapyDEBUG = True
   _ZapyDEBUG = False

   def __init__(self, keyFileName, apiUrl):
      """
	 Class Configuration Attributes
	    keyFileName: 	File Name of the API Key Pair
	    controllerName:	Shortened URL e.g "zen.example.com"
	    apiKeyId:		API Key Id Token
	    apiSecretKeyBase64:	API Secret Key Token
	    apiUrl:		URL of the Target Controller
      """

      self._cfg = {
	 "keyFileName":		None,
	 "controllerName":	None,
	 "apiKeyId":		None,
	 "apiSecretKeyBase64":	None,
	 "apiUrl":		None
      }

      if self._ZapyDEBUG:
	 print "keyChain.__init__()"
   
      #
      # Load Keys
      #
      if self._ZapyDEBUG:
	 print 'keyFile  == ', keyFileName

      with open(keyFileName, 'r') as f:
	 keyStore = json.load(f)

	 if self._ZapyDEBUG:
	    print 'keyStore loaded'

	 self._cfg['apiKeyId']           = keyStore['apiKeyId']
	 self._cfg['apiSecretKeyBase64'] = keyStore['apiSecretKeyBase64']
	 self._cfg['keyFileName']        = keyFileName

      #
      # Validate and Save Url
      #
      self._cfg['apiUrl'] = self.validateUrl(apiUrl)

      #
      # We should wipe the keyStore object and delete it...
      #    Even if it goes out of scope it might still be in memory!
      #

   ####################################################################################################
   #
   # Class Member Functions
   #
   ####################################################################################################

   # def __str__(self):
   #    return 'keyChain'

   ####################################################################################################

   def get(self, key):
      return(self._cfg[key])

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
   # Method to Validate API URL
   #
   ####################################################################################################

   def validateUrl(self, Url):
      """
         Validates the WFF of an API Url

	 This method expects a Url of the form:

	    go.zentera.net/zAccess
	    go.zentera.net/zCenter

	 It will fill in the rest of a WFF API Url

         Rough BNF of the Rules Used:

	    Protocol    ::= 'https://'
	    Controller  ::= IpAddress | DnsName				# Not validated in this version
	    Service	::= ['zCenter' | 'zAccess'] 'webapi/doApi'	# inserts 'raadmin' if needed

	    apiUrl	::= Protocol Controller Service
      """

      self._cfg['controllerName'] = Url

      apiUrl = Url

      if 'https' not in Url:
         apiUrl = 'https://' + apiUrl

      if 'zAccess' in apiUrl:
         if 'webapi/doApi' not in apiUrl:
	    apiUrl = apiUrl + '/raadmin/webapi/doApi'
      else:
         if 'webapi/doApi' not in apiUrl:
	    apiUrl = apiUrl + '/webapi/doApi'

      apiUrl = apiUrl.replace('zAccess', 'zaccess')

      return apiUrl

   ####################################################################################################
