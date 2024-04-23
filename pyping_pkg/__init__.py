"""
Pyping_pkg
----------

    Pyping_pkg is a module used to check projects PyPi web site informations as if already exists and your respective versions.

    This module also is prepared to leading you to upload your own python module project on PyPi repository.

    Can we try? Let's go!

Best regards from Natanael Quintino
"""

__all__ = ["exists", "getVersions", "uploadProject"]

import os
import re
import requests
from .scriptsText import setupScript, tomlScript, mitLicenseScript, readmeScript

def exists(package: str, verbose: bool = False) -> (bool):
    response = requests.get(f"https://pypi.org/project/{package}")
    unavailable = response.status_code == 200
    if unavailable and verbose:
        print(
        f"Unfortunately, '{package}' already exists in the Pypi repository."
        )
    elif verbose:
        print(
        f"Fortunately, '{package}' does not exist in Pypi repository!"
        )

    return unavailable


def getVersions(package) -> (list[str]):
    response = requests.get(f"https://pypi.org/project/{package}/#history")

    versions = re.findall(
        "\<p class=\"release__version\"\>\s*(.*)\s*\<\/p\>",
        response.text
    )

    # # Get lines from response text content
    # contentLines = response.text.split("\n")

    # # Get versions index on contentLines
    # versionsIdx = [
    #     i+1 for i, t in enumerate(contentLines)
    #         if '<p class="release__version">' in t
    # ]

    # # Get versions from contentLines
    # versions = [contentLines[i].strip() for i in versionsIdx]

    return versions


def generateSetup(path) -> (None):
    """Generate setup.py file"""

    while exists(module:=input("Type the pymodule name: "), verbose=True):
        pass
    description      = input("           description: ")
    author           = input("           author name: ")
    author_email     = input("          author email: ")
    license          = input("               license: ")
    requirements     = input(" packages requirements: ")
    keywords         = input("              keywords: ")
    long_description = description

    path = path.rstrip("/")

    if "setup.py" in os.listdir(path):
        print("setup.py already exists!")
        answer = input("Do you wanna update 'setup.py'? (Y/n) ")
        if "n" in answer.lower():
            return None

    with open("{path}/setup.py", "x") as f:
        f.write(
            setupScript.format(
                module=module, description=description, long_description=long_description, author=author, author_email=author_email, license=license, requirements=requirements, keywords=keywords
            )
        )

    return None


def generateToml(path) -> (None):
    """Generate pymodule.toml file"""

    while exists(module:=input("Type the pymodule name: "), verbose=True):
        pass
    description    = input("     description: ")
    author         = input("     author name: ")
    author_email   = input("    author email: ")
    license        = input("         license: ")
    githubUserName = input(" github UserName: ")

    path = path.rstrip("/")

    if f"{module}.toml" in os.listdir(path):
        print(f"{module}.toml already exists!")
        answer = input(f"Do you wanna update '{module}.toml'? (Y/n) ")
        if "n" in answer.lower():
            return None

    with open("{path}/{module}.toml", "w") as f:
        f.write(
            tomlScript.format(
                module=module, description=description, 
                author=author, author_email=author_email,
                license=license, githubUserName=githubUserName
            )
        )

    return None


def generateReadme(path) -> (None):
    """Generate README.md file"""

    while exists(module:=input("Type the pymodule name: "), verbose=True):
        pass
    description    = input("     description: ")

    path = path.rstrip("/")

    if f"README.md" in os.listdir(path):
        print(f"README.md already exists!")
        answer = input(f"Do you wanna update 'README.md'? (Y/n) ")
        if "n" in answer.lower():
            return None

    with open("{path}/README.md", "w") as f:
        f.write(
            readmeScript.format(
                module=module, description=description
            )
        )

    return None


def generateMitLicense(path) -> (None):
    """Generate LICENSE file"""

    author         = input("Type the pymodule author name: ")

    path = path.rstrip("/")

    if f"LICENSE" in os.listdir(path):
        print(f"LICENSE already exists!")
        answer = input(f"Do you wanna update 'LICENSE'? (Y/n) ")
        if "n" in answer.lower():
            return None

    with open("{path}/LICENSE", "w") as f:
        f.write(
            mitLicenseScript.format(
                author=author
            )
        )

    return None


def generateAllFiles(path):
    """Generate setup.py, pymodule.toml, README.md and LICENSE files"""

    while exists(module:=input("Type the pymodule name: "), verbose=True):
        pass
    description      = input("           description: ")
    author           = input("           author name: ")
    author_email     = input("          author email: ")
    license          = input("               license: ")
    requirements     = input(" packages requirements: ")
    keywords         = input("              keywords: ")
    githubUserName   = input("       github UserName: ")
    long_description = description

    path = path.rstrip("/")

    for fileName in ["setup.py", f"{module}.toml", "README.md", "LICENSE"]:
        if fileName in os.listdir(path):
            print(f"'{fileName}' already exists!")
            answer = input(f"Do you wanna update '{fileName}'? (Y/n) ")
            if "n" in answer.lower():
                continue
            
        script = {
            "setup.py": setupScript,
            f"{module}.toml": tomlScript,
            "README.md": readmeScript,
            "LICENSE": mitLicenseScript
        }[fileName]

        from pyidebug import debug
        debug(globals(), locals())
        input("HERE")

        with open(f"{path}/{fileName}", "w") as f:
            f.write(
                script.format(
                    module=module, description=description, long_description=long_description, author=author, author_email=author_email, license=license, requirements=requirements, keywords=keywords,
                    githubUserName=githubUserName
                )
            )

    return None


def buildProject(
        module: str = None,
        version: str = None,
        path: str = None
        ) -> (None):

    if module is None or exists(module, verbose=True):
        while exists(module:=input("Type the pymodule name: "), verbose=True):
            pass
    versions = getVersions(module)
    if version is None or version in versions:
        while (version:=input("Type the pymodule version: ").strip(" .")) in versions:
            pass
    if path is None:
        path = input("Type the pymodule main path: ")

    path = "."\
        if not any(path)\
        else path.rstrip(r"/")

    module = module.lower().replace("-","_")
    for file in [f"{path}/setup.py",
                 f"{path}/{module}.toml",
                 f"{path}/{module}/__init__.py"]:
        with open(file, "r+") as f:
            content = f.readlines()
            for i, c in enumerate(content):
                if "VERSION = " in c or "version = " in c \
                        or "__version__ = " in c:
                    pos = c.find('"')
                    content[i] = c[:pos+1] + version + '"\n'
            f.seek(0)
            f.write("".join(content))

    os.system(
        " && ".join([
            f"cd {path}",               # Go to package folder folder
            "python3 -m build --sdist", # Compacting package file
        ])
    )

    return None


def uploadPackage(path, version):
    "Upload module to PyPI repository"

    # Check if module already exists in PyPI repository
    exists()

    out = os.system(
        f"python3 -m twine upload {path}/dist/*{version}.tar.gz", #
    )

    return out


def removeCompactedFiles(path):
    "Remove compacted files"

    os.system(
        f"rm -R {path}/dist"
    )

    return None


def pyping(
        module: str,
        version: str,
        path: str,
        createAllFiles: bool = False
        ) -> (None):

    if createAllFiles:
        generateAllFiles(path)
    buildProject(module, version, path)
    uploadPackage(path)
    removeCompactedFiles(path)

    return None
