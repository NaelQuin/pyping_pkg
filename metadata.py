"""
Py modules metadata
"""

__author__ = "Natanael Quintino"
__gitUser__ = "NaelQuin"
__email__ = "natanael.quintino@ipiaget.pt"
__license__ = "MIT License"

template = {
    'description': "",
    'long_description': "",
    'requirements': "",
    'keywords': "",
    'author': __author__,
    'author_email': __email__,
    'license': __license__,
    'githubUserName': __gitUser__,
}

metadata = {
    "opytimal": template | dict(
        description="",
        long_description="",
        keywords=""
    ),
    "pyping_pkg": template | dict(
        description="Pyping_pkg is a module used to check projects PyPi web site informations as if already exists and your respective versions.",
        long_description="Pyping_pkg is a module used to check projects PyPi web site informations as if already exists and your respective versions.",
        requirements="build, twine",
        keywords="pypi, automation, install, packages, module"
    ),
    "pyidebug": template | dict(
        description="",
        long_description="",
        keywords=""
    ),
    "pystr": template | dict(
        description="",
        long_description="",
        keywords=""
    ),
    "pycompiler": template | dict(
        description="",
        long_description="",
        keywords=""
    ),
    "pyle_handling": template | dict(
        description="",
        long_description="",
        keywords=""
    ),
    "pyaget": template | dict(
        description="",
        long_description="",
        keywords=""
    ),
    "chatybot": template | dict(
        description="",
        long_description="",
        keywords=""
    ),
    "pyai_comm": template | dict(
        description="",
        long_description="",
        keywords=""
    ),
}