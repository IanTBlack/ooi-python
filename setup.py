import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
	
	
setuptools.setup(
    name="ooi",
    version="0.0.1",
    author="Ian Black",
    author_email="ian.black@oregonstate.edu",
    description="Modules for navigating the OOI M2M system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IanTBlack/ooi-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    install_requires=[
        'xarray',
        'requests',
        ],
)