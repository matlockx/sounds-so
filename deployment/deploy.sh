#!/usr/bin/env bash

ansible-playbook sso-platform.yml -i ./inventory --ask-vault-pass -u root
