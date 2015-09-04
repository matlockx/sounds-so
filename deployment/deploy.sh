#!/usr/bin/env bash

ansible-playbook sso-backend.yml -i ./inventory --ask-vault-pass -u root
