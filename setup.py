import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="charusat-unofficial-api",
    version="1.0.0",
    author="aditya76-git",
    author_email="cdr.aditya.76@gmail.com",
    description="CHARUSAT API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aditya76-git/charusat-unofficial-api",
    project_urls={
        "Tracker": "https://github.com/aditya76-git/charusat-unofficial-api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "beautifulsoup4"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)