import setuptools

with open("README.md") as f:
    long_description = f.read()

with open("./src/watchpoints/__init__.py") as f:
    for line in f.readlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            break
    else:
        print("Can't find version! Stop Here!")
        exit(1)

setuptools.setup(
    name="watchpoints",
    version=version,
    author="Tian Gao",
    author_email="gaogaotiantian@hotmail.com",
    description="watchpoints monitors read and write on variables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaogaotiantian/watchpoints",
    packages=setuptools.find_packages("src"),
    package_dir={"":"src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
    install_requires = [
        "objprint>=0.0.3"
    ]
)
