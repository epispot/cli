import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epicli", # Replace with your own username
    version="0.0.1",
    author="epispot",
    description="The epispot package - in the command line.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/epispot/epicli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)