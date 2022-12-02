#!/bin/bash

base_path="$(cat vars.yml | grep base_path | awk '{print $2}')"

rm -rf $base_path

