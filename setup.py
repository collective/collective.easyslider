from setuptools import setup, find_packages
import os
# import sys

version = "2.0.0a1"

# sys.path.insert(0, os.path.abspath("src/"))

setup(
    name="collective.easyslider",
    version=version,
    description="The product will allow you to apply an easyslider to any "
    "page with the ability to create each slide using a WYSIWYG "
    "editor. It also provides a slider view for Folders and "
    "Collections.",
    long_description="%s\n%s"
    % (open("README.rst").read(), open(os.path.join("docs", "HISTORY.txt")).read()),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Plone :: 6.0",
    ],
    keywords="plone easyslider",
    author="Nathan Van Gheem",
    author_email="vangheem@gmail.com",
    url="https://github.com/collective/collective.easyslider",
    license="GPL",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    extras_require={
        "test": [
            "plone.app.testing",
        ]
    },
    install_requires=[
        "setuptools",
        "plone.app.z3cform",
    ],
    entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
)
