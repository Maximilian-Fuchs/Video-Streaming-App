#!/bin/bash
##
## entrypoint for the docker images

if [ ! -f /.dockerenv ] && [ ! -f /.dockerinit ]; then
	echo "WARNING: this script should be only run inside docker!!"
	exit 1
fi

if [ ! -z $gid ] && [ ! -z $uid ]; then
	groupmod -g $gid core
	usermod -u $uid -g $gid core

	# check if homedir is mounted
	if grep -q '/home/core' /proc/mounts; then
		# homedir is mounted into the docker so don't touch the ownership of the files
		true
	else
		# fixup for changed uid and gid
		chown -R core:core /home/core
	fi
fi

function startCore() {
	echo "Starting Voctomix CORE"
	if [ -x /bin/gosu ]; then
		gosu core app.py -v
	else
		echo "no gosu found..."
		exec su -l -c "app.py -v" core
	fi
}

function isVideoMounted() {

}

function startGui() {

}

function listExamples() {

}

function runExample() {

}

function usage() {
	echo "Usage: $0 <cmd>"
	echo "help			- this text"
	echo "core 			- starts voctomix gore"
	echo "gui 			- starts the voctomix GUI"
	echo "examples	 	- lists the example scripts"
	echo "bash			- run interactive bash"
	echo "scriptname.py - starts the example script named 'scriptname.py' "
}

if [ -z $1 ]; then
	usage
	exit
fi

case $1 in
	help )
		usage
		;;
	examples )
		listExamples
		;;
	gui )
		startGui
		;;
	core )
		startCore
		;;
	bash )
		shift
		bash $@
		;;
	* )
		runExample $1
		;;
esac
