#! /usr/bin/env python
"""
##############################################################################
##
##
## @Name   : PopSourlientUpAdder.py 
##
##
## @author  :  Nicholas Lemay
##
## @license : MetPX Copyright (C) 2004-2006  Environment Canada
##            MetPX comes with ABSOLUTELY NO WARRANTY; For details type 
##            see the file named COPYING in the root of the source directory 
##            tree.
##
## @since  : 2007-07-03, last updated on 2008-04-15
##
## @summary : This file is to be called from the graphicsResquest page to update
##            the small popup adder utility windows.   
##
##                   
##
##############################################################################
"""

import cgi, gettext, os, time, sys
import cgitb; cgitb.enable()


sys.path.insert(1, sys.path[0] + '/../../..')

from pxStats.lib.GeneralStatsLibraryMethods import GeneralStatsLibraryMethods
from pxStats.lib.StatsConfigParameters import StatsConfigParameters
from pxStats.lib.LanguageTools import LanguageTools
from pxStats.lib.StatsPaths import StatsPaths

LOCAL_MACHINE = os.uname()[1]

CURRENT_MODULE_ABS_PATH =  os.path.abspath(__file__).replace( ".pyc", ".py" )

def generateWebPage( sourlientNames, groups, fileType, outputFileName, language ):
    """
    
        
        @summary: Generates popupAdder web page named after the 
                  received outputFileName and based on the 
                  list of sourlients names received  
        
        @param sourlientNames : List of sources or clients that need to be printed.
        
        @param groups : List of groups that need to be printed.
        
        @param fileType:  tx or rx 
        
        @param outputFileName : Filename that needs to be created.
        
        @return : None
    
    """
     
    statsPaths = StatsPaths()
    statsPaths.setPaths(language)
    
    _ = LanguageTools.getTranslatorForModule( CURRENT_MODULE_ABS_PATH, language )        
    
    if not  os.path.isdir( os.path.dirname(outputFileName) ):
        os.makedirs( os.path.dirname(outputFileName) )
    
    """ Redirect the output"""  
    #print outputFileName
    fileHandle = open( outputFileName, "w" )
    oldStdOut = sys.stdout #save previous stdout
    sys.stdout = fileHandle
    
    print """
    
    <html>
      <head>
        
        <title>Add items to list.</title>
        <meta name="Author" content="Nicholas Lemay">
        <meta name="Description" content="Small popup window used to add items into a list. To be used with graphicsResquests.py">
        <meta name="Keywords" content="">
        <style type="text/css">
            div.selectObject{
                width:300px;            
                height: auto;
            }
            
            
        
        </style>
        <link rel="stylesheet" type="text/css" href="/css/style.css">
    
        <script type="text/javascript" language="JavaScript">
            
            function popupAddingWindow( url ) {
                var newWindow;
                var props = 'scrollBars=no,resizable=no,toolbar=no,menubar=no,location=no,directories=no,width=700,height=300';
                newWindow = window.open(url, "Add_from_Src_to_Dest", props);
            }
            
            function closeWindow(){
                window.close();
            }
            
            // Fill the selcted item list with the items already present in parent.
            function copyLists( srcList, destList ) {
                
                var len = destList.length;
                for(var i = 0; i < srcList.length; i++) {
                    if ( srcList.options[i] != null ) {
                        
                        //Check if this value already exist in the destList or not
                        //if not then add it otherwise do not add it.
                        var found = false;
                        for(var count = 0; count < len; count++) {
                            if (destList.options[count] != null) {
                                if (srcList.options[i].text == destList.options[count].text) {
                                    found = true;
                                    break;
                                }
                            }
                        }
                        
                        if (found != true) {
                            destList.options[len] = new Option(srcList.options[i].text); 
                            len++;
                        }
                    }
                }
            }
            
            
            // Add the SELECTED items from the source to destination list
            // will only add the items wich are not allready present in dest list.
            function addSrcToDestList( srcList, destList ) {
                var len = destList.length;
                for(var i = 0; i < srcList.length; i++) {
                    if ((srcList.options[i] != null) && (srcList.options[i].selected)) {
                        //Check if this value already exist in the destList or not
                        //if not then add it otherwise do not add it.
                        var found = false;
                        for(var count = 0; count < len; count++) {
                            if (destList.options[count] != null) {
                                if (srcList.options[i].text == destList.options[count].text) {
                                    found = true;
                                    break;
                                }
                            }
                        }
                        if (found != true) {
                            destList.options[len] = new Option(srcList.options[i].text); 
                            len++;
                        }
                    }
                }
            }
            
            // Deletes from the destination list.
            function deleteFromList( list ) {
                var len = list.options.length;
                for(var i = (len-1); i >= 0; i--) {
                    if ((list.options[i] != null) && (list.options[i].selected == true)) {
                        list.options[i] = null;
                    }
                }
            }
            
        
        </script>
      
      </head>
      
        <body text="#FFFFFF" link="#FFFFFF" vlink="000000" bgcolor="#7ACC7A">
            
            <center>
            
            <form name="adderForm" method="POST">
                
                <table bgcolor="#FFF4E5" >
                    
                    <tr>
                        <font color ="white">
    
                            <td bgcolor="#006699" width="300" >""" + _("Available") + """</td>
                            <td bgcolor="#006699" >&nbsp;</td>
                            <td bgcolor="#006699" width="300" >""" + _("Selected") + """</td>
                        </font>    
                    </tr>
                    
                    <tr>
        
                        <td bgcolor="#7ACC7A" width="300">
                                
                                <select size="12" style="width: 300px;height: 225px;font: 14px;" name="srcList" multiple> 
  
    """
    
    startingIndex = 1
    
    if len(groups) > 0 :
        
        print """
                                        <optgroup label=""" + '"' + _("Groups:") + """">""" + _("Groups:") + """</optgroup>
        """
        
        for i in range(len(groups)):
            print """    
                                        <option value="%s">%s</option>                      
            """%( i+startingIndex, groups[i] )
        
        startingIndex = i 
    
    
    if len( sourlientNames ) > 0:
        
        if fileType == "tx":
            print """
                                        <optgroup label=""" + '"'+ _("TX clients :") + """">""" + _("TX clients :") + """ </optgroup>
            """  
            
        elif fileType == "rx":
            print """
                                        <optgroup label=""" + '"'+ _("RX sources :") + """">""" + _("RX sources :") + """ </optgroup>
            """
        else:
            print """
                                        <optgroup label=""" + '"'+ _("Sourlients :") + """">""" + _("Sourlients :") +""" </optgroup>
            """       
        
        for i in range(len(sourlientNames)):
            print """    
                                        <option value="%s">%s</option>                      
            """%( i+startingIndex, sourlientNames[i] )
   
   
   
    print """   
                                
                                </select>
    
                        
                        </td>
                        
                        <td bgcolor="#FFF4E5" width="74" align="center">
                            <input type="button" value=" >> " style="font: 14px;" onClick="javascript:addSrcToDestList( document.forms['adderForm'].elements['srcList'], document.forms['adderForm'].elements['destList']  )">
                            <br><br>
                            <input type="button" value=" << " style="font: 14px;" onclick="javascript:deleteFromList( document.forms['adderForm'].elements['destList'] );">
                            <br><br> 
                            <input type="button" value=""" + '"' + _("Done") + '"' + """ style="font: 14px;" onClick ="javascript:window.opener.copyLists(document.forms['adderForm'].elements['destList'], window.opener.document.forms['inputForm'].elements['sourlientList']);javascript:closeWindow();">  
                        </td>
                        
                        <td bgcolor="#7ACC7A" width="300">               
                            <select size="12" style="width: 300px;height: 225px;font: 14px;" name="destList" multiple>
                            </select>
    
                        </td>
                    
                    </tr>

                </table>
            
            </form>
    
            
        </body>
    
    </html>
    
    """
    
    fileHandle.close()                 
    sys.stdout = oldStdOut #resets standard output 
    


def returnReply( error = '' ):
    """
        @summary : Prints an empty reply so that the receiving web page will
                   not modify it's display.
        
    """
    
    reply = "images='';error=%s" %error 
    
    print """
        HTTP/1.0 200 OK
        Server: NCSA/1.0a6
        Content-type: text/plain

    """
    
    print """%s"""  %( reply )    



def getGroups( fileType, machine):
    """
        @summary : Gathers group found in config file.   
        
        @param fileType: Filetype for wich to search groups for.
        @param machine : Machien for wich to search groups for.
        
        @return: returns the list of groups matching the filetype and machine parameters
            
    """
    
    configParameters = StatsConfigParameters()
    configParameters.getAllParameters()
    
    interestingGroups = configParameters.groupParameters.getGroupsAssociatedWithFiletypeAndMachine( fileType, machine )

    return interestingGroups

    
def main():
    """
        @summary : Generates the web page based on the received 
                   machines and file type parameters.
        
    """
    try:
        
        
        newForm = {}
        
        form = cgi.FieldStorage()
        
        for key in form.keys():
            value = form.getvalue(key, "")
            if isinstance(value, list):
                # Multiple username fields specified
                newvalue = ",".join(value)
            else:
                newvalue = value
            
            newForm[key.replace("?","")]= newvalue
        
        form = newForm
        
        try:
            language = form["lang"]
        except: 
            language = ""
            error = "Error.Unknwown language detected in popSourlientUpAdder"    
        
        try:
            fileType = form['fileType']
            if fileType !='tx' and fileType != 'rx':
                error= "Error. File type needs to be either rx or tx."
            
        except:
            fileType = ""
            
            
            
        try:
            machines  = form['machines']
            machine = machines.split( ',' )[0]
            machines = machines.replace( ',', '' )
        except:
            error = "Error. Machine names need to be specified."
            machine = ""
        
        if machines != "":          
            
            rxNames, txNames = GeneralStatsLibraryMethods.getRxTxNames( LOCAL_MACHINE, machine )
            
            groups = getGroups( fileType, machine )
        
        #print "/../../html/popUps/%s%sPopUpSourlientAdder_%s.html" %( fileType, machines, language )
        #----------------------------- fileHandle = open("/web/pxStats/out","w")
        # fileHandle.write(sys.path[0] + "/../../html/popUps/%s%sPopUpSourlientAdder_%s.html" %( fileType, machines, language ))
        #---------------------------------------------------- fileHandle.close()
        
        path = StatsPaths()
        path.setPaths( language )
        
        
        if fileType == "tx":
            generateWebPage(txNames, groups, fileType, path.STATSWEBPAGESHTML + "/popUps/%s%sPopUpSourlientAdder_%s.html" %( fileType, machines, language ), language )
        elif fileType == "rx":
            generateWebPage(rxNames, groups, fileType, path.STATSWEBPAGESHTML + "/popUps/%s%sPopUpSourlientAdder_%s.html" %( fileType, machines, language ), language )
        
        returnReply('') 
    
    except Exception, instance:
        fileHandle = open("/web/pxStats/out","w")
        fileHandle.write( "bug in main method" )
        fileHandle.write( str( instance ) )
        fileHandle.close()                
        sys.exit()
        
        
        
if __name__ == '__main__':
    main()
