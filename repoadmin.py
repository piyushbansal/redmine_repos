#!/usr/bin/python
import os, commands, json,sys

""" REQUIREMENTS : A directory system such as /labs/projectname/git , /labs/projectname/svn, /labs/projectname/bazaar already existing
		 : svn ,git, bzr, python  preinstalled 	"""

LAB_HOME='/labs/'
DEBUG=False


#----------------------------------------------------------------------------------------------------------------------#


# The function run_command takes as input ,a string ,and executes it as a command . For example , if it 	#
# is given a sting { "ls" + "-" + "la" } then it would concatenate it and execute ls -la in the command 	#
# line . This is achieved by usage of a built in method declared in module commands called 			#
# commands.getstatusoutput(command).										#


# USED TO 		: To execute a string in shell.
# USAGE   		: One argument, essentially a string.
# OUTPUT  		: Returns a 2-tuple (status, output) 
# VARIABLES USED	: response [ 2-tuple ] , command [ string ]

def run_command(command=None):
    if command is None:
        return ['1',"error"]
    response = commands.getstatusoutput(command)
    if DEBUG:
	print "command is "+command
        print response[1]
    return response

#----------------------------------------------------------------------------------------------------------------------#


# The function response_gen is used to print the response to the screen, it has mainly debugging benefits	#
# For example , if provided with a dictionary that has various datatypes, it would convert all those datatypes  #
# into standard json string format, and can be used later on. json.dumps() is a built in method in python's 	#
# json module , that takes a dictionary and converts it into json strings.					#


# USED TO		: To generate response of the overall process and convert the dictionary datatypes into json string.
# USAGE			: One agrument, essentially a dictionary (hash)
# OUTPUT		: The dictionary with all datatypes changed into json string format.
# VARIABLES USED	: response_obj [ dictionary ], response [ json string formatted dictionary ]

def response_gen(response_obj):
    response = None
    try:
        response = json.dumps(response_obj)
    except e:
        print "unable to process to json "+ e
    return response


#----------------------------------------------------------------------------------------------------------------------#


# The function svncreate is used to create a svn repository , at /labs/labid/svn/repo  , here labid would be   	 #
# an argument , which would also be the name of the project in redmine_repos plugin. Basically we create a 	 #
# svn repository and in it copy contents of ldk folder ( lab development kit) , Perform svn add * , and commit	 # 
# run_command fucntion has been used a lot here, whcih has been defined above already				 #


# USED TO 		: To create a svn repository
# USAGE			: Three arguments,repo_location, labid - project name (string) , repo - repository name (string)
# OUTPUT		: A dictionary with status variable mapped to 1 and summary
# VARIABLES USED	: labid [string], repo [string]

def svncreate(repo_location,labid,repo):
	run_command('cd '+ LAB_HOME+labid +'/'+'svn'+'/' + ';svnadmin create '+repo+' ; chmod -R g+w '+repo)[1]
        run_command('mkdir -p /tmp/ldk')[1]
        run_command('svn co file://'+repo_location+' /tmp/ldk')[1]
        run_command('cp -r ldk/* /tmp/ldk')[1]
        run_command('cd /tmp/ldk ; svn add * ;svn commit -m "LDK committed"')[1]
        run_command('cd /tmp; rm -rf /tmp/ldk')[1]
        run_command('chmod g+w '+repo_location+'/db/rep-cache.db')
        return {'status' : 1 ,'summary' : 'Repo initialized with ldk' }


#----------------------------------------------------------------------------------------------------------------------#


	
# The function gitcreate is used to create a git repository , at /labs/labid/git/repo  , here labid would be   	 #
# an argument , which would also be the name of the project in redmine_repos plugin. Basically we create a 	 #
# git repository and in it copy contents of ldk folder ( lab development kit) , Perform git add * , and commit	 # 
# run_command fucntion has been used a lot here, whcih has been defined above already				 #


# USED TO 		: To create a git repository
# USAGE			: Three arguments,repo_location, labid - project name (string) , repo - repository name (string)
# OUTPUT		: A dictionary with status variable mapped to 1 and summary
# VARIABLES USED	: labid [string], repo [string]

def gitcreate(repo_location,labid,repo):
	run_command('cd '+ LAB_HOME+labid +'/'+'git'+ ' ;git init --bare '+repo+' ; chmod -R g+w '+repo)[1]
        run_command('mkdir -p /tmp/ldk')[1]
        run_command('git clone file://'+repo_location+' /tmp/ldk')[1]
        run_command('cp -r ldk/* /tmp/ldk')[1]
        run_command('cd /tmp/ldk ; git add * ;git commit -m "LDK committed"')[1]
        run_command('cd /tmp; rm -rf /tmp/ldk')[1]
        run_command('chmod g+w '+repo_location+'/db/rep-cache.db')
        return {'status' : 1 ,'summary' : 'Repo initialized with ldk' }


#----------------------------------------------------------------------------------------------------------------------#


# The function bazaarcreate is used to create a bazaar repository , at /labs/labid/bazaar/repo  , here labid     #
# is an argument , which would also be the name of the project in redmine_repos plugin. Basically we create a 	 #
# bazaar repository and in it copy contents of ldk folder ( lab development kit) , Perform bzr add * , and 	 # 
# commit . "run_command" function has been used a lot here, whcih has been defined above already		 #


# USED TO 		: To create a bazaar repository
# USAGE			: Three arguments, repo_location,labid - project name (string) , repo - repository name (string)
# OUTPUT		: A dictionary with status variable mapped to 1 and summary
# VARIABLES USED	: repo_location [string], labid [string], repo [string]

def bazaarcreate(repo_location,labid,repo):
	run_command('cd '+ LAB_HOME+labid+'/'+'bazaar' + ' ;bzr init-repo '+repo+' ; chmod -R g+w '+repo)[1]
       	run_command('mkdir -p /tmp/ldk')[1]
       	run_command('bzr pull file://'+repo_location+' /tmp/ldk')[1]
       	run_command('cp -r ldk/* /tmp/ldk')[1]
       	run_command('cd /tmp/ldk ; bzr add * ;bzr commit -m "LDK committed"')[1]
       	run_command('cd /tmp; rm -rf /tmp/ldk')[1]
       	run_command('chmod g+w '+repo_location+'/db/rep-cache.db')
       	return {'status' : 1 ,'summary' : 'Repo initialized with ldk' }


#----------------------------------------------------------------------------------------------------------------------#


# The function create calls either of svncreate,gitcreate or bazaarcreate depending on typeofrepo, it additionally #
# checks if repo path exists already or not , by running a function inbuilt in the python os module os.path.exists #
# if it returns true then funtions returns a dictionary with status mapped to 0 and summary that repo exists       #
# otherwise calls either of the three functions. 								   #


# USED TO 		: To select which [repo]create function to call according to typeofrepo			   
# USAGE			: three arguments, typeofrepo , labid - project name, repo - repository name
# OUTPUT		: Same as [repo]create functions
# VARIABLES USED	: repo_location - full path to server's repository location [string] , rest are same as [repo]create functions.

def create(typeofrepo,labid,repo):
            repo_location = LAB_HOME+labid+'/'+typeofrepo+'/'+repo
            if os.path.exists(LAB_HOME+labid+'/'+typeofrepo+'/'+repo):		
                return {'status' : 0 , 'summary' : 'repo exists'}
	    elif typeofrepo == 'svn':
			return svncreate(repo_location,labid,repo)
	    elif typeofrepo == 'git':
	    		return gitcreate(repo_location,labid,repo)
            elif typeofrepo == 'bazaar':
	    		return bazaarcreate(repo_location,labid,repo)


#----------------------------------------------------------------------------------------------------------------------#


# The function is used to delete the repository completely , rest of the things about it are same as create function #

def discard(typeofrepo,labid,repo):
	run_command('rm -rf '+LAB_HOME+labid+'/'+typeofrepo+'/'+repo)
	return {'status' : 1,'summary' : 'Repo removed' }


#----------------------------------------------------------------------------------------------------------------------#


# The main function block, where we pass arguments to create or discard functions as system arguments (params) .     #
# If the first system argument happens to be 'add', then create function is called with rest of the system arguments #
# as arguments to create function. Same is the case with discard function , the only difference being the first system
# argument , if it happens to be 'discard', then the repository is deleted.					     #


# VARIABLES USED 	: response_obj , which is output of create/discard function, look at create/discard for more info
#			: params - system arguments
		
if __name__ == '__main__':
    params = sys.argv
    if params[1] == 'add':
    	response_obj = create(params[2],params[3],params[4])
    elif params[1] == 'discard': 
	response_obj = discard(params[2],params[3],params[4])
    print response_gen(response_obj)
