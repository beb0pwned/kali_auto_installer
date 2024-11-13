import os

# Define colors for output
GREEN = "\033[92m"
RED = "\033[91m"
TEAL = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


banner = f"""{RED}
 _ __      _  _  ___               
| / / ___ | |<_>| | '_ _  ___  _ _ 
|  \\ <_> || || || |-| | |/ ._>| '_>
|_\\_\\<___||_||_||_| `_. |\\___.|_|  
                    <___'          {RESET}
        {TEAL}by beb0pwned{RESET}
"""

# Tools and wordlists to be installed
tools = [
    "nmap",
    "curl",
    "aircrack-ng",
    "sqlmap",
    "hydra",
    "medusa",
    "hashcat",
    "john",
    "bettercap",
    "ffuf",
    "dirb",
]

snap_tools = [
    'metasploit-framework',
    'feroxbuster',
]

raw_wordlists = [
    "seclists",
    "PayloadsAllTheThings"
]

git_wordlists = [
            'git clone https://github.com/danielmiessler/SecLists.git',
            'git clone https://github.com/swisskyrepo/PayloadsAllTheThings.git',
             ]

def packages():
    """
    Displays the list of tools and wordlists to be installed and asks for user confirmation.
    """
    print("This will install the following packages:")
    total = 0

    # Print Tools
    for i, tool in enumerate(tools):
        print(f"{i+1}) {tool}")
        total += 1

    # Print tools that need to be downloaded with snap
    for i, tool in enumerate(snap_tools):
        print(f"{i+1+total}) {tool}")
        total += 1

    #Print Wordlists
    for i, wordlist in enumerate(raw_wordlists):
        print(f"{i+1+total}) {wordlist}")
    
    print("")
    choice = input("Do you want to continue? Y/N: ").lower()

    return choice


def check_directories(path='/opt/wordlists'):
    """
    Iterates through the names of directories in the specified path and checks to see if they already exist
    """
    existing_wordlists = set()
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                existing_wordlists.add(item.lower())

    except Exception as e:
        print(f"Error: {e}")

    except PermissionError:
        print(f"{RED}Permission denied to access {path}.{RESET}")
    return existing_wordlists


def lowercase_directories(path=''):
    """
    Iterates through the names of directories in the specified path and changes them to lowercase.
    """
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)

            # Check if the item is a directory
            if os.path.isdir(full_path):
                # Convert the directory name to lowercase
                new_name = item.lower()

                # Rename the directory if the name is different
                if item != new_name:
                    new_full_path = os.path.join(path, new_name)
                    os.rename(full_path, new_full_path)
                    print(f"{TEAL}Rename: {item} -> {new_name}{RESET}")
    
    except Exception as e:
        print(f"Error: {e}")

def main():
    try:
        # Check if the script is being run with sudo/root privileges
        if os.getuid() != 0:
            print("Please use sudo.")
        else:
            print(banner)
            decision = packages()
            if decision == 'y':
                # Update + Upgrade first
                print(f"{GREEN}Updating and Upgrading{RESET}")
                os.system("apt update -y && apt upgrade -y")
                os.system("apt full-upgrade -y")

                print(f"{GREEN}Starting installation...{RESET}")

                #Install tools
                for tool in tools:
                    print(f"{GREEN}Installing {tool}{RESET}")
                    os.system(f'apt install {tool}')

                # Install snap tools
                for tool in snap_tools:
                    print(f"{GREEN}Installing {tool} with snap.{RESET}")
                    os.system(f'snap install {tool}')
                
                #Create directory for wordlists and check for existing wordlists
                os.system("mkdir -p /opt/wordlists")
                existing_wordlists = check_directories("/opt/wordlists")


                print(f"{GREEN}Installing Wordlists...{RESET}")
                
                for i, git_link in enumerate(git_wordlists):
                    wordlist_name = raw_wordlists[i].lower()

                    if wordlist_name in existing_wordlists:
                        print(f"{TEAL}Skipping {raw_wordlists[i]} (already installed).{RESET}")

                    else:
                        print(f"{GREEN}Installing {raw_wordlists[i]} at /opt/wordlists{RESET}")
                        os.system(f"cd /opt/wordlists; git clone {git_link}")

                # Rename directories to lowercase after cloning
                lowercase_directories("/opt/wordlists")

                print(f"{GREEN}Done!{RESET}")
                
            elif decision == 'n':
                print(f"{RED}Exitting...{RESET}")
                os.system("exit")
                
            else:
                print(f"{RED}Invalid. Please enter 'Y' or 'N'.{RESET}")
                main()

    except KeyboardInterrupt:
        print(f"\n{RED}Installation interrupted by user.{RESET}")
    
    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")



if __name__ == "__main__":
    main()