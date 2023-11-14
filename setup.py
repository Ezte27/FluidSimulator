import pathlib
from setuptools import setup, find_packages

# The directory containing this file
SETUP_PATH = pathlib.Path(__file__).parent

# The text of the README file
README = (SETUP_PATH / "README.md").read_text()

NAME                = "FluidSimulator"
VERSION             = "1.0.0"
DESCRIPTION         = "This fluid simulator offers an interactive and visually captivating simulation of fluid dynamics, providing an engaging way to explore the behavior of fluids in a 2D environment."
LONG_DESCRIPTION    = README
AUTHOR              = "Esteban Calderon"
AUTHOR_EMAIL        = "estedcg27@gmail.com"
URL                 = "https://github.com/Ezte27/FluidSimulator"
LICENSE             = "MIT"
KEYWORDS            = ["Fluid", "Simulation", "Fluid simulation", "Liquid simulation", "Gas simulation", "Fluid simulator"]
PLATFORMS           = ["Windows", "Linux"]
INSTALL_REQUIRES    = ["numpy", "matplotlib", "pygame"]

# This call to setup() does all the work
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    packages=find_packages(),
    py_modules= [],
    scripts=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    license=LICENSE,
    keywords=KEYWORDS,
    platforms=PLATFORMS,
    python_requires=">=3.10",
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    # entry_points={
    #     "console_scripts": [
    #         "FluidSim=FluidSimulator.__main__:main",
    #     ]
    # },
)