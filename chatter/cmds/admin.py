# Modules
from ..colors import colored

# Command function
def admin(manager, author, args):

    """Turns a user into a server admin | name"""

    # Check for admin
    if not author.is_admin():

        return manager.relay_message(colored("You need to be a server administrator to use this command.", "red"))    

    # Load the user from our clients
    name = args[0]
    user = manager.locate_user(name)

    if not user:

        return manager.relay_message(colored("No client has that name.", "red"))

    elif user.is_admin() and manager.admins:

        return manager.relay_message(colored(f"{user.name} is already a server administrator.", "red"))

    user.make_admin()

    manager.relay_message(f"Successfully made {user.name} a server administrator.")
