#! /bin/bash
#
# test.sh

gvfs-set-attribute test.sh -t stringv metadata::emblems new
nautilus . &
