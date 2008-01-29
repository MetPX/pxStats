#! /usr/bin/env python
"""
MetPX Copyright (C) 2004-2006  Environment Canada
MetPX comes with ABSOLUTELY NO WARRANTY; For details type see the file
named COPYING in the root of the source directory tree.

##############################################################################
##
##
## Name   : weeklyGraphicsWebPage.py 
##
##
## @author:  Nicholas Lemay
##
## @since:  22-11-2006 ,last updated on 2007-10-23 
##
##
## @summary : Generates a web pages that gives access to user 
##            to the weekly graphics of the last 5 weeks for all rx sources 
##            and tx clients.
##
##
##############################################################################
"""
"""
    Small function that adds pxlib to the environment path.  
"""
import gettext, os, time, sys
sys.path.insert(1, sys.path[0] + '/../../../')

try:
    pxlib = os.path.normpath( os.environ['PXROOT'] ) + '/lib/'
except KeyError:
    pxlib = '/apps/px/lib/'
sys.path.append(pxlib)


"""
    Imports
    PXManager requires pxlib 
"""
from PXManager import *

from pxStats.lib.StatsPaths import StatsPaths
from pxStats.lib.StatsDateLib import StatsDateLib
from pxStats.lib.GeneralStatsLibraryMethods import GeneralStatsLibraryMethods
from pxStats.lib.StatsConfigParameters import StatsConfigParameters
from pxStats.lib.WebPageGeneratorInterface import WebPageGeneratorInterface


LOCAL_MACHINE = os.uname()[1]      
   
NB_WEEKS_DISPLAYED = 3 

CURRENT_MODULE_ABS_PATH = os.path.abspath( sys.path[0] ) + '/' + __name__ 

class DailyGraphicsWebPageGenerator( WebPageGeneratorInterface ): 



    def __init__( self, displayedLanguage = 'en', filesLanguage='en', weeks = None, \
                  pathsTowardsGraphics = None, pathsTowardsOutputFiles = None  ):
        """
        
            @summary : Constructor 
            
            @param displayedLanguage: Languages in which to display 
                                      the different captions found within 
                                      the generated web page.  
            
            @param fileLanguages: Language in which the files that 
                                  will be referenced within this page
                                  have been generated.
                                  
            @param weeks : List of weeks that the web page covers.
        
            @note : Will set two global translators to be used throughout this module 
                    _ which translates every caption that is to be printed.
                    _F which translates every filename that is to be linked.     
        """
        
        configParameters = StatsConfigParameters()
        configParameters.getGeneralParametersFromStatsConfigurationFile()
      
        global _ 
        _ =  self.getTranslatorForModule( CURRENT_MODULE_ABS_PATH, displayedLanguage )
        
        if weeks == None:
            self.setWeeks()
        else:    
            self.weeks = weeks
                
        self.displayedLanguage = displayedLanguage
        self.filesLanguage     = filesLanguage
       
        self.pathsTowardsGraphics = StatsPaths()
        self.pathsTowardsGraphics.setPaths( filesLanguage )
        
        self.pathsTowardsOutputFiles = StatsPaths()
        self.pathsTowardsOutputFiles.setPaths( configParameters.mainApplicationLanguage )    
    

    
    def setWeeks( self ):
        """
            Returns the 3 week numbers including current week number.
        
        """
        
        weeks = []
        
        startTime = (time.time() - ( NB_WEEKS_DISPLAYED*7*24*60*60 ) )
        for i in range( 1, ( NB_WEEKS_DISPLAYED + 1 ) ):
            weeks.append( startTime + (i*7*24*60*60) )
       
        self.weeks = weeks 


    
    
    
    def getStartEndOfWebPage():
        """
            Returns the time of the first 
            graphics to be shown on the web 
            page and the time of the last 
            graphic to be displayed. 
            
        """
        
        currentTime = StatsDateLib.getIsoFromEpoch( time.time() )  
        
        start = StatsDateLib.rewindXDays( currentTime, ( NB_WEEKS_DISPLAYED - 1 ) * 7 )
        start = StatsDateLib.getIsoTodaysMidnight( start )
             
        end   = StatsDateLib.getIsoTodaysMidnight( currentTime )
            
        return start, end     
    
    getStartEndOfWebPage = staticmethod( getStartEndOfWebPage )  
    
    
    
    def printWebPage( self, rxNames, txNames ):
        """
            @summary : Generates a web page based on all the 
                       rxnames and tx names that have run during
                       the past x weeks. 
                    
            @param rxNames: List of sources for which to write 
                            links to their weekly graphics.         
            
            @param txNames: List of clients for which to write 
                            links to their weekly graphics.  
            
            @param weekNumbers: List of weeks to search graphics for 
                                look up.
            
            @param language: Language in which to display the web page.
            
            @notes :   Only links to available graphics will be 
                       displayed.
            
            @return : None
        
        """  
        
        rxNamesArray = rxNames.keys()
        txNamesArray = txNames.keys()
        
        rxNamesArray.sort()
        txNamesArray.sort()
        
        #Redirect output towards html page to generate.   
        if not os.path.isdir( self.pathsTowardsOutputFiles.STATSWEBPAGESHTML ):
            os.makedirs(  self.pathsTowardsOutputFiles.STATSWEBPAGESHTML )      
        fileHandle = open( "%sweeklyGraphs_%s.html" % (self.pathsTowardsOutputFiles.STATSWEBPAGESHTML, self.displayedLanguage) , 'w' )
    
    
        fileHandle.write(  """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
       
    
        <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
        
            <head>
                <title> PX Graphics </title>
            
                <link rel="stylesheet" href="../scripts/js/windowfiles/dhtmlwindow.css" type="text/css" />
                
                <script type="text/javascript" src="../scripts/js/windowfiles/dhtmlwindow.js">
                    
                    This is left here to give credit to the original 
                    creators of the dhtml script used for the group pop ups: 
                    /***********************************************
                    * DHTML Window Widget-  Dynamic Drive (www.dynamicdrive.com)
                    * This notice must stay intact for legal use.
                    * Visit http://www.dynamicdrive.com/ for full source code
                    ***********************************************/
                
                </script>
    
        
                <script type="text/javascript">
        
                    var descriptionWindow=dhtmlwindow.open("description", "inline", "description", "Group description", "width=900px,height=120px,left=150px,top=10px,resize=1,scrolling=0", "recal")
                    descriptionWindow.hide()
        
                </script>
        
        
                <STYLE>
                    <!--
                    A{text-decoration:none}
                    -->
                </STYLE>
                
                <style type="text/css">
                    div.left { float: left; }
                    div.right {float: right; }
                </style>
            
               <style type="text/css">
               
                    a.blackLinks{
                        color: #000000;
                    }
                    
                    div.tableContainer {
                        width: 95%%;        /* table width will be 99%% of this*/
                        height: 275px;     /* must be greater than tbody*/
                        overflow: auto;
                        margin: 0 auto;
                        }
                    
    
                    
                    table.cssTable {
                        width: 99%%;        /*100%% of container produces horiz. scroll in Mozilla*/
                        border: none;
                        background-color: #f7f7f7;
                        table-layout: fixed;
                        }
                        
                    table.cssTable>tbody    {  /* child selector syntax which IE6 and older do not support*/
                        overflow: auto; 
                        height: 225px;
                        overflow-x: hidden;
                        }
                        
                    thead tr    {
                        position:relative; 
                        
                        }
                        
                    thead td, thead th {
                        text-align: center;
                        font-size: 14px; 
                        background-color:"#006699";
                        color: steelblue;
                        font-weight: bold;
                        border-top: solid 1px #d8d8d8;
                        }    
                        
                    td.cssTable  {
                        color: #000;
                        padding-right: 2px;
                        font-size: 12px;
                        text-align: left;
                        border-bottom: solid 1px #d8d8d8;
                        border-left: solid 1px #d8d8d8;
                        }
                    
                    tfoot td    {
                        text-align: center;
                        font-size: 11px;
                        font-weight: bold;
                        background-color: papayawhip;
                        color: steelblue;
                        border-top: solid 2px slategray;
                        }
                
                    td:last-child {padding-right: 20px;} /*prevent Mozilla scrollbar from hiding cell content*/
                
                </style>
                
                  
                
                
                <script>
                    counter =0;             
                    function wopen(url, name, w, h){
                    // This function was taken on www.boutell.com
                        
                        w += 32;
                        h += 96;
                        counter +=1; 
                        var win = window.open(url,
                        counter,
                        'width=' + w + ', height=' + h + ', ' +
                        'location=no, menubar=no, ' +
                        'status=no, toolbar=no, scrollbars=no, resizable=no');
                        win.resizeTo(w, h);
                        win.focus();
                    }   
                </script>                 
                
                
                <script>
                    function showSourceHelpPage(){
                       var sourceHelpPage = dhtmlwindow.open("sourceHelpPage", "iframe", "helpPages/source_%s.html" """ %self.displayedLanguage + """, " """ + _("Definition of 'source'") + """", "width=875px,height=100px,resize=1,scrolling=1,center=1", "recal")
                       sourceHelpPage.moveTo("middle", "middle"); 
                    }
                    
                    function showBytecountHelpPage(){
                       var byteCountHelpPage = dhtmlwindow.open("byteCount", "iframe", "helpPages/byteCount_%s.html" """ %self.displayedLanguage + """, " """ +_( "Definition of 'byteCount'") + """", "width=875px,height=150px,resize=1,scrolling=1,center=1", "recal")
                        byteCountHelpPage.moveTo("middle", "middle");
                    }
                    
                    function showClientHelpPage(){
                       var clientHelpPage = dhtmlwindow.open("client", "iframe", "helpPages/client_%s.html" """ %self.displayedLanguage + """, " """ +_( "Definition of 'client'") + """", "width=875px,height=150px,resize=1,scrolling=1,center=1", "recal")
                        .moveTo("middle", "middle");
                    }
                    
                    function showErrorsHelpPage(){
                       var errorsHelpPage = dhtmlwindow.open("errors", "iframe", "helpPages/errors_%s.html" """ %self.displayedLanguage + """, " """ +_( "Definition of 'errors'") +"""", "width=875px,height=150px,resize=1,scrolling=1,center=1", "recal")
                        errorsHelpPage.moveTo("middle", "middle");
                    }
                    
                    function showFilecountHelpPage(){
                       var fileCountHelpPage = dhtmlwindow.open("fileCount", "iframe", "helpPages/fileCount_%s.html" """ %self.displayedLanguage + """, " """ +_("Definition of 'filecount'") + """", "width=875px,height=150px,resize=1,scrolling=1,center=1", "recal")
                        fileCountHelpPage.moveTo("middle", "middle");
                    }
                              
                    function showFilesOverMaxLatencyHelpPage(){
                       var filesOverMaxLatencyHelpPage = dhtmlwindow.open("filesOverMaxLatency", "iframe", "helpPages/filesOverMaxLatency_%s.html" """ %self.displayedLanguage + """, " """ +_("Definition of 'filesOverMaxLatency'") + """", "width=875px,height=150px,resize=1,scrolling=1,center=1", "recal")
                        filesOverMaxLatencyHelpPage.moveTo("middle", "middle");
                    }
                    
                    function showLatencyHelpPage(){
                       var latencyHelpPage = dhtmlwindow.open("latency", "iframe", "helpPages/latency_%s.html" """ %self.displayedLanguage + """, " """ + _("Definition of 'latency'") + """" , "width=875px,height=150px,resize=1,scrolling=1,center=1", "recal")
                        latencyHelpPage.moveTo("middle", "middle");
                    }
                                   
                    
                </script>
                
            </head>    
            
            <body text="#000000" link="#FFFFFF" vlink="000000" bgcolor="#FFF4E5" >
            <br>
            <table width = "100%">
                <tr width = "100%">
                    <div class="left"><b><font size="5"> """ + _("Weekly graphics for RX sources from MetPx.") +""" </font><font size = "2">""" + _("*updated hourly") + """</font></b></div> 
        
        """)
    
        oneFileFound = False
        
        for weekNumber in self.weeks:    
            parameters = StatsConfigParameters( )
            parameters.getAllParameters()               
            machinesStr = str( parameters.sourceMachinesTags ).replace( '[','' ).replace( ']','' ).replace(',','').replace("'","").replace('"','').replace(" ","")
            currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( weekNumber )
            currentWeek = time.strftime("%W", time.gmtime(weekNumber))
            file = "/apps/px/pxStats/data/csvFiles/weekly/" + 'rx' "/%s/%s/%s.csv" %( machinesStr, currentYear, currentWeek ) 
            webLink = "csvFiles/weekly/" + 'rx' +  "/%s/%s/%s.csv" %( machinesStr, currentYear, currentWeek ) 
            
            if os.path.isfile( file ):
                if oneFileFound == False:
                    fileHandle.write(  "<div class='right'><font size='2' color='black'>CSV files&nbsp;:&nbsp; " )
                    oneFileFound = True 
                
                fileHandle.write(  """<a  href="%s" class="blackLinks">%.3s.csv&nbsp;</a>"""%(  webLink,currentWeek ) ) 
            
        if oneFileFound == True :    
            fileHandle.write(  """
                                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                </font>
                            </div>
            """ )
            
            
        fileHandle.write("""
                     </tr>               
                 </table>   
             <br>
             <br>   
        
        
            <div class="tableContainer">         
               <table class="cssTable"> 
               <thead>
            
                <tr>
                    <td bgcolor="#006699" class="cssTable">
                        
                            <font color = "white">                            
                                <center>
                                    """ + _('Sources') + """     
                                    <br>                       
                                    <a target ="popup" href="#" onClick="showSourceHelpPage(); return false;">
                                        ?
                                    </a>
                                <center>        
                            </font>      
                       
                    </td>
                    
                    <td bgcolor="#006699" class="cssTable" title =" """ + _("Display the total of bytes received every day of the week for each sources.") + """">
                        
                            <font color = "white">
                                <center>
                                    """ + _('Bytecount') + """   
                                    <br>
                                    <a target ="popup" href="#" onClick="showBytecountHelpPage(); return false;">                                
                                        ?
                                    </a>
                                </center>
                            </font>
                        
                    </td>
                    
                    <td bgcolor="#006699" class="cssTable" title =" """ + _("Display the total of files received every day of the week for each sources.") + """">
                       
                            <font color = "white">
                                <center>
                                    """ + _('Filecount') + """
                                    <br>
                                    <a target ="popup" href="#" onClick="showFilecountHelpPage(); return false;">                            
                                        ?                          
                                    </a>
                                </center>    
                            </font>
                                      
                    </td>
                    
                    <td bgcolor="#006699" class="cssTable" title =" """+ _("Display the total of errors that occured during the receptions for every day of the week for each sources.") + """">
                        
                            <font color = "white">
                                <center>
                                    """ + _('Errors') + """
                                    <br>
                                    <a target ="popup"  href="#" onClick="showErrorsHelpPage(); return false;">
                                        ?
                                    </a>
                                </center>
                            </font>
                       
                    
                    </td>
                </tr>
            
            </thead>
            <tbody>
               
                    
        """ )    
        
        
        for rxName in rxNamesArray :
            
            if rxNames[rxName] == "" :
                fileHandle.write( """ <tr> <td bgcolor="#99FF99" class="cssTable"> %s </td> """ %(rxName))
                fileHandle.write( """<td bgcolor="#66CCFF"> """+ _("Weeks") + """&nbsp;:&nbsp;""" )
            else:
                machineName = self.getMachineNameFromDescription( rxNames[rxName] )
                fileHandle.write( """ <tr> <td bgcolor="#99FF99" class="cssTable"><div class="left"> %s </div> <div class="right"><a href="#" onClick="descriptionWindow.load('inline', '%s', 'Description');descriptionWindow.show(); return false"><font color="black">?</font></a></div><br>(%s)</td> """ %(rxName, rxNames[rxName].replace("'","").replace('"',''), machineName ) )
                fileHandle.write( """<td bgcolor="#66CCFF">  """+ _("Weeks") + """&nbsp;:&nbsp;""" )        
            
            
            for week in self.weeks:
                currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
                currentWeek = time.strftime("%W", time.gmtime(week))
                file = self.pathsTowardsGraphics.STATSGRAPHSARCHIVES + "weekly/rx/%s/"%( rxName ) + str(currentYear) + "/bytecount/%s.png" %str(currentWeek)
                webLink =  "archives/weekly/rx/%s/"%( rxName ) + str(currentYear) + "/bytecount/%s.png" %str(currentWeek)
                
                if os.path.isfile( file ):
                    fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">%s&nbsp;</a>"""%( rxName, webLink , currentWeek ) ) 
            
            fileHandle.write( "</td>" )    
        
        
            
            fileHandle.write(  """ <td bgcolor="#66CCFF" class="cssTable" >"""+ _("Weeks") + """&nbsp;:&nbsp;""" )
            
            for week in self.weeks:
                currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
                currentWeek = time.strftime("%W", time.gmtime(week))
                file = self.pathsTowardsGraphics.STATSGRAPHSARCHIVES + "weekly/rx/%s/"%( rxName ) + str(currentYear) + "/filecount/%s.png" %str(currentWeek)
                webLink = "archives/weekly/rx/%s/"%( rxName ) + str(currentYear) + "/filecount/%s.png" %str(currentWeek)
                
                if os.path.isfile( file ):
                    fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">%s&nbsp;</a>"""%( rxName, webLink , currentWeek ) ) 
            
            fileHandle.write( "</td>" ) 
            
            
            fileHandle.write(  """ <td bgcolor="#66CCFF" class="cssTable">"""+ _("Weeks") + """&nbsp;:&nbsp;""" )
            
            for week in self.weeks:
                currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
                currentWeek = time.strftime("%W", time.gmtime(week))
                file = self.pathsTowardsGraphics.STATSGRAPHSARCHIVES + "weekly/rx/%s/"%( rxName ) + str(currentYear) + "/errors/%s.png" %str(currentWeek)
                webLink = "archives/weekly/rx/%s/"%( rxName ) + str(currentYear) + "/errors/%s.png" %str(currentWeek)
                
                if os.path.isfile( file ):
                    fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">%s&nbsp;</a>"""%( rxName, webLink , currentWeek ) ) 
            
            fileHandle.write( "</td></tr>" )                            
        
            
            
        fileHandle.write(  """    
        </tbody>
            </table>
        </div> 
        
            <br>
            <table width = "100%">            
                <tr width = "100%">
                    <div class="left"><b><font size="5"> """ + _("Weekly graphics for TX clients from MetPx.") + """ </font><font size = "2">""" +_("*updated hourly") +"""</font></b></div> 
        
        """)
    
        oneFileFound = False
        
        for weekNumber in self.weeks:    
            parameters = StatsConfigParameters( )
            parameters.getAllParameters()               
            machinesStr = str( parameters.sourceMachinesTags ).replace( '[','' ).replace( ']','' ).replace(',','').replace("'","").replace('"','').replace(" ","")
            currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( weekNumber )
            currentWeek = time.strftime("%W", time.gmtime(weekNumber))
            file = "/apps/px/pxStats/data/csvFiles/weekly/" +  "tx" + "/%s/%s/%s.csv" %( machinesStr, currentYear, currentWeek ) 
            webLink = "csvFiles/weekly/" + 'tx' +  "/%s/%s/%s.csv" %( machinesStr, currentYear, currentWeek ) 
            
            
            if os.path.isfile( file ):
                if oneFileFound == False:
                    fileHandle.write(  "<div class='right'><font size='2' color='black'> CSV files&nbsp;:&nbsp; " )
                    oneFileFound = True 
                
                fileHandle.write(  """<a  href="%s" class="blackLinks">%.3s.csv&nbsp;</a>"""%(  webLink,currentWeek ) ) 
            
        if oneFileFound == True :    
            fileHandle.write(  """
                                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                </font>
                            </div>
            """ )
        
        
        
        fileHandle.write("""   
                         </tr>
                        
                     </table>   
                 <br>
                 <br>
        
        
            <div class="tableContainer">         
                <table class="cssTable" > 
                   <thead>
                        <tr>
    
                            <td bgcolor="#006699" class="cssTable">
                                
                                    <font color = "white">
                                        <center>
                                            """ + _('Clients') + """
                                            <br>
                                            <a target ="popup" href="#" onClick="showClientHelpPage(); return false;">
                                                ?
                                            </a>
                                        </center>    
                                    </font> 
                               
                            </td>
                        
                            <td bgcolor="#006699" class="cssTable" title = " """ + _("Display the average latency of file transfers for every day of the week for each clients.") + """">
                                
                                    <font color = "white">
                                        <center>
                                            """ + _('Latency') + """
                                            <br>
                                            <a target ="popup" href="#" onClick="showLatencyHelpPage(); return false;">
                                                ?
                                            </a>
                                        </center>
                                    </font>
                               
                            </td>
                        
                            <td bgcolor="#006699"  class="cssTable" title = " """ + _("Display the total number of files for wich the latency was over 15 seconds for every day of the week for each clients.") +"""">
                                
                                    <font color = "white">
                                        <center>
                                            """ + _('Files Over Max. Lat.') + """
                                            <br>
                                            <a target ="popup" href="#" onClick="showFilesOverMaxLatencyHelpPage(); return false;">
                                                ?
                                            </a>
                                        </center>
                                    </font>
                                                
                            </td>
                        
                            <td bgcolor="#006699" class="cssTable" title = " """ +_("Display the total of bytes transfered every day of the week for each clients.") + """">
                                
                                    <font color = "white">    
                                        <center>
                                            """ + _('Bytecount') + """
                                            <br>
                                            <a target ="popup" href="#" onClick="showBytecountHelpPage(); return false;">
                                                ?
                                            </a>
                                        </center>                                  
                                    </font>
                                
                            </td>
                            
                            <td bgcolor="#006699" class="cssTable" title = " """ +_("Display the total of files transferred every day of the week for each clients.") + """">
                                
                                    <font color = "white">
                                        <center>
                                            """ + _('Filecount') + """
                                            <br>
                                            <a target ="popup" href="#" onClick="showFilecountHelpPage(); return false;">
                                                ?
                                            </a>
                                        </center>
                                    </font>
                                               
                            </td>
                            
                            <td bgcolor="#006699" class="cssTable" title = " """ + _("Display the total of errors that occured during file transfers every day of the week for each clients.") +"""">
                                
                                    <font color = "white">
                                        <center>
                                            """ + _('Errors') + """
                                            <br>
                                            <a target ="popup" href="#" onClick="showErrorsHelpPage(); return false;">
                                                ?
                                            </a>
                                        </center>    
                                    </font>                                       
                            </td>
                
                        </tr>
                    </thead>
                    
                    <tbody>
            
                            
            
        """ )
        
        for txName in txNamesArray :      
            if txNames[txName] == "" :
                fileHandle.write( """<tr> <td bgcolor="#99FF99" class="cssTable"> %s </td> """ %(txName))
                fileHandle.write( """<td bgcolor="#66CCFF" class="cssTable">""" +_("Weeks") + """&nbsp;:&nbsp;""" )
            else:
                machineName = self.getMachineNameFromDescription( txNames[txName] )
                fileHandle.write( """<tr> <td bgcolor="#99FF99" class="cssTable"><div class="left"> %s </div><div class="right"><a href="#" onClick="descriptionWindow.load('inline', '%s', 'Description');descriptionWindow.show(); return false"><font color="black">?</font></a></div><br>(%s)</td> """ %(txName, txNames[txName].replace("'","").replace('"',''), machineName ))
                fileHandle.write( """<td bgcolor="#66CCFF" class="cssTable">""" +_("Weeks") + """&nbsp;:&nbsp;""" ) 
              
            
            for week in self.weeks:
                currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
                currentWeek = time.strftime("%W", time.gmtime(week))
                file = self.pathsTowardsGraphics.STATSGRAPHSARCHIVES + "weekly/tx/%s/"%( txName ) + str(currentYear) + "/latency/%s.png" %str(currentWeek)
                webLink =  "archives/weekly/tx/%s/"%( txName ) + str(currentYear) + "/latency/%s.png" %str(currentWeek)
                
                if os.path.isfile( file ):
                    fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">&nbsp;%s</a>"""%( txName, webLink , currentWeek ) )
            
            fileHandle.write( "</td>" )
            
    
            fileHandle.write(  """ <td bgcolor="#66CCFF" class="cssTable">""" +_("Weeks") + """&nbsp;:&nbsp;""" )
            
            for week in self.weeks:
                currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
                currentWeek = time.strftime("%W", time.gmtime(week))
                
                file = self.pathsTowardsGraphics.STATSGRAPHSARCHIVES + "weekly/tx/%s/"%( txName ) + str(currentYear) + "/filesOverMaxLatency/%s.png" %str(currentWeek)
                webLink = "archives/weekly/tx/%s/"%( txName ) + str(currentYear) + "/filesOverMaxLatency/%s.png" %str(currentWeek)
                
                
                if os.path.isfile( file ):
                    fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">&nbsp;%s</a>"""%( txName, webLink, currentWeek ) )
            
            fileHandle.write( "</td>" )  
            
            
            fileHandle.write(  """ <td bgcolor="#66CCFF" class="cssTable">""" +_("Weeks") + """&nbsp;:&nbsp;""" )
            
            for week in self.weeks:
                currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
                currentWeek = time.strftime("%W", time.gmtime(week))
                
                file    = self.pathsTowardsGraphics.STATSGRAPHSARCHIVES + "weekly/tx/%s/"%( txName ) + str(currentYear) + "/bytecount/%s.png" %str(currentWeek) 
                webLink = "archives/weekly/tx/%s/"%( txName ) + str(currentYear) + "/bytecount/%s.png" %str(currentWeek)
                
                if os.path.isfile( file ):
                    fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">&nbsp;%s</a>"""%( txName, webLink, currentWeek ) )
            
            fileHandle.write( "</td>" )    
            
            fileHandle.write(  """<td bgcolor="#66CCFF" class="cssTable">""" +_("Weeks") + """&nbsp;:&nbsp;""" )
            
            for week in self.weeks:
                currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
                currentWeek = time.strftime("%W", time.gmtime(week))
                
                file    = self.pathsTowardsGraphics.STATSGRAPHSARCHIVES + "weekly/tx/%s/"%( txName ) + str(currentYear) + "/filecount/%s.png" %str(currentWeek)
                webLink = "archives/weekly/tx/%s/"%( txName ) + str(currentYear) + "/filecount/%s.png" %str(currentWeek)
                            
                if os.path.isfile( file ):
                    fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">&nbsp;%s</a>"""%( txName, webLink, currentWeek ) )
            
            fileHandle.write( "</td>" )   
            
            fileHandle.write(  """ <td bgcolor="#66CCFF" class="cssTable">""" +_("Weeks") + """&nbsp;:&nbsp;""" )
            
            for week in self.weeks:
                currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
                currentWeek = time.strftime("%W", time.gmtime(week))
                
                file    =  self.pathsTowardsGraphics.STATSGRAPHSARCHIVES + "weekly/tx/%s/"%( txName ) + str(currentYear) + "/errors/%s.png" %str(currentWeek)
                webLink =  "archives/weekly/tx/%s/"%( txName ) + str(currentYear) + "/errors/%s.png" %str(currentWeek)
                            
                if os.path.isfile( file ):
                    fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">&nbsp;%s</a>"""%( txName, webLink, currentWeek ) )
            
            fileHandle.write( "</td></tr>" )    
     
            
    
        fileHandle.write(  """    
                     </tbody>
                 </table>    
            </div>
        </body>
        
        
    </html>
        
        
        
        """  )      
                    
        fileHandle.close()         
        
    

    def generateWebPage( self ):
        """
        
            @summary : Call to generate the web page. 
            
        """
        
        self.setWeeks()
        start, end = self.getStartEndOfWebPage()
        rxNames, txNames = GeneralStatsLibraryMethods.getRxTxNamesForWebPages( start, end )
        self.printWebPage( rxNames, txNames )
    
    
   