"""
Pyping_pkg
----------

    Pyping_pkg is a module used to check projects PyPi web site informations as if already exists and your respective versions.

    This module also is prepared to leading you to upload your own python module project on PyPi repository.

    Can we try? Let's go!

Best regards from Natanael Quintino
"""

import os
import re
import sys
import requests
from .scriptsText import setupScript, tomlScript, mitLicenseScript, readmeScript
from metadata import metadata


__version__ = "0.2.0"
__all__ = [
    "exists", "getVersions", "uploadPackage", "buildProject",
    "pyping"
    ]


def prepareRequirements(requirements: str) -> (str):
    requirements = requirements.split(",")
    for i, req in enumerate(requirements):
        requirements[i] = f"'{req.strip()}'"
    return ", ".join(requirements)


def addVersion(file):

    content = file.read()
    check = '__version__ = ' in content

    file.seek(0)

    if not check:
        pos = content.find("\ndef ")
        if pos != -1:
            content = content[:pos] + "\n__version__ = \"0.1.0\"\n" + content[pos:]
            file.write(content)

    return check


def getKey(dic, key, func, *args):
    value = dic[key]\
        if key in dic\
        else func(*args)
    return value


def packageNameSuggestion(package: str) -> (None):
    global PACKAGE_NAME_TRY, HISTORY_NAMES

    PACKAGE_NAME_TRY += 1
    HISTORY_NAMES.append(package)

    if PACKAGE_NAME_TRY == 3:
        # namesSug = getNamesSuggestions(package)
        # print(
        #     f"\nMaybe you like one of these names? ({namesSug})\n"
        #     )
        namesSug = HISTORY_NAMES
        print(
            f"\nMaybe you can generate a combinarion of these names? ({namesSug})\n"
            )
    else:
        print(
            f"\nUnfortunately, '{package}' already exists.",
            "Choose another name.\n",
        )
    return None


def getNamesSuggestions(package: str) -> (str):
    global HISTORY_NAMES

    from pyai_comm import Copilot

    answer = Copilot(os.environ["COPILOT_API_KEY"]).ask(
        "Suggest me 3 names for my python package that nonexists on PyPI repository and considering the following names as inspiration: {'\''.join(HISTORY_NAMES)}. Give me your suggestions in a enumerated list.",
        stream=False
    )

    names = answer.replace("\n\n", "\n")\
                 .replace("1. ", "")\
                 .replace("2. ", "")\
                 .replace("3. ", "")\
                 .split("\n")[1:-1]

    return f"[{', '.join(names)}]"


def getMaintainers(package: str) -> (bool):
    response = requests.get(f"https://pypi.org/project/{package}/#data")

    MAINTAINERS = maintainers = set(
        re.findall(
            "\<span class=\"sidebar-section__user-gravatar-text\"\>\s*(.*)\s*\</span\>",
            response.text
        )
    )

    return maintainers


def exists(package: str, verbose: bool = False) -> (bool):
    global VERSIONS

    response = requests.get(f"https://pypi.org/project/{package}")
    unavailable = response.status_code == 200
    if MAINTAINER_CHECK and unavailable and verbose:
        print(
        f"\nUnfortunately, '{package}' already exists in the version. Choose another version different of these: {VERSIONS}\n"
        )
    elif unavailable and verbose:
        print(
        f"\nUnfortunately, '{package}' already exists in the Pypi repository."
        )
    elif verbose:
        print(
        f"Fortunately, '{package}' does not exist in Pypi repository!"
        )

    return unavailable


def maintainerCheck(package: str) -> (bool):
    maintainers = getMaintainers(package)

    nickname = input(
        f"\nWhat is your Gravatar nickname associated to this python package? "
    )

    output = nickname in maintainers

    return output


def getVersions(package) -> (list[str]):
    global VERSIONS

    response = requests.get(f"https://pypi.org/project/{package}/#history")

    VERSIONS = versions = re.findall(
        "\<p class=\"release__version\"\>\s*(.*)\s*\<\/p\>",
        response.text
    )

    return versions


def generateSetup(package, version, path) -> (None):
    """Generate setup.py file"""

    printed = False
    while exists(package, verbose=True) and not MAINTAINER_CHECK:
        package=input("Type the pypackage name: ")
        printed = True
        packageNameSuggestion(package)

    if version in VERSIONS and MAINTAINER_CHECK:
        while (version:=input("Type the pypackage version: ").strip(" .")) in VERSIONS and MAINTAINER_CHECK:
            print(f"\nChoose another version that not exists in the versions list: {VERSIONS}\n")
        updateVersion(package, version, path)

    if not printed:
        print("Type the pypackage ", end="")

    description = getKey(
        metadata[package],
        "description",
        input,
        "           description: "
    )
    author = getKey(
        metadata[package],
        "author",
        input,
        "           author name: "
    )
    author_email = getKey(
        metadata[package],
        "author_email",
        input,
        "          author email: "
    )
    license = getKey(
        metadata[package],
        "license",
        input,
        "               license: "
    )
    requirements = getKey(
        metadata[package],
        "requirements",
        input,
        " packages requirements: "
    )
    keywords = getKey(
        metadata[package],
        "keywords",
        input,
        "              keywords: "
    )
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
                package=package, description=description,
                long_description=long_description, author=author,
                author_email=author_email, license=license,
                requirements=prepareRequirements(requirements),
                keywords=keywords,
            )
        )

    return None


def generateToml(package, version, path) -> (None):
    """Generate <package>.toml file"""

    printed = False
    while exists(package, verbose=True) and not MAINTAINER_CHECK:
        package=input("Type the pypackage name: ")
        printed = True
        packageNameSuggestion(package)

    if version in VERSIONS and MAINTAINER_CHECK:
        while (version:=input("Type the pypackage version: ").strip(" .")) in VERSIONS and MAINTAINER_CHECK:
            print(f"\nChoose another version that not exists in the versions list: {VERSIONS}\n")
        updateVersion(package, version, path)

    if not printed:
        print("Type the pypackage ", end="")

    description = getKey(
        metadata[package],
        "description",
        input,
        "     description: "
    )
    author = getKey(
        metadata[package],
        "author",
        input,
        "     author name: "
    )
    author_email = getKey(
        metadata[package],
        "author_email",
        input,
        "    author email: "
    )
    license = getKey(
        metadata[package],
        "license",
        input,
        "         license: "
    )
    githubUserName = getKey(
        metadata[package],
        "githubUserName",
        input,
        " github UserName: "
    )

    path = path.rstrip("/")

    if f"{package}.toml" in os.listdir(path):
        print(f"{package}.toml already exists!")
        answer = input(f"Do you wanna update '{package}.toml'? (Y/n) ")
        if "n" in answer.lower():
            return None

    with open("{path}/{package}.toml", "w") as f:
        f.write(
            tomlScript % {
                "module": package,
                "author": author,
                "author_email": author_email,
                "description": description,
            }
        )

    return None


def generateReadme(package, version, path) -> (None):
    """Generate README.md file"""

    printed = False
    while exists(package, verbose=True) and not MAINTAINER_CHECK:
        package=input("Type the pypackage name: ")
        printed = True
        packageNameSuggestion(package)

    if version in VERSIONS and MAINTAINER_CHECK:
        while (version:=input("Type the pypackage version: ").strip(" .")) in VERSIONS and MAINTAINER_CHECK:
            print(f"\nChoose another version that not exists in the versions list: {VERSIONS}\n")
        updateVersion(package, version, path)

    if not printed:
        print("Type the pypackage ", end="")

    description = getKey(
        metadata[package],
        "description",
        input,
        "     description: "
    )

    path = path.rstrip("/")

    if f"README.md" in os.listdir(path):
        print(f"README.md already exists!")
        answer = input(f"Do you wanna update 'README.md'? (Y/n) ")
        if "n" in answer.lower():
            return None

    with open("{path}/README.md", "w") as f:
        f.write(
            readmeScript.format(
                module=package, description=description
            )
        )

    return None


def generateMitLicense(package, version, path) -> (None):
    """Generate LICENSE file"""

    author = getKey(
        metadata[package],
        "author",
        input,
        "Type the pypackage author name: "
    )

    if version in VERSIONS and MAINTAINER_CHECK:
        while (version:=input("Type the pypackage version: ").strip(" .")) in VERSIONS and MAINTAINER_CHECK:
            print(f"\nChoose another version that not exists in the versions list: {VERSIONS}\n")
        updateVersion(package, version, path)

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


def generateAllFiles(package, version, path):
    """Generate setup.py, <package>.toml, README.md and LICENSE files"""

    printed = False
    while exists(package, verbose=True) and not MAINTAINER_CHECK:
        package=input("Type the pypackage name: ")
        printed = True
        packageNameSuggestion(package)

    if version in VERSIONS and MAINTAINER_CHECK:
        while (version:=input("Type the pypackage version: ").strip(" .")) in VERSIONS and MAINTAINER_CHECK:
            print(f"\nChoose another version that not exists in the versions list: {VERSIONS}\n")
        updateVersion(package, version, path)

    if not printed:
        print("Type the pypackage ", end="")

    description = getKey(
        metadata[package],
        "description",
        input,
        "                  description: "
    )
    author = getKey(
        metadata[package],
        "author",
        input,
        "                  author name: "
    )
    author_email = getKey(
        metadata[package],
        "author_email",
        input,
        "                 author email: "
    )
    license = getKey(
        metadata[package],
        "license",
        input,
        "                      license: "
    )
    requirements = getKey(
        metadata[package],
        "requirements",
        input,
        "        packages requirements: "
    )
    keywords = getKey(
        metadata[package],
        "keywords",
        input,
        "                     keywords: "
    )
    githubUserName = getKey(
        metadata[package],
        "githubUserName",
        input,
        "              github UserName: "
    )
    long_description = description

    # Remove / from path
    path = path.rstrip("/")

    for fileName in ["setup.py", f"{package}.toml", "README.md", "LICENSE"]:

        if fileName in os.listdir(path):
            print(f"'{fileName}' already exists!")
            answer = input(f"Do you wanna update '{fileName}'? (Y/n) ")
            if "n" in answer.lower():
                continue

        script = {
            "setup.py": setupScript,
            f"{package}.toml": tomlScript,
            "README.md": readmeScript,
            "LICENSE": mitLicenseScript
        }[fileName]

        with open(f"{path}/{fileName}", "w") as f:

            if fileName.endswith(".toml"):
                # Formattin toml file
                script = script % {
                    "module": package,
                    "author": author,
                    "author_email": author_email,
                    "description": description,
                }

            else:
                # Formatting file text content
                script = script.format(
                        module=package, description=description,
                        long_description=long_description, author=author,
                        author_email=author_email, license=license,
                        requirements=prepareRequirements(requirements),
                        keywords=keywords, githubUserName=githubUserName
                    )

            # Write content on file
            f.write(
                script.strip("\t\n ")
            )

    return package, version


def buildProject(
        package: str = None,
        version: str = None,
        path: str = None
        ) -> (None):
    global VERSIONS

    if package is None \
            or (exists(package, verbose=True) and not MAINTAINER_CHECK):
        while exists(package:=input("Type the pypackage name: "), verbose=True):
            packageNameSuggestion(package)
    versions = getVersions(package)\
        if "VERSIONS" not in globals() or not any(VERSIONS)\
        else VERSIONS
    if version is None or version in versions and MAINTAINER_CHECK:
        while (version:=input("Type the pypackage version: ").strip(" .")) in versions and MAINTAINER_CHECK:
            print(f"\nChoose another version that not exists in the versions list: {VERSIONS}\n")
        updateVersion(package, version, path)
    if path is None:
        path = input("Type the pypackage main path: ")

    path = "."\
        if not any(path)\
        else path.rstrip(r"/")

    package = package.lower().replace("-","_")

    updateVersion(package, version, path)

    os.system(
        " && ".join([
            f"cd {path}",               # Go to package folder folder
            #"python3 -m build --sdist", # Compacting package file
            "python3 setup.py sdist",   # Compacting package file
        ])
    )

    return package, version


def updateVersion(package, version, path):
    "Update version file "

    files2Change = [
        (f"{path}/setup.py", "VERSION = "),
        (f"{path}/{package}.toml", "version = "),
        (f"{path}/{package}/__init__.py", "__version__ = ")
    ]

    for file, toChange in files2Change:

        with open(file, "r+") as f:

            if toChange == "__version__ = " and not addVersion(f):
                continue
            else:
                content = f.readlines()

            for i, c in enumerate(content):

                if toChange in c:
                    pos = c.find('"')
                    newVersionLine = c[:pos+1] + version + '"\n'

                    if not newVersionLine.startswith(toChange):
                        continue

                    content[i] = newVersionLine

                    break

            # input("".join(content))

            f.seek(0)
            f.write("".join(content))

    return None


def uploadPackage(package, version, path):
    "Upload package to PyPI repository"

    # Check if package already exists in PyPI repository
    if not exists(package) or MAINTAINER_CHECK:
        out = os.system(
            f"python3 -m twine upload {path}/dist/*{version}.tar.gz",
        )
    else:
        out = None

    return out


def removeCompactedFiles(path):
    "Remove compacted files"

    os.system(
        f"rm -R {path}/dist"
    )

    return None


def pyping(
        package: str,
        version: str,
        path: str,
        createAllFiles: bool = False
        ) -> (None):
    global VERSIONS, MAINTAINER_CHECK, PACKAGE_NAME_TRY, HISTORY_NAMES

    MAINTAINER_CHECK = maintainerCheck(package)
    VERSIONS = getVersions(package)
    PACKAGE_NAME_TRY = 0
    HISTORY_NAMES = []

    if exists(package) and not MAINTAINER_CHECK:
        print(f"\nUnfortunately, '{package}' already exists in the Pypi repository and you not in maintainer list.\n", file=sys.stderr)
        return None

    if createAllFiles:
        package, version = generateAllFiles(package, version, path)
    package, version = buildProject(package, version, path)
    uploadPackage(package, version, path)
    removeCompactedFiles(path)

    return None