# Modules
from ..colors import colored

# Command function
def kick(manager, author, args):

    """Removes a user from the server temporarily | name"""

    # Check for admin
    if not author.is_admin():

        return manager.relay_message(colored("You need to be a server administrator to use this command.", "red"))    

    # Load the user from our clients
    name = args[0]
    user = manager.locate_user(name)

    if not user:

        return manager.relay_message(colored("No client has that name.", "red"))

    elif user.is_admin():

        return manager.relay_message(colored(f"{user.name} is an administrator and cannot be kicked.", "red"))

    user.disconnect()
    manager.relay_message(f"Successfully kicked {user.name} from the server.")
