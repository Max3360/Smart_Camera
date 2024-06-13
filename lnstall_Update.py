import subprocess

def is_package_installed(package):
    # Check if the package is installed using the pip show command.
    result = subprocess.run(['pip', 'show', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0 # If the returncode is 0, it means it's installed.

# packages Stores the package name and version to be installed.
packages ={
    'cvzone': '==1.5.6',
    'ultralytics': '==8.0.35',
    'hydra-core': '==1.2.0',
    'matplotlib': '',
    'numpy': '',
    'opencv-python': '',
}
# Looping through packages
for package, version in packages.items():
    if is_package_installed(package):
        print(f'{package}{version} is already installed.') # If the package is installed Print a message that the package is installed.
    else:
        try:
            subprocess.run(['pip', 'install', f'{package}{version}']) # If the package is not installed yet, it will install the package.
            print(f'Susccessfully install {package}{version}') # If the installation is successful Type a message that the installation was successful.
        except Exception as e:
            print(f'Error installing {package}{version}: {e}') # If there is an error in installation will show an error message
            continue # Jump to install the next package.

