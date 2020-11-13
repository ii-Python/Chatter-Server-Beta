# Color dictionary
colors = {
  "red": "\033[91m",
  "green": "\033[92m",
  "cyan": "\033[36m",
  "blue": "\033[94m",
  "yellow": "\033[93m",
  "reset": "\033[0m"
}

# The main function
def colored(text, color):

    """This function returns a string formatted with ascii color codes."""

    return colors[color] + text + colors["reset"]
