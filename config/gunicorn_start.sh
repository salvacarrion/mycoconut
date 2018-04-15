#!/bin/bash

NAME="coconut"                                                  # Name of the application
USER=salvacarrion                                              # the user to run as
# GROUP=webapps                                                # the group to run as
NUM_WORKERS=3                                                  # how many worker processes should Gunicorn spawn
TIMEOUT=120                                                    # Seconds before the timeout error
DJANGO_SETTINGS_MODULE=mycoconut.settings                         # which settings file should Django use
DJANGO_WSGI_MODULE=mycoconut.wsgi                                 # WSGI module name
DJANGODIR=/home/salvacarrion/Coconut/mycoconut                     # Django project directory
VENVDIR=/home/salvacarrion/Coconut/venv-coconut/bin/activate     # virtualenv directory
SOCKFILE=/home/salvacarrion/Coconut/mycoconut/run/gunicorn.sock    # we will communicte using this unix socket
LOGSFILE=/home/salvacarrion/Coconut/mycoconut/logs/gunicorn.log    # logs file


echo "Starting $NAME as `whoami`"

# Activate the virtual environment
source $VENVDIR
cd $DJANGODIR

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --user=$USER \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=$LOGSFILE