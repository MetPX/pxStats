#! /usr/bin/env python

"""
##########################################################################
##
## @name    : pxStatsStartup.py 
##  
##
## @license : MetPX Copyright (C) 2004-2006  Environment Canada
##            MetPX comes with ABSOLUTELY NO WARRANTY; For details type 
##            see the file named COPYING in the root of the source directory tree.
##
##
## @author  : Nicholas Lemay  
##
## @since   : May 19th 2006, Last updated on March 05th 2008
##
##
## @summary : PXStats' main application file. Everything can be run
##            automatically from here granted the configuration files
##            are filled in properly. 
##             
##            Should be called by a crontab, but can be called from command 
##           
##
#############################################################################
"""

import os, sys, commands, time

"""
    Adds pxStats to sys.path
"""
sys.path.insert(1, os.path.dirname( os.path.abspath(__file__) ) + '/../../')

from pxStats.lib.StatsPaths import StatsPaths
from pxStats.lib.StatsDateLib import StatsDateLib

from pxStats.lib.MachineConfigParameters import MachineConfigParameters
from pxStats.lib.StatsConfigParameters import StatsConfigParameters
from pxStats.lib.CpickleWrapper import CpickleWrapper
from pxStats.lib.GeneralStatsLibraryMethods import GeneralStatsLibraryMethods
from pxStats.lib.WebPageGraphicsGenerator import WebPageGraphicsGenerator
from pxStats.lib.DailyGraphicsWebPageGenerator import DailyGraphicsWebPageGenerator
from pxStats.lib.WeeklyGraphicsWebPageGenerator import WeeklyGraphicsWebPageGenerator
from pxStats.lib.MonthlyGraphicsWebPageGenerator import MonthlyGraphicsWebPageGenerator
from pxStats.lib.YearlyGraphicsWebPageGenerator import YearlyGraphicsWebPageGenerator
from pxStats.lib.BottomWebPageGenerator import BottomWebPageGenerator
from pxStats.lib.TopWebPageGenerator import TopWebPageGenerator
from pxStats.lib.TotalsGraphicsWebPagesGenerator import TotalsGraphicsWebPageGenerator
from pxStats.lib.AutomaticUpdatesManager import AutomaticUpdatesManager
from pxStats.lib.LanguageTools import LanguageTools


LOCAL_MACHINE = os.uname()[1]

CURRENT_MODULE_ABS_PATH =  os.path.abspath(__file__).replace( ".pyc", ".py" )             



def validateParameters( parameters, machineParameters, logger = None  ):
    """
        @summary : Validates parameters. 
        
        @note    : If a an illegal parameter is encountered application
                   will be terminated.     
          
    """   
    
    global _ 
    
    if len( parameters.picklingMachines ) != len(parameters.sourceMachinesTags ) :
    
        if logger != None:
            logger.error( _("Error reading config file in launchGraphCreation program. Parameter number mismatch. Program was terminated abruptly.") ) 
        print _( "Error reading config file in launchGraphCreation program. Parameter number mismatch. Program was terminated abruptly.")
        sys.exit()
        
        
    for tag in parameters.sourceMachinesTags:
        
        if len( parameters.detailedParameters.sourceMachinesForTag[tag]) != len( parameters.detailedParameters.picklingMachines[tag] ):    
            if logger != None:
                logger.error( _("Error reading config file in launchGraphCreation program. Parameter number mismatch. Program was terminated abruptly.")  )
            
            print _("Error reading config file. Parameter number mismatch between pickling machines and source machines associated with %s tag . Program was terminated abruptly.") %tag    
            print _("source machines : %s  picklingmachines : %s ") %(parameters.detailedParameters.sourceMachinesForTag[tag], parameters.detailedParameters.picklingMachines[tag] )
            sys.exit()
               
        for machine in parameters.detailedParameters.sourceMachinesForTag[tag]:
            if machineParameters.getUserNameForMachine( machine ) == "":            
                        
                if logger != None:
                    logger.error( _("Error reading config file in launchGraphCreation program. Program was terminated abruptly.") ) 
                print _("Error reading config file in launchGraphCreation program. Program was terminated abruptly.")
                sys.exit()
    

            
def updatePickles( parameters, machineParameters, currentTimeInIsoFormat ):
    """
        @summary : Updates the pickle files for all the specified log machines
                   so that they are available for graphic production.
        
        @note : Pickling is to be done on specified pickling machines.
        
                All the pickle files that are produced on remote machines will be 
                downloaded on the local machine.
                
        
        @param parameters: StatsConfigParameters instance containing 
                           the parameters found in the config file.
        
        @param machineParameters: MachineConfigParameters instance containing 
                                  the parameters found in the config file.
        
        @param currentTimeInIsoFormat : Time at which this program was originally 
                                        called.        
    
        
    """      
        
    nbChildProcess = 0        
    
    paths = StatsPaths()
    paths.setPaths()
    
    for tag in parameters.sourceMachinesTags:
        pid = os.fork()
        if pid == 0: #if child                   
            sourceMachines = machineParameters.getMachinesAssociatedWith(tag)            
            
            for i in range( len( sourceMachines  ) ):
                
                picklingMachine  = parameters.detailedParameters.picklingMachines[tag][i]
                            
                # If pickling and source machines differ, download log files frm source to pickling machine.            
                if  sourceMachines[i] != picklingMachine: 
                    
                    if parameters.detailedParameters.picklingMachines[tag][i] != LOCAL_MACHINE :#pickling to be done elsewhere
                        for j in range(3):#do 3 times in case of currently turning log files.
                            remotePxLogPath = paths.getPXPathFromMachine(paths.PXLOG, sourceMachines[i], machineParameters.getUserNameForMachine( sourceMachines[i]))
                            output = commands.getoutput( "ssh %s@%s 'rsync -avzr --delete-before -e ssh  %s@%s:%s %s%s/' "  %( machineParameters.getUserNameForMachine( picklingMachine), picklingMachine,machineParameters.getUserNameForMachine( sourceMachines[i] ) , sourceMachines[i] , remotePxLogPath,  paths.STATSLOGS, sourceMachines[i] ) )
                            print "ssh %s@%s 'rsync -avzr --delete-before -e ssh  %s@%s:%s %s%s/' "  %( machineParameters.getUserNameForMachine( picklingMachine), picklingMachine,machineParameters.getUserNameForMachine( sourceMachines[i] ) , sourceMachines[i] , remotePxLogPath,  paths.STATSLOGS, sourceMachines[i] ) 
                            print output
                    else:
                        
                        for j in range(3):#do 3 times in case of currently turning log files.
                            remotePxLogPath = paths.getPXPathFromMachine(paths.PXLOG, sourceMachines[i], machineParameters.getUserNameForMachine( sourceMachines[i]))
                            print "le remote paths : ", remotePxLogPath
                            print                            
                            output = commands.getoutput( "rsync -avzr --delete-before -e ssh %s@%s:%s   %s%s/ " %( machineParameters.getUserNameForMachine( sourceMachines[i] ), sourceMachines[i] , remotePxLogPath,  paths.STATSLOGS, sourceMachines[i] ) )
                            print
                            print "*****************************"
                            print
                            print "rsync -avzr --delete-before -e ssh " + """%s@%s:%s   %s%s/"""  %( machineParameters.getUserNameForMachine( sourceMachines[i] ), sourceMachines[i] , remotePxLogPath,  paths.STATSLOGS, sourceMachines[i] )
                            print
                            print output   
                                    
                   
                if picklingMachine != LOCAL_MACHINE :#pickling to be done elsewhere,needs ssh             
                              
                    output = commands.getoutput( """ssh %s@%s 'python %spickleUpdater.py  -m %s -f rx --date "%s" '   """ %( machineParameters.getUserNameForMachine( picklingMachine ), picklingMachine, paths.STATSBIN,  sourceMachines[i], currentTimeInIsoFormat ) ) 
                    print "ssh %s@%s 'python %spickleUpdater.py  -m %s -f rx'   "  %( machineParameters.getUserNameForMachine( picklingMachine ), picklingMachine, paths.STATSBIN, sourceMachines[i] )
                    print output
                    
                    output = commands.getoutput( """ssh %s@%s 'python %spickleUpdater.py -m %s -f tx --date "%s" '  """( machineParameters.getUserNameForMachine( picklingMachine ), picklingMachine , paths.STATSBIN, sourceMachines[i], currentTimeInIsoFormat ) )
                    print "ssh %s@%s 'python %spickleUpdater.py -m %s -f tx'  "%( machineParameters.getUserNameForMachine( picklingMachine ), picklingMachine , paths.STATSBIN, sourceMachines[i] )
                    print output
                    
                    output = commands.getoutput( """%spickleSynchroniser.py -l %s -m %s  """%( paths.STATSTOOLS, machineParameters.getUserNameForMachine( picklingMachine ), picklingMachine ) )      
                    print "%spickleSynchroniser.py -l %s -m %s  " %( paths.STATSTOOLS, machineParameters.getUserNameForMachine( picklingMachine ), picklingMachine )
                    print output
                
                    
                else: # pickling is to be done locally. Log files may or may not reside elsewhere.
                    
                    output = commands.getoutput( """python %spickleUpdater.py -f rx -m %s --date "%s" """%( paths.STATSBIN, sourceMachines[i], currentTimeInIsoFormat ) )
                    print "python %spickleUpdater.py -f rx -m %s " %( paths.STATSBIN, sourceMachines[i] )
                    print output
                    
                    output = commands.getoutput( """python %spickleUpdater.py -f tx -m %s --date "%s" """  %(  paths.STATSBIN, sourceMachines[i], currentTimeInIsoFormat ) )
                    print "python %spickleUpdater.py -f tx -m %s " %( paths.STATSBIN, sourceMachines[i] )
                    print output
        
            sys.exit()            
            
        elif nbChildProcess!=0 and nbChildProcess%3 == 0 :
            while True:#wait on all non terminated child process'
                try:   #will raise exception when no child process remain.
                    pid, status = os.wait()
                except:
                    break
                
    while True:#wait on all non terminated child process'
        try:   #will raise exception when no child process remain.
            pid, status = os.wait( )
        except:
            break
                

        
def uploadGraphicFiles( parameters, machineParameters ):
    """
        @summary : Takes all the created daily graphics dedicated to clumbo and 
                   uploads them to the machines specified in the parameters. 
    """
    
    paths = StatsPaths()
    paths.setPaths()
    
    for uploadMachine in parameters.graphicsUpLoadMachines :
        output = commands.getoutput( "scp %s* %s@%s:%s " %( paths.STATSCOLGRAPHS, machineParameters.getUserNameForMachine(uploadMachine), uploadMachine, paths.PDSCOLGRAPHS   ) )
        
        print "scp %s* %s@%s:%s " %( paths.STATSCOLGRAPHS, machineParameters.getUserNameForMachine(uploadMachine),uploadMachine, paths.PDSCOLGRAPHS )
        print output


        
def transferToDatabaseAlreadyRunning():
    """
        @summary : Returns whether or not a transfer from pickle 
                   to rrd databases is allresdy running.
        
    """
    
    alreadyRuns = False 
    output = commands.getoutput( "ps -ax " ) 
    lines = output.splitlines()
    
    for line in lines:        
        if "transferPickleToRRD.py" in line and "R" in line.split()[2]:
            alreadyRuns = True
            break    
        
    return alreadyRuns
    

        
def updateDatabases( parameters, machineParameters, currentTimeInIsoFormat ):
    """
        @summary :  Updates all the required databases by transferring the
                    data found in the pickle files into rrd databases files.
                    
                    First transfers all the pickles into databases for all the clusters.
                    
                    Then combines all the data required by the different groups found 
                    within the config file.
       
        @param parameters: StatsConfigParameters instance containing 
                           the parameters found in the config file.
        
        @param machineParameters: MachineConfigParameters instance containing 
                                  the parameters found in the config file.
        
        @param currentTimeInIsoFormat : Time at which this program was originally 
                                        called.    
                                        
        @return : None
                                                
    """
    
    paths = StatsPaths()
    paths.setPaths()
    
    #Small safety measure in case another instance of the program is allready running.
    if transferToDatabaseAlreadyRunning() == False :
        
        for tag in parameters.machinesToBackupInDb :
             machines = machineParameters.getMachinesAssociatedWith(tag)             
             machines = str( machines ).replace( "[", "" ).replace( "]", "" ).replace( " ", "" )
             output = commands.getoutput( "%stransferPickleToRRD.py -m '%s' -e '%s' " %( paths.STATSBIN, machines, currentTimeInIsoFormat )  )
             print  "%stransferPickleToRRD.py -m '%s' " %( paths.STATSBIN, machines )
             print "output:%s" %output
        
        if parameters.groupParameters.groups != []:
            
            for group in  parameters.groupParameters.groups :
                                
                groupMembers = str( parameters.groupParameters.groupsMembers[group]).replace( "[", "" ).replace( "]", "" ).replace( " ", "" )
                groupMachines = str( parameters.groupParameters.groupsMachines[group] ).replace( "[", "" ).replace( "]", "" ).replace( " ", "" )                 
                groupProducts = str( parameters.groupParameters.groupsProducts[group] ).replace( "[", "" ).replace( "]", "" ).replace( " ", "" )
                groupFileTypes = str(parameters.groupParameters.groupFileTypes[group]).replace( "[", "" ).replace( "]", "" ).replace( " ", "" )
               
                output = commands.getoutput( "%stransferPickleToRRD.py -c '%s' -m '%s' -g '%s' -f %s -p '%s' -e '%s' " %( paths.STATSBIN, groupMembers, groupMachines, group, groupFileTypes, groupProducts, currentTimeInIsoFormat  ) )
                print   "%stransferPickleToRRD.py -c '%s' -m '%s' -g '%s' -f %s -p '%s' " %( paths.STATSBIN, groupMembers, groupMachines, group, groupFileTypes, groupProducts  )
                print output
 
 
 
def getGraphicsForWebPages( generalParameters, currentTimeInIsoFormat ):
    """
        @summary : Launchs the getGraphicsForWebPages.py
                   program. 
                   
        @param generalParameters      : StatsConfigParameters instance. 
        
        @param currentTimeInIsoFormat : Time at which this program was originally 
                                        called. 
        @return: None
                                        
    """
    
    for language in generalParameters.artifactsLanguages:
        graphicsGenerator = WebPageGraphicsGenerator( currentTimeInIsoFormat, language) 
        graphicsGenerator.generateAllForEverySupportedWebPagesBasedOnFrequenciesFoundInConfig()


    
def updateWebPages( generalParameters ):
    """
        @summary : Generates all the required web pages
                   based on the language parameters found within
                   the configuration files.
            
    """ 
    
    paths = StatsPaths()
    paths.setPaths()
    
    
    generalParameters = StatsConfigParameters()
    generalParameters.getAllParameters()
    
    otherLanguages = []

 
    generatorsTypes = [ DailyGraphicsWebPageGenerator, WeeklyGraphicsWebPageGenerator, MonthlyGraphicsWebPageGenerator, YearlyGraphicsWebPageGenerator, TotalsGraphicsWebPageGenerator   ]   
    
    for languagePair in generalParameters.webPagesLanguages :
        for generatorsType in generatorsTypes :
            generator = generatorsType( languagePair[0], languagePair[1] )
            generator.generateWebPage()
        
        topWebPageGenerator = TopWebPageGenerator(languagePair[0]) 
        topWebPageGenerator.generateTopWebPage()
        otherLanguages.append( languagePair[0] )
    
    try:
        while(1):
            otherLanguages.remove( generalParameters.mainApplicationLanguage )
    except:
        pass
    
    bottomWebPageGenerator = BottomWebPageGenerator(generalParameters.mainApplicationLanguage, otherLanguages )
    bottomWebPageGenerator.printWebPage()
    
    
    
def monitorActivities( configParameters, currentTime ):
    """
        @summary: Monitors all the activities that occured during 
        the course of this program. Report is sent out by mail
        to recipients specified in the config file.
        
        @param configParameters: StatsConfigParameters instance.
                               
        @param currenTime: currentTime in seconds since epoch format.
        
    """    
    
    paths = StatsPaths()
    paths.setPaths()
    
    updateManager = AutomaticUpdatesManager( configParameters.nbAutoUpdatesLogsToKeep, "monitoring")
    
    if updateManager.updateIsRequired(currentTime)  :  
         output = commands.getoutput( paths.STATSBIN + "statsMonitor.py '%s'" %( currentTime ) )
         print paths.STATSBIN + "statsMonitor.py"
         print output
         updateManager.addAutomaticUpdateToLogs( currentTime )
 
 
 
def needsToBeRun( frequency, currentTime ):        
    """
    
        @summary : This method is built to mimick the behavior of a crontab entry. 
                    
                   Entries will be judged to be needing to be run if the current time 
                   minus epoch is a multiple of the frequency that was asked in the 
                   parameters. This way we ensure that program are run at every 5 hours
                   for example at not at every hour of the day where the hour number is a
                   5 multiple.
                   
                   Also this prevents us from having to save the time of the last time a 
                   certain program has ran, wich could become troublesome if this program 
                   did not run for a while. 
        
        @param frequency: Frequency at wich a certain program needs to be run.
                          MUST be of the array type and of the the following form: 
                          { value : unitOfTime  } 
       
       @param currentTime: CurrentTime in seconds since epoch format.
       
       @return: Returns wheter a certain program needs to be run or not.
        
    """
    
    needsToBeRun = False     
    
    value = frequency.keys()[0]
     
        
    if frequency[value] == "minutes":
       value = float(value) 
       currentTime = currentTime - ( currentTime % (60) )
       
       if int(currentTime) % int(value*60) == 0:
            needsToBeRun = True    
         
    elif frequency[value] == "hours":      
        value = float(value) 
        currentTime = currentTime - ( currentTime % (60*60) )
        
        if int(currentTime) % int(value*60*60) == 0:
            needsToBeRun = True 
    
    elif frequency[value] == "days":     
        value = float(value)     
        currentTime = currentTime - ( currentTime % (60*60) )
        
        int(currentTime) % int(value*60*60*24)
        if int(currentTime) % int(value*60*60*24) == 0:
            needsToBeRun = True 
    
    elif frequency[value] == "months":
        value = float(value) 
        
        currentMonth = time.strftime( "%m", time.gmtime( currentTime ) )
        if int(currentTime) % int(value) == 0:
            needsToBeRun = True 
    
    return needsToBeRun
    
    
    
def cleanUp( configParameters, currentTime, daysOfPicklesToKeep ):
    """
    
        @summary: Based on current time and frequencies contained
                  within the time parameters, we will run 
                  the cleaners that need to be run.       
                            
        @param configParameters: StatsConfigParameters instance.
                               
        @param currenTime: currentTime in seconds since epoch format.
                                  
    """     
    
    paths = StatsPaths()
    paths.setPaths()
    
    updateManager = AutomaticUpdatesManager(configParameters.nbAutoUpdatesLogsToKeep, "picklecleaner")
    
    if updateManager.updateIsRequired(currentTime) :
        
        output = commands.getoutput( paths.STATSTOOLS + "pickleCleaner.py %s" %int(daysOfPicklesToKeep) )
        print paths.STATSTOOLS + "pickleCleaner.py" + " " + str( daysOfPicklesToKeep )
        updateManager.addAutomaticUpdateToLogs( currentTime )
        
    updateManager = AutomaticUpdatesManager(configParameters.nbAutoUpdatesLogsToKeep, "generalCleaner")    
    
    if updateManager.updateIsRequired(currentTime) :
        commands.getstatusoutput( paths.STATSTOOLS + "clean_dir.plx" + " " + paths.STATSETC + "clean_dir.conf"   )
        print paths.STATSTOOLS + "clean_dir.plx" + " " + paths.STATSETC + "clean_dir.conf" 
        updateManager.addAutomaticUpdateToLogs( currentTime )
    
    
def backupRRDDatabases( configParameters, currentTime, nbBackupsToKeep ):
    """
    
        @summary: Based on current time and frequencies contained
                  within the time parameters, we will backup the databases
                  only if necessary.       
                            
        @param configParameters: StatsConfigParameters instance.
                               
        @param currenTime: currentTime in seconds since epoch format.
                                  
    """  
    
    paths = StatsPaths()
    paths.setPaths()    
    
    updateManager = AutomaticUpdatesManager(configParameters.nbAutoUpdatesLogsToKeep, "dbBackups" )
    
    if updateManager.updateIsRequired( currentTime )  :
        commands.getstatusoutput( paths.STATSTOOLS + "backupRRDDatabases.py" + " " + str( int(nbBackupsToKeep)) )             
        print paths.STATSTOOLS + "backupRRDDatabases.py" + " " + str(nbBackupsToKeep)
        updateManager.addAutomaticUpdateToLogs( currentTime )


def saveCurrentMachineParameters( machineParameters  ):
    """
        @summary : Saves the current machineParameters into 
                   the /data/previousMachineParameters file. 
        
        @param machineParameters: Machine parameters to save.
        
    """
    
    paths = StatsPaths()
    paths.setPaths()
    
    if not os.path.isdir( os.path.dirname( paths.STATSPREVIOUSMACHINEPARAMS ) ):
        os.makedirs( os.path.dirname(paths.STATSPREVIOUSMACHINEPARAMS) )
    
    CpickleWrapper.save( machineParameters, paths.STATSPREVIOUSMACHINEPARAMS)
        


def getMachineParametersFromPreviousCall() :
    """
        @summary: Gets the machine parameters that are 
                  saved in data/previousMachineParameters.   
        
        @return: Returns the saved machine parameters. 
    
    """
    
    paths = StatsPaths()
    paths.setPaths()
    
    previousMachineParams = None
    if os.path.isfile( paths.STATSPREVIOUSMACHINEPARAMS ):
        previousMachineParams = CpickleWrapper.load( paths.STATSPREVIOUSMACHINEPARAMS )
    
    return  previousMachineParams  
      
      
        
def getMachinesTagsNeedingUpdates( configParameters, machineParameters ):
    """
        @summary : Verifies every machine tags to see if a
                   member of that group has been renamed 
                   since the last cront job.
        
        @param machineParameters:  Current machine parameters 
                                  found within the config files.
                                  
        @return: List of tags needing updates.
                 Will return an empty list if nothing needs to be updated.
                
                 Will return None if no previous configs were saved.                                     
    
    
    """  
    
    tagsNeedingupdates = []
    
    previousParameters = getMachineParametersFromPreviousCall()
    
    if previousParameters == None:     
        tagsNeedingupdates = None
    else:
        print previousParameters.machinesForMachineTags
        for tag in configParameters.sourceMachinesTags:
            try:
                if previousParameters.getMachinesAssociatedWith( tag ) != machineParameters.getMachinesAssociatedWith( tag ):
                    tagsNeedingupdates.append( tag )
            except:
                pass    
            
    return tagsNeedingupdates

   
    
def updateFilesAssociatedWithMachineTags( tagsNeedingUpdates, machineParameters ):   
    """
        @summary : For all the tags for wich 
                   a machine was change we rename all the 
                   files associated with that tag.
        
        @param tagsNeedingUpdates: List of tags that have been modified 
                                   since the last call.
                                             
    
    """
    
    paths = StatsPaths()
    paths.setPaths()
    
    previousParameters = getMachineParametersFromPreviousCall()
    
    for tag in tagsNeedingUpdates:
        previousCombinedMachineNames = ""
        previousCombinedMachineNames = previousCombinedMachineNames.join( [ x for x in previousParameters.getMachinesAssociatedWith( tag ) ] )
        
        currentCombinedMachineNames = ""
        currentCombinedMachineNames = currentCombinedMachineNames.join( [ x for x in machineParameters.getMachinesAssociatedWith( tag ) ]) 
        
        output = commands.getoutput( "%sfileRenamer.py -o %s  -n %s --overrideConfirmation" %( paths.STATSTOOLS, previousCombinedMachineNames, currentCombinedMachineNames  ) )
        print "%sfileRenamer.py -o %s  -n %s --overrideConfirmation" %( paths.STATSTOOLS, previousCombinedMachineNames, currentCombinedMachineNames  )
        print output 

    
        
def updateCsvFiles():
    """    
        
        @summary : Runs the csv file update utility.
        
    """
    
    paths = StatsPaths()
    paths.setPaths()    
    output = commands.getoutput( "%sgetCsvFilesforWebPages.py" %paths.STATSWEBPAGESGENERATORS )
    
    
    
def  setGlobalLanguageParameters():
    """
        @summary : Sets up all the needed global language 
                   tranlator so that it can be used 
                   everywhere in this program.
        
        @Note    : The scope of the global _ function 
                   is restrained to this module only and
                   does not cover the entire project.
        
        @return: None
        
    """
    
    global _ 
    
    _ = LanguageTools.getTranslatorForModule( CURRENT_MODULE_ABS_PATH )      
    
    
    
def main():
    """
        @summary : Gets all the parameters from config file.
                   Updates pickle files.
                   Generates all the required graphics.
                   Generates therwuired csv files.
                   Updates the different web pages.
                   Updates the desired databases.                    
                   Uploads graphics to the required machines. 
                   Monitors the result of all the activities.
    
    """
    
    
    if GeneralStatsLibraryMethods.processIsAlreadyRunning( "pxStatsStartup" ) == False:
        
        setGlobalLanguageParameters()
        
        GeneralStatsLibraryMethods.createLockFile( "pxStatsStartup" )
        
        currentTime = time.time()
        currentTimeInIsoFormat = StatsDateLib.getIsoFromEpoch( currentTime )
                
        generalParameters = StatsConfigParameters()
        
        generalParameters.getAllParameters()
                                                                    
        machineParameters = MachineConfigParameters()
        machineParameters.getParametersFromMachineConfigurationFile()
        
        validateParameters( generalParameters, machineParameters, None  )
        
        tagsNeedingUpdates = getMachinesTagsNeedingUpdates( generalParameters, machineParameters )
        if tagsNeedingUpdates == None : #no previous parameter found
            saveCurrentMachineParameters( machineParameters  )
        elif tagsNeedingUpdates != [] :
            updateFilesAssociatedWithMachineTags( tagsNeedingUpdates, machineParameters )
            saveCurrentMachineParameters( machineParameters  )
               
                
        updatePickles( generalParameters, machineParameters, currentTimeInIsoFormat )
        
        updateDatabases( generalParameters, machineParameters, currentTimeInIsoFormat )
        
        backupRRDDatabases( generalParameters, currentTimeInIsoFormat, generalParameters.nbDbBackupsToKeep )
        
        #updateCsvFiles( )
        
        getGraphicsForWebPages( generalParameters, currentTimeInIsoFormat )
                    
        updateWebPages( generalParameters )
        
        #uploadGraphicFiles( generalParameters, machineParameters )
     
        cleanUp( generalParameters , currentTimeInIsoFormat, generalParameters.daysOfPicklesToKeep )
    
        monitorActivities(  generalParameters, currentTimeInIsoFormat )
        
        updateManager = AutomaticUpdatesManager( generalParameters.nbAutoUpdatesLogsToKeep, "pxStatsStartup" )
        updateManager.addAutomaticUpdateToLogs( currentTimeInIsoFormat )
        
        GeneralStatsLibraryMethods.deleteLockFile( "pxStatsStartup" )
        
        print _( "Finished." )
    
    else:
        print _( "Error. An other instance of pxStatsStartup is allready running." )
        print _( "Only one instance of this software can be run at once."  )
        print _( "Please terminate the other instance or wait for it to end it's execution" )
        print _( "before running this program again." )
        print _( "Program terminated." )
        sys.exit()
    
    
    
if __name__ == "__main__":
    main()
