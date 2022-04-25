import pathlib
from setuptools import setup
from assets.Version import Version
# The directory containing this file
HERE = pathlib.Path(__file__).parent.resolve()

# The text of the README file
README = (HERE / "README.md").read_text()
requirements = (HERE / 'assets' / 'requirements.txt').read_text(encoding='utf-8').split("\n")

# This call to setup() does all the work
setup(
    name="dbis-relational-model",
    version=Version.version,
    description=Version.description,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rwth-acis/dbis-relational-model.git",
    author="Philipp Hochmann",
    author_email="hochmann@dbis.rwth-aachen.de",
    license="Apache",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=["excmanager"],
    include_package_data=True,
    install_requires=requirements
)
