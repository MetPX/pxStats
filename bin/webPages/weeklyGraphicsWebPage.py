#! /usr/bin/env python
"""
MetPX Copyright (C) 2004-2006  Environment Canada
MetPX comes with ABSOLUTELY NO WARRANTY; For details type see the file
named COPYING in the root of the source directory tree.

##############################################################################
##
##
## Name   : generateGraphics.py 
##
##
## Author : Nicholas Lemay
##
## Date   : 22-11-2006 
##
##
## Description : Generates a web pages that gives access to user 
##               to the weekly graphics of the last 5 weeks for all rx sources 
##               and tx clients.
##
##
##############################################################################
"""
"""
    Small function that adds pxlib to the environment path.  
"""
import os, time, sys
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


LOCAL_MACHINE = os.uname()[1]      
   
NB_WEEKS_DISPLAYED = 3 
    
def getWeeks():
    """
        Returns the 3 week numbers including current week number.
    
    """
    
    weeks = []
    
    startTime = (time.time() - ( NB_WEEKS_DISPLAYED*7*24*60*60 ) )
    for i in range( 1, ( NB_WEEKS_DISPLAYED + 1 ) ):
        weeks.append( startTime + (i*7*24*60*60) )
   
    return weeks
    
    
    
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
    
    
    
def generateWebPage( rxNames, txNames, weekNumbers ):
    """
        Generates a web page based on all the 
        rxnames and tx names that have run during
        the pas x weeks. 
        
        Only links to available graphics will be 
        displayed.
        
    """  
    
    rxNamesArray = rxNames.keys()
    txNamesArray = txNames.keys()
    
    rxNamesArray.sort()
    txNamesArray.sort()
    
    #Redirect output towards html page to generate.   
    if not os.path.isdir( StatsPaths.STATSWEBPAGESHTML ):
        os.makedirs(  StatsPaths.STATSWEBPAGESHTML )      
    fileHandle = open( "%sweeklyGraphs.html" % StatsPaths.STATSWEBPAGESHTML , 'w' )


    fileHandle.write(  """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
   
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
        
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
            
        div.txScroll {
            height: 200px;
            width: 1255px;
            overflow: auto;
            word-wrap:break-word;
            border: 0px ;                    
            padding: 0px;
        }
            
        div.txTableEntry{
            width:177px;            
            height: 10px;
        }
        
        div.rxScroll {
            height: 200px;
            width: 1255px;
            overflow: auto;
            word-wrap:break-word;
            border: 0px ;                    
            padding: 0px;
        }
            
        div.rxTableEntry{
            width:277px;            
            height: 10px;
        }
        
        
        </style>
        
        <head>
            <title> PX Graphics </title>
            
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
            
            
        </head>    
        <body text="#000000" link="#FFFFFF" vlink="000000" bgcolor="#CCCCCC" >
        
        <br>
        <h2>Weekly graphics for RX sources from MetPx.  <font size = "2">*updated hourly</font></h2>
                
        <table cellspacing=10 cellpadding=8 id=header bgcolor="#cccccc">
        
            <tr>
                <td bgcolor="#006699">
                    <div class = "rxTableEntry">
                        <font color = "white">
                            <div class="left">
                            Sources                            
                            </div>
                            <a target ="popup" href="%s" onClick="wopen('helpPages/source.html', 'popup', 875, 100); return false;">
                                <div class="right">
                                ?
                                </div>
                            </a>    
                        </font>      
                    </div>
                </td>
                
                <td bgcolor="#006699" title = "Display the total of bytes received every day of the week for each sources.">
                    <div class = "rxTableEntry">
                        <font color = "white">
                            <div class="left">
                            Bytecount
                            </div>
                            <a target ="popup" href="%s" onClick="wopen('helpPages/byteCount.html', 'popup', 875, 100); return false;">
                                <div class="right">
                                ?
                                </div>
                            </a>
                        </font>
                    </div>
                </td>
                
                <td bgcolor="#006699" title = "Display the total of files received every day of the week for each sources.">
                    <div class = "rxTableEntry">
                        <font color = "white">
                            <div class="left">Filecount</div>
                            <a target ="popup" href="%s" onClick="wopen('helpPages/fileCount.html', 'popup', 875, 100); return false;">                            
                                <div class="right">?</div>                            
                            </a>
                        </font>
                    </div>                
                </td>
                
                <td bgcolor="#006699" title = "Display the total of errors that occured during the receptions for every day of the week for each sources.">
                    <div class = "rxTableEntry">
                        <font color = "white">
                            <div class="left">Errors</div>
                            <a target ="popup"  href="%s" onClick="wopen('helpPages/errors.html', 'popup', 875, 100); return false;">
                                <div class="right">?</div>
                            </a>
                        </font>
                    </div>
                
                </td>
            </tr>
        
        </table>
        
        <div class="rxScroll">    
                
    """ )    
    
    
    for rxName in rxNamesArray :
        
        if rxNames[rxName] == "" :
            fileHandle.write( """<table cellspacing=10 cellpadding=8> <tr> <td bgcolor="#99FF99"><div class = "rxTableEntry"> %s </div></td> """ %(rxName))
            fileHandle.write( """<td bgcolor="#66CCFF"><div class = "rxTableEntry">   Weeks&nbsp;:&nbsp;""" )
        else:
            fileHandle.write( """<table cellspacing=10 cellpadding=8> <tr> <td bgcolor="#99FF99"><div class = "rxTableEntry"><div class="left"> '%s' </div><div class="right"><a href="#" onClick="descriptionWindow.load('inline', %s, 'Group description');descriptionWindow.show(); return false">?</a></div></div></td> """ %(rxName, rxNames[rxName].replace("'","").replace('"','')))
            fileHandle.write( """<td bgcolor="#66CCFF"><div class = "rxTableEntry">   Weeks&nbsp;:&nbsp;""" )        
        
        
        for week in weekNumbers:
            currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
            currentWeek = time.strftime("%W", time.gmtime(week))
            file = StatsPaths.STATSGRAPHSARCHIVES + "weekly/rx/%s/"%( rxName ) + str(currentYear) + "/bytecount/%s.png" %str(currentWeek)
            webLink =  "archives/weekly/rx/%s/"%( rxName ) + str(currentYear) + "/bytecount/%s.png" %str(currentWeek)
            
            if os.path.isfile( file ):
                fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">%s&nbsp;</a>"""%( rxName, webLink , currentWeek ) ) 
        
        fileHandle.write( "</div></td>" )    
    
    
        
        fileHandle.write(  """ <td bgcolor="#66CCFF"><div class = "rxTableEntry">Weeks&nbsp;:&nbsp;""" )
        
        for week in weekNumbers:
            currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
            currentWeek = time.strftime("%W", time.gmtime(week))
            file = StatsPaths.STATSGRAPHSARCHIVES + "weekly/rx/%s/"%( rxName ) + str(currentYear) + "/filecount/%s.png" %str(currentWeek)
            webLink = "archives/weekly/rx/%s/"%( rxName ) + str(currentYear) + "/filecount/%s.png" %str(currentWeek)
            
            if os.path.isfile( file ):
                fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">%s&nbsp;</a>"""%( rxName, webLink , currentWeek ) ) 
        
        fileHandle.write( "</div></td>" ) 
        
        
        fileHandle.write(  """ <td bgcolor="#66CCFF"><div class = "rxTableEntry">Weeks&nbsp;:&nbsp;""" )
        
        for week in weekNumbers:
            currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
            currentWeek = time.strftime("%W", time.gmtime(week))
            file = StatsPaths.STATSGRAPHSARCHIVES + "weekly/rx/%s/"%( rxName ) + str(currentYear) + "/errors/%s.png" %str(currentWeek)
            webLink = "archives/weekly/rx/%s/"%( rxName ) + str(currentYear) + "/errors/%s.png" %str(currentWeek)
            
            if os.path.isfile( file ):
                fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">%s&nbsp;</a>"""%( rxName, webLink , currentWeek ) ) 
        
        fileHandle.write( "</div></td></tr></table>" )                            
    
        
        
    fileHandle.write(  """    
    </div> 
    
    <br>        
    
    <h2>Weekly graphics for TX clients from MetPx.  <font size = "2">*updated hourly</font></h2>    
    
        <table cellspacing=10 cellpadding=8 id=header bgcolor="#cccccc">        
            <tr>

                <td bgcolor="#006699">
                    <div class = "txTableEntry">
                        <font color = "white">
                            <div class="left">Clients</div>
                            <a target ="popup" href="%s" onClick="wopen('helpPages/client.html', 'popup', 875, 100); return false;">
                                <div class="right">?</div>
                            </a>
                        </font> 
                    </div>
                </td>
            
                <td bgcolor="#006699" title = "Display the taverage latency of file transfers for every day of the week for each clients.">
                    <div class = "txTableEntry">
                        <font color = "white"><div class="left">Latency</div>
                            <a target ="popup" href="%s" onClick="wopen('helpPages/latency.html', 'popup', 875, 100); return false;">
                                <div class="right">?</div>
                            </a>
                        </font>
                    </div>
                </td>
            
                <td bgcolor="#006699" title = "Display the total number of files for wich the latency was over 15 seconds for every day of the week for each clients.">
                    <div class = "txTableEntry">
                        <font color = "white"><div class="left">Files Over Max. Lat.</div>
                            <a target ="popup" href="%s" onClick="wopen('helpPages/filesOverMaxLatency.html', 'popup', 875, 100); return false;">
                                <div class="right">?</div>
                            </a>
                        </font>
                    </div>                
                </td>
            
                <td bgcolor="#006699" title = "Display the total of bytes transfered every day of the week for each clients.">
                    <div class = "txTableEntry">
                        <font color = "white">                 
                            <div class="left">Bytecount</div>
                             <a target ="popup" href="%s" onClick="wopen('helpPages/byteCount.html', 'popup', 875, 100); return false;">
                                    <div class="right">?</div>
                             </a>                            
                        </font>
                    </div>
                </td>
                
                <td bgcolor="#006699"  title = "Display the total of files transferred every day of the week for each clients.">
                    <div class = "txTableEntry">
                        <font color = "white">
                            <div class="left">Filecount</div>
                            <a target ="popup" href="%s" onClick="wopen('helpPages/fileCount.html', 'popup', 875, 100); return false;">
                                <div class="right">?</div>
                            </a>
                        </font>
                    </div>                
                </td>
                
                <td bgcolor="#006699" title = "Display the total of errors that occured during file transfers every day of the week for each clients.">
                    <div class = "txTableEntry">
                        <font color = "white">
                            <div class="left">Errors</div>
                            <a target ="popup" href="%s" onClick="wopen('helpPages/errors.html', 'popup', 875, 100); return false;">
                                <div class="right">?</div>
                            </a>
                        </font>
                    </div>                
                </td>
            
            </tr>
        
        </table>
        
        <div class="txScroll">                
        
    """ )
    
    for txName in txNamesArray :      
        if txNames[txName] == "" :
            fileHandle.write( """<table cellspacing=10 cellpadding=8> <tr> <td bgcolor="#99FF99"><div class = "txTableEntry"> %s </div></td> """ %(txName))
            fileHandle.write( """<td bgcolor="#66CCFF"><div class = "txTableEntry">Weeks&nbsp;:&nbsp;""" )
        else:
            fileHandle.write( """<table cellspacing=10 cellpadding=8> <tr> <td bgcolor="#99FF99"><div class = "txTableEntry"><div class="left"> %s </div><div class="right"><a href="#" onClick="descriptionWindow.load('inline', '%s', 'Group description');descriptionWindow.show(); return false">?</a></div></div></td> """ %(txName, txNames[txName].replace("'","").replace('"','')))
            fileHandle.write( """<td bgcolor="#66CCFF"><div class = "txTableEntry">Weeks&nbsp;:&nbsp;""" ) 
          
        
        for week in weekNumbers:
            currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
            currentWeek = time.strftime("%W", time.gmtime(week))
            file = StatsPaths.STATSGRAPHSARCHIVES + "weekly/tx/%s/"%( txName ) + str(currentYear) + "/latency/%s.png" %str(currentWeek)
            webLink =  "archives/weekly/tx/%s/"%( txName ) + str(currentYear) + "/latency/%s.png" %str(currentWeek)
            
            if os.path.isfile( file ):
                fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">&nbsp;%s</a>"""%( txName, webLink , currentWeek ) )
        
        fileHandle.write( "</div></td>" )
        

        fileHandle.write(  """ <td bgcolor="#66CCFF"><div class = "txTableEntry">Weeks&nbsp;:&nbsp;""" )
        
        for week in weekNumbers:
            currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
            currentWeek = time.strftime("%W", time.gmtime(week))
            
            file = StatsPaths.STATSGRAPHSARCHIVES + "weekly/tx/%s/"%( txName ) + str(currentYear) + "/filesOverMaxLatency/%s.png" %str(currentWeek)
            webLink = "archives/weekly/tx/%s/"%( txName ) + str(currentYear) + "/filesOverMaxLatency/%s.png" %str(currentWeek)
            
            
            if os.path.isfile( file ):
                fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">&nbsp;%s</a>"""%( txName, webLink, currentWeek ) )
        
        fileHandle.write( "</div></td>" )  
        
        
        fileHandle.write(  """ <td bgcolor="#66CCFF"><div class = "txTableEntry">Weeks&nbsp;:&nbsp;""" )
        
        for week in weekNumbers:
            currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
            currentWeek = time.strftime("%W", time.gmtime(week))
            
            file    = StatsPaths.STATSGRAPHSARCHIVES + "weekly/tx/%s/"%( txName ) + str(currentYear) + "/bytecount/%s.png" %str(currentWeek) 
            webLink = "archives/weekly/tx/%s/"%( txName ) + str(currentYear) + "/bytecount/%s.png" %str(currentWeek)
            
            if os.path.isfile( file ):
                fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">&nbsp;%s</a>"""%( txName, webLink, currentWeek ) )
        
        fileHandle.write( "</div></td>" )    
        
        fileHandle.write(  """<td bgcolor="#66CCFF"><div class = "txTableEntry">Weeks&nbsp;:&nbsp;""" )
        
        for week in weekNumbers:
            currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
            currentWeek = time.strftime("%W", time.gmtime(week))
            
            file    = StatsPaths.STATSGRAPHSARCHIVES + "weekly/tx/%s/"%( txName ) + str(currentYear) + "/filecount/%s.png" %str(currentWeek)
            webLink = "archives/weekly/tx/%s/"%( txName ) + str(currentYear) + "/filecount/%s.png" %str(currentWeek)
                        
            if os.path.isfile( file ):
                fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">&nbsp;%s</a>"""%( txName, webLink, currentWeek ) )
        
        fileHandle.write( "</div></td>" )   
        
        fileHandle.write(  """ <td bgcolor="#66CCFF"><div class = "txTableEntry">Weeks&nbsp;:&nbsp;""" )
        
        for week in weekNumbers:
            currentYear, currentMonth, currentDay = StatsDateLib.getYearMonthDayInStrfTime( week )
            currentWeek = time.strftime("%W", time.gmtime(week))
            
            file    =  StatsPaths.STATSGRAPHSARCHIVES + "weekly/tx/%s/"%( txName ) + str(currentYear) + "/errors/%s.png" %str(currentWeek)
            webLink =  "archives/weekly/tx/%s/"%( txName ) + str(currentYear) + "/errors/%s.png" %str(currentWeek)
                        
            if os.path.isfile( file ):
                fileHandle.write(  """<a target ="popup" href="%s" onClick="wopen('%s', 'popup', 875, 240); return false;">&nbsp;%s</a>"""%( txName, webLink, currentWeek ) )
        
        fileHandle.write( "</div></td></tr></table>" )    
 
        

    fileHandle.write(  """    
    
    </div>
    </body>
    </html>
    
    
    
    """  )      
                
    fileHandle.close()         
    
    

def main():        
    
    weeks = getWeeks() 
    
    start, end = getStartEndOfWebPage()     
    
    rxNames, txNames = GeneralStatsLibraryMethods.getRxTxNamesForWebPages(start, end)
             
    generateWebPage( rxNames, txNames, weeks)
    
    
   
if __name__ == "__main__":
    main()