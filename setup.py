import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wgame",
    version="0.1",
    author="WoodRixel",
    author_email="woodrixel@post.cz",
    description="Library for making games in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woodrixel/WGame",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
