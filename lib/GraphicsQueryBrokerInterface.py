#! /usr/bin/env python
"""
MetPX Copyright (C) 2004-2006  Environment Canada
MetPX comes with ABSOLUTELY NO WARRANTY; For details type see the file
named COPYING in the root of the source directory tree.


##############################################################################
##
##
## @Name   : GraphicsQueryBrokerInterface.py 
##
##
## @author :  Nicholas Lemay
##
## @since  : 2007-06-28, last updated on 2007-07-03  
##
##
## @summary : This interfaces lists the methods that need to be implemented 
##            by any GraphicsQueryBroker class.
##
##            
##
## @requires: Nothing.
##
##############################################################################
"""


class GraphicsQueryBrokerInterface(object):
    """
        Interface containing the list of methods
        wich need to be implemented by the class 
        wich implement the GraphicsQueryBroker.
          
    """
    
    class _QueryParameters(object):
        """
            List of parameters needed for queries.
        """
        def __init__(self):
            raise "Error. Class needs to implement _QueryParameters class."
    
    class _ReplyParameters(object):
        """
            List of parameters required for replies.
        """
        def __init__(self):
            raise "Error. Class needs to implement _ReplyParameters class."    
    
    def __init__(self):
        """
            Constructor.
        """
        raise "Error. Class needs to implement method"
    
    def getParameters(self):
        """
            Get parameters from cgi...
        """
        raise "Error. Class needs to implement method"
    
    def validateParameters(self):
        """
            Validate parameters.
        """
        raise "Error. Class needs to implement method"    

    def prepareQuery(self):
        """
            Buildup the query  to be executed.
        """
        raise "Error. Class needs to implement method"
    
    def executeQuery(self):
        """
            Execute the built-up query on the needed plotter.
        """
        raise "Error. Class needs to implement method" 
    
    def getReplyToSendToquerier(self):
        """
           Returns the reply of the query to send to the querier.
        """
        raise "Error. Class needs to implement method"