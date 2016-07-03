#!/usr/bin/env bash
# helper method for providing error messages for a command
run_or_fail() {
  # Declared as local variable.
  local explanation=$1
  # The positional parameters are shifted to the left by this number, N.
  # 第一个参数被抛弃
  shift 1
  # $@ is all of the parameters passed to the script.
  "$@"
  # $? is the return code (status code) of the last command or script executed.
  # 0 == success, any other number means a failure
  if [ $? != 0 ]; then
    # 1>&2 : Redirects stdout to stderr .
    echo ${explanation} 1>&2
    exit 1
  fi
}
