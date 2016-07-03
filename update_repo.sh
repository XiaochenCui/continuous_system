#!/bin/bash

# The source command can be used to load any functions file into the
# current shell script or a command prompt.
source run_or_fail.sh
# delete previous id 
rm -f .commit_id

# go to repo and update it to given commit
run_or_fail "Repository folder not found!" pushd $1 1> /dev/null
run_or_fail "Could not reset git" git reset --hard HEAD

# get the most recent commit
COMMIT=$(run_or_fail "Could not call 'git log' on repository" git log -n1)
if [ $? != 0 ]; then
  echo "Could not call 'git log' on repository"
  exit 1
fi
# get its id
COMMIT_ID=`echo ${COMMIT} | awk '{ print $2 }'`

# update the repo
run_or_fail "Could not pull from repository" git pull

# get the most recent commit
COMMIT=$(run_or_fail "Could not call 'git log' on repository" git log -n1)
if [ $? != 0 ]; then
  echo "Could not call 'git log' on repository"
  exit 1
fi
# get its id
NEW_COMMIT_ID=`echo ${COMMIT} | awk '{ print $2 }'`

# if the id changed, then write it to a file
if [ ${NEW_COMMIT_ID} != ${COMMIT_ID} ]; then
  # Redirect the standard out to the /dev/null.
  # popd : Remove the top entry from the directory stack, and cd to the new top directory.
  # 1> /dev/null : Redirects stdout to /dev/null .
  popd 1> /dev/null
  echo ${NEW_COMMIT_ID} > .commit_id
fi
