setupScript = """
    from setuptools import setup, find_packages

    MODULE = "{module}"
    VERSION = "0.0.0"
    DESCRIPTION = "{description}"
    LONG_DESCRIPTION = "{long_description}"
    AUTHOR = "{author}"
    AUTHOR_EMAIL = "{author_email}"
    LICENSE = "{license}"
    REQUIREMENTS = "{requirements}"
    KEYWORDS = "{keywords}"

    setup(
        name=MODULE,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        packages=find_packages(
            include=[MODULE, MODULE+'.*']
            ),
        install_requires=[
            REQUIREMENTS
        ],
        keywords=KEYWORDS,
        classifiers= [
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
        ]
    )
""".replace("\n    ", "\n")

tomlScript = """
    [build-system]
    requires = ["setuptools>=61.0"]
    build-backend = "setuptools.build_meta"

    [project]
    name = "{module}"
    version = "0.0.0"
    authors = [
        {name="{author}", email="{author_email}"},
    ]
    description = "{description}"
    readme = "README.md"
    requires-python = ">=3.8"
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: {license}",
        "Operating System :: OS Independent",
    ]

    [project.urls]
    "Homepage" = "https://github.com/{githubUserName}/{module}"
    "Bug Tracker" = "https://github.com/{githubUserName}/{module}/issues"
""".replace("\n    ", "\n")


mitLicenseScript = """
    MIT License

    Copyright (c) 2024 {author}

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""".replace("\n    ", "\n")

readmeScript = """
    # {module}

    {description}
""".replace("\n    ", "\n")
