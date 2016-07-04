#!/usr/bin/env bash

source run_or_fail.sh

run_or_fail "Fail to restart process $1" sudo restart $1