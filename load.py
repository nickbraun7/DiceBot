#!/usr/bin/env python
# -*- coding: utf-8 -*-

def token(): #load discord token
    with open("discord_token.txt", "r") as fp:
        token = fp.read()
    return token
