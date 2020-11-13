# Modules
import inspect
import importlib

from os import listdir
from os.path import abspath

from .colors import colored
from .types import ChatterCommand

# Get a list of commands
def load_commands(manager):

    commands = {}

    for command in listdir(abspath("chatter/cmds")):

        # Try to load the module
        if not command.endswith(".py"): continue  # Prevent pycache and other things
        
        try:

            m = importlib.import_module(f"chatter.cmds.{command[:-3]}")

            # Loop through our functions
            for name, f in inspect.getmembers(m, inspect.isfunction):

                # Fetch the arguments
                args = []

                if f.__doc__:

                    if "|" in f.__doc__:

                        args = f.__doc__.split("| ")[1].split(" ")

                # Load the command
                commands[f.__name__] = {
                    "args": args,
                    "function": f
                }

        except ImportError:

            # This is alright if it fails.
            pass

    return commands

# Main function
def run_command(manager, author, command):

    # Link our commands to the core
    try: manager.commands
    except AttributeError: manager.commands = load_commands(manager)

    # Command parsing
    args = command.split(" ")[1:]
    command = command.split(" ")[0][1:]

    # Command doesn't exist
    if not command in manager.commands:

        return manager.relay_message(colored(f"No command named '{command}'.", "red"))

    # Identify our command and check args
    command = manager.commands[command]

    if len(command["args"]) > len(args):

        return manager.relay_message(colored(f"Missing arguments: {command['args']}.", "red"))

    # Run the command
    command["function"](manager, author, args)
