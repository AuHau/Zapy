"Zapy” is an Object Oriented Class Library written in Python for the Zentera API.

The library consists of a set of Python Classes, each named after the API object it represents.

Zapy includes a generator, "genClasses", that writes most of the code.

How? The config files for genClasses contain information literally copied text out of the API documents and pasted it into the config files (with edits). Those config files drive the creation of the Python Classes for the "Zentera API in Python” == “Zapy”.

There is also a generic Parent Class that knows a bunch of high level stuff about our API "zapyClass.py".  Child classes inherit all of those common abilities and add their own capabilities.

Three Directories drive the generator:

   1) Attribs		# Things the Classes Know About
   2) Methods		# Lists of API Calls by Class
   3) Protos		# Short Python functions that add additional capabilites for a Method

There is another "template file" for the Classes, "baseTemplate.py", that seeds the overall structure of
the Classes.

The generator outputs a directory, "Zapy", that contains the Python Package for the library.

Note: Do not directly edit the generated Python files in the Zapy library! Make the changes in
      the appropriate Attribs. Methods, or Proto files and regenerate!
