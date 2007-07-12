#! /usr/bin/env python
"""
MetPX Copyright (C) 2004-2006  Environment Canada
MetPX comes with ABSOLUTELY NO WARRANTY; For details type see the file
named COPYING in the root of the source directory tree.


##############################################################################
##
##
## @Name   : RRDQueryBroker.py 
##
##
## @author :  Nicholas Lemay
##
## @since  : 2007-06-28, last updated on 2007-07-03  
##
##
## @summary : This class implements the GraphicsQueryBrokerInterface
##            and allows to execute queries towards the rrd graphics
##            creator from a web interface.  
##
##            
##
## @requires: generateRRDGraphics.py 
##
##############################################################################
"""

import cgi, commands, os, sys
import cgitb; cgitb.enable()
sys.path.insert(1, sys.path[0] + '/../../')


from pxStats.lib.StatsPaths import StatsPaths
from pxStats.lib.GeneralStatsLibraryMethods import GeneralStatsLibraryMethods


class RRDQueryBroker(GraphicsQueryBrokerInterface):
    """
        Interface containing the list of methods
        wich need to be implemented by the class 
        wich implement the GraphicsQueryBroker.
          
    """
    
    def __init__(self,  query, reply, queryParameters = None, replyParameters = None, graphicProducer = None ):
        """
            @summary: GnuQueryBroker constructor.
            
            @param queryParameters: _QueryParameters instance wich 
                                    contains the query parameters. 
            
            @param replyParameters: _replyParameters instance wich contains the reply parameters.
             
            @param reply: Reply to send to querier
            
            @query : Query to send to generateRRDGraphics.py
              
        
        """
        
        
        self.queryParameters = queryParameters
        self.query = query
        self.replyParameters = replyParameters
        self.reply = reply 
    
    
    
    class _QueryParameters(object):
        """
            List of parameters needed for queries.
        """
        
        
        
        def __init__( self, fileType, sourLients, groupName, machines, individual, total, endTime,  products, statsTypes,  span, specificSpan, fixedSpan ):
            """
                @summary : _QueryParameters parameters class constructor.                
                
                @param fileType: rx or tx                
                @param sourLients: list of sour or clients for wich to produce graphic(s).                
                @param groupName: Group name tag to give to a group of clients.      
                @param machines : List of machine on wich the data resides.           
                @param individual: Whether or not to make individual graphics for every machines.
                @param total : Whether or not to  make a total of all the data prior to plotting the graphics.               
                @param endTime: time of query of the graphics                
                @param products: List of specific products for wich to plot graphics.                
                @param statsTypes : List of stats types for wich to create the graphics.
                @param span: span in hoursof the graphic(s).            
                @param specificSpan: Daily, weekly,monthly or yearly
                @param fixedSpan : fixedPrevious or fixedCurrent
                
            """
            
            self.fileType     = fileType
            self.sourLients   = sourLients
            self.groupName    = groupName
            self.machines     = machines
            self.individual   = individual
            self.total        = total
            self.endTime      = endTime
            self.products     = products
            self.statsTypes   = statsTypes
            self.span         = span
            self.specificSpan = specificSpan
            self.fixedSpan    = fixedSpan    
    
    
    class _ReplyParameters(object):
        """
            List of parameters required for replies.
        """
        
        def __init__( self, querier, plotter, image, fileType, sourLients, groupName, machines, individual, total, endTime,  products, statsTypes,  span, specificSpan, fixedSpan ):
            """
                @summary : _QueryParameters parameters class constructor.    
                            
                @param querier:Path to the program that sent out the request.
                @param plotter : Type of plotter that was selected.
                @param image   : image(s) that was/were produced by the plotter. 
                @param fileType: rx or tx                
                @param sourLients: list of sour or clients for wich to produce graphic(s).                
                @param groupName: Group name tag to give to a group of clients.      
                @param machines : List of machine on wich the data resides.           
                @param individual: Whether or not to make individual graphics for every machines.
                @param total : Whether or not to  make a total of all the data prior to plotting the graphics.               
                @param endTime: time of query of the graphics                
                @param products: List of specific products for wich to plot graphics.                
                @param statsTypes : List of stats types for wich to create the graphics.
                @param span: span in hoursof the graphic(s).            
                @param specificSpan: Daily, weekly,monthly or yearly
                @param fixedSpan : fixedPrevious or fixedCurrent
            """
            
            self.querier      = querier
            self.plotter      = plotter 
            self.image        = image
            self.fileType     = fileType
            self.sourLients   = sourLients
            self.groupName    = groupName
            self.machines     = machines
            self.individual   = individual
            self.total        = total
            self.endTime      = endTime
            self.products     = products
            self.statsTypes   = statsTypes
            self.span         = span
            self.specificSpan = specificSpan
            self.fixedSpan    = fixedSpan    
    
    
        
    def getParametersFromForm(self, form):
        """
             @summary: Initialises the queryParameters and 
                       reply parameters based on the form 
                       received as parameter. 
        """
        
        #Every param is set in an array, use [0] to get first item, nothing for array.
        querier      = form["querier"][0]
        plotter      = form["plotter"][0] 
        image        = None
        fileTypes    = form["fileType"]
        sourLients   = form["sourLients"]
        groupName    = form["groupName"][0]        
        machines     = form["machines"]
        individual   = form["individual"][0]
        total        = form["total"][0]        
        endTime      = form["endTime"][0]
        products     = form["products"]
        statsTypes   = form["statsTypes"]
        span         = form["span"][0] 
        specificSpan = form["specificSpan"][0]
        fixedSpan    = form["fixedSpan"][0]
    
    
        
    def getParameters(self, parser, form):
        """
            @summary : Get parameters from either a form or a parser. 
                       Both need to have parameter names wich are the 
                       same as the ones used in the _QueryParameters
                       class.  
        """
        
        if form != None:
             self.getParametersFromForm( form )
    
    
    
    def searchForParameterErrors(self):
        """
            @summary : Validates parameters.
           
            @return  : Returns the first error 
                       found within the current
                       query parameters. 
        """
        
        error = ""
           
        try :
            
            if self.queryParameters.plotter != "rrd":
                error = "Internal error. GnuQueryBroker was not called to plota gnuplot graphic."
                raise
        
            for filetype in self.queryParameters.fileTypes :
                if fileType != "tx" and fileType != "rx":
                    error = "Error. FileType needs to be either rx or tx."
                    raise
                
            if self.queryParameters.sourLients == []:
                error = "Error. At least one sourlient needs to be specified."
            
            if self.queryParameters.machines == []:
                error = "Error. At least one machine name needs to be specified."
            
            if self.queryParameters.combine != 'true' and self.queryParameters.combine != 'false':
                error = "Error. Combine sourlients option needs to be either true or false."  
            
            if self.queryParameters.statsTypes == []:
                error = "Error. At Leat one statsType needs to be specified."   
            
            if self.queryParameters.groupName != "" and self.queryParameters.total != 'true':
                error = "Error. Groupname needs to be used with total option."
                raise 
            
            if self.queryParameters.groupName != "" and self.queryParameters.individual == 'true':
                error = "Error. Groupname cannot be used with individual option."
                raise
            
            if self.queryParameters.fixedSpan != "" and self.specificSpan == "":
                error = "Error. Fixed spans need to be used with a specific spans."
                raise
            
            try:
                int(self.queryParameters.span)
            except:
                error = "Error. Span(in hours) value needs to be numeric."          
                
        except:
            
            pass
        
        
        return error     
    


    def prepareQuery(self):
        """
            @summary : Buildup the query  to be executed.
        
            @SIDE_EFFECT :  modifies self.query value.
            
        """
        
        pathToGenerateRRDGraphs = StatsPaths.STATSBIN + "generateRRDGraphics.py"
        
        sourlients = '-c %s'  %( str( self.queryParameters.sourLients).replace( '[', '' ).replace( ']', '' ) )
        
        splitDate = date.split("-")
        date = "-d '%s'" %( splitDate[2] + '-' + splitDate[1]  + '-' + splitDate[0] + '-' + splitDate[3] )
        
        fileType = '-f %s' %( self.queryParameters.fileType )
        
        #optional option
        if self.queryParameters.specificSpan == "daily":
            specificSpan = "-d"
        elif self.queryParameters.specificSpan == "weekly":
            specificSpan = "-m"        
        elif self.queryParameters.specificSpan == "monthly":
            specificSpan = "-m"
        elif self.queryParameters.specificSpan == "yearly":
            specificSpan = "-y"
        else:
            specificSpan = ""      
        
        if self.queryParameters.fixedSpan == "fixedCurrent" :
            fixedSpan = "--fixedCurrent"
        elif self.queryParameters.fixedSpan == "fixedPrevious":
            fixedSpan = "--fixedPrevious"     
        else:
            fixedSpan = ""
            
        if self.queryParameters.havingRun == 'true':
            havingRun = "--havingrun"
        else:
            havingRun = ""
        
        if self.queryParameters.individual == 'true':
            individual = '--individual'
        else:
            individual = ''    
        
        if self.queryParameters.total == 'true' :
            total = '--total'
        else:
            total = ''    
        
        if self.queryParameters.type !=[]:
            type = str(self.queryParameters.type)        
        else:
            types = "--types %s" %( str(self.queryParameters.type).replace( '[', '' ).replace( ']', '' ) )
        
        self.query = "%s %s %s %s %s %s %s %s %s %s %s %s " %( pathToGenerateRRDGraphs, sourlients, date, fileType, fixedSpan, specificSpan, havingRun, total, individual, types)
            
            
    def getImagesFromOutput( output ):
        """ 
            @summary : Parses the output and retreives 
                       the name of images that were plotted.
            
            @return: Returns the list of images
        """
        
        images = []
        
        lines = output.splitlines()
        
        for line in lines :
            if "".startswith( "Plotted : " ):
                imageName = (line.split( ":" )[1]).replace( " ", "")
            images.append( imageName )
            
        return images 
    
    
    
    def executeQuery(self):
        """
            @summary : Simply Execute the query stored in self.query.
            
            @SIDE-EFECT : Will set the name of the generated images in self.replyparameters.image
            
        """
        
        status, output = commands.getstatusoutput( self.query )  
        
        if status == 0 :#If query was executed properly.
            self.image = RRDQueryBroker.getImageFromQueryOutput( output )
    
    
    
    def getReplyToSendToquerier(self):
        """
           Returns the reply of the query to send to the querier.
        """
        params = self.replyParameters
        
        reply = "?plotter=%s&?image=%s&fileType=%s&sourlients=%s&groupName=%s&machines=%s&individual=%s&total=%s&%endTime=%s&products=%s&statsTypes=%s&span=%s&specificSpan=%s&fixedSpan=%s" \
         %( params.plotter, params.image, params.fileType, params.sourLients, params.groupName,
            params.machines, params.individual, params.total, params.endtime, params.products, params.statsTypes, params.span, params.specificSpan, params.fixedSpan  )
         
        return reply
        
        
        
        
        