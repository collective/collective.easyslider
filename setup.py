from setuptools import find_packages, setup
import os

install_requires = [
    'setuptools',
]

try:
    # Plone < 4.3
    import plone.app.z3cform
    install_requires.append('plone.app.z3cform')
except:
    # Plone >= 4.3
    install_requires.append('plone.z3cform')

version = '1.4.2'

setup(name='collective.easyslider',
      version=version,
      description="The product will allow you to apply an easyslider to any "
                  "page with the ability to create each slide using a WYSIWYG "
                  "editor. It also provides a slider view for Folders and "
                  "Collections.",
      long_description='%s\n%s' % (
          open("README.rst").read(),
          open(os.path.join("docs", "HISTORY.txt")).read()
      ),
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Framework :: Plone :: 3.3",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3"
      ],
      keywords='plone easyslider',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='http://plone.org/products/collective.easyslider/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'test': [
              'plone.app.testing',
          ]
      },
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """)
