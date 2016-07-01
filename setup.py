from setuptools import setup, find_packages
setup(
    name = "cnet",
    version = "0.5",
    packages = find_packages(),
    install_requires = ["requests","paramiko"]
)
