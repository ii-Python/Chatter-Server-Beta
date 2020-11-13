######################################################
#                                                    #
#  Chatter - a secure way to chat over the internet  #
#            Copyright 2020, iiPython                #
#                                                    #
######################################################

# Chatter uses a custom method of transmitting data via TCP packets.
# This method is called triport and utilizes all-caps words to signify events.
# 
# Some examples of this protocol:
# NAME-REQUESTED
# AUTH:1234
# BANNED
# ...
# 
# It's rather simple, but works incredibly well.
# Before attempting to replicate any of this code, it is recommended to know
# a decent chunk of these event names. This rule also applies to the client
# as it uses the same protocol.
#
# Please note: Chatter will only use a local config.json file since it's meant to be privacy based.
# It is highly recommended to run Chatter off of a USB drive or other removable media source.

# Modules
from sys import argv
from chatter import ChatterServer

# Initialization
chatter = ChatterServer(argv)
chatter.start()
