import setuptools
import os

with open(os.path.join(os.getcwd(), "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudconvert",
    version="0.0.14",
    author="Josias Montag",
    author_email="josias@montag.info",
    description="Python REST API wrapper for cloud convert",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luckysher/cloudconvert-python",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "urllib3"
    ],
    tests_require=["requests-mock"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)