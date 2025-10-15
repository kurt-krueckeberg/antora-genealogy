#!/usr/bin/env bash
rm -rf public
npx antora local-playbook.yml 
cp  fonts/* public/_/font/
