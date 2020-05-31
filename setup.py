import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scraphub",
    version="0.1.0",
    author="Thomas PERROT",
    author_email="thomas.perrot1@gmail.com",
    description="A scrapping and analyzing tool for Pornhub",
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
