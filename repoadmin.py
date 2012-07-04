#!/usr/bin/python

LAB_HOME='/labs/'
DEBUG=False
def run_command(command=None):
    import commands
    if command is None:
        return ['1',"error"]
# commands .getstatusoutput returns an array with two values , first one is status and second one is the result of command.
    response = commands.getstatusoutput(command)
    if DEBUG:
	print "command is "+command
        print response[1]
    return response

def request_parser(param):
    import json
    request = None
    try:
        request = json.loads(param)
    except e:
        print "Error parsing "+ e
    return request

def response_gen(response_obj):
    import json
    response = None
    try:
        response = json.dumps(response_obj)
    except e:
        print "unable to process to json "+ e
    return response



def create(typeofrepo,labid,repo):
	if typeofrepo == 'svn':
            # check if the repo exists 
            import os
            if os.path.exists(LAB_HOME+labid+'/'+'svn'+'/'+repo):		
                return {'status' : 0 , 'summary' : 'repo exists'}
		# create the repo 
            repo_location = LAB_HOME+labid+'/'+'svn'+'/'+repo
		#print repo_location
            run_command('cd '+ LAB_HOME+labid +'/'+'svn'+'/' + ';svnadmin create '+repo+' ; chmod -R g+w '+repo)[1]
            run_command('mkdir -p /tmp/ldk')[1]
            run_command('svn co file://'+repo_location+' /tmp/ldk')[1]
            run_command('cp -r ldk/* /tmp/ldk')[1]
            run_command('cd /tmp/ldk ; svn add * ;svn commit -m "LDK committed"')[1]
            run_command('cd /tmp; rm -rf /tmp/ldk')[1]
		# fix repo cache group write issue
            run_command('chmod g+w '+repo_location+'/db/rep-cache.db')
            return {'status' : 1 ,'summary' : 'Repo initialized with ldk' }
	elif typeofrepo == 'git':
            # check if the repo exists 
            import os
            if os.path.exists(LAB_HOME+labid+'/'+ 'git'+'/'+repo):		
                return {'status' : 0 , 'summary' : 'repo exists'}
		# create the repo 
            repo_location = LAB_HOME+labid+'/'+ 'git'+'/'+repo
#### here we are going into the directory /labs/"labid"/ and initialising an empty git repo there.
            run_command('cd '+ LAB_HOME+labid +'/'+'git'+ ' ;git init --bare '+repo+' ; chmod -R g+w '+repo)[1]
#### we create a folder /tmp/ldk 
            run_command('mkdir -p /tmp/ldk')[1]
#### here we clone all the files at repo_location to /tmp/ldk
            run_command('git clone file://'+repo_location+' /tmp/ldk')[1]
#### now we copy contents of ldk/ into /tmp/ldk
            run_command('cp -r ldk/* /tmp/ldk')[1]
#### cd into /tmp/ldk add new changes , commit and remove the temporary repo.
            run_command('cd /tmp/ldk ; git add * ;git commit -m "LDK committed"')[1]
            run_command('cd /tmp; rm -rf /tmp/ldk')[1]
	# fix repo cache group write issue
            run_command('chmod g+w '+repo_location+'/db/rep-cache.db')
            return {'status' : 1 ,'summary' : 'Repo initialized with ldk' }
	elif typeofrepo == 'bazaar':
            # check if the repo exists 
            import os
            if os.path.exists(LAB_HOME+labid+'/'+'bazaar'+'/'+repo):		
                return {'status' : 0 , 'summary' : 'repo exists'}
	# create the repo 
            repo_location = LAB_HOME+'/'+labid+'/'+'bazaar'+'/'+repo
	#print repo_location
            run_command('cd '+ LAB_HOME+labid+'/'+'bazaar' + ' ;bzr init-repo '+repo+' ; chmod -R g+w '+repo)[1]
            run_command('mkdir -p /tmp/ldk')[1]
####################################
#since a developer can switch from one branch to another while developing in case of bazaar , we woild have to use bzr merge first and then bzr pull., so uncertainity :)
####################################
            run_command('bzr pull file://'+repo_location+' /tmp/ldk')[1]
##############
#assumming that the developer never switched branch
##############
            run_command('cp -r ldk/* /tmp/ldk')[1]
            run_command('cd /tmp/ldk ; bzr add * ;bzr commit -m "LDK committed"')[1]
            run_command('cd /tmp; rm -rf /tmp/ldk')[1]
	# fix repo cache group write issue
            run_command('chmod g+w '+repo_location+'/db/rep-cache.db')
            return {'status' : 1 ,'summary' : 'Repo initialized with ldk' }
        
def discard(typeofrepo,labid,repo):
	if typeofrepo=='svn':
    		run_command('rm -rf '+LAB_HOME+labid+'/'+'svn'+'/'+repo)
    		return {'status' : 1 ,'summary' : 'Repo removed' }
	elif typeofrepo=='git':
		run_command('rm -rf '+LAB_HOME+labid+'/'+'git'+'/'+repo)
		return {'status' : 1,'summary' : 'Repo removed' }
	elif typeofrepo=='bazaar':
		run_command('rm -rf '+LAB_HOME+labid+'/'+'bazaar'+'/'+repo)
		return {'status' : 1,'summary' : 'Repo removed' }

		


if __name__ == '__main__':
    import sys
    params = sys.argv
    if params[1] == 'add':
# calling function create
    	response_obj = create(params[2],params[3],params[4])
# calling function discard
    elif params[1] == 'discard': 
	response_obj = discard(params[2],params[3],params[4])
# respose_gen function called
    print response_gen(response_obj)
