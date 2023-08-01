# Probabilistic data-driven modeling

This repo contains the code related to the book titled __Probabilistic data-driven modeling__, written by Tomaso Aste, professor of Complexity Science at University College London. The book introduces and guides the reader through a selection of methodologies and approaches to construct models from data. These data-driven approaches have been originally developed in different fields from statistics to complexity science. They are general procedures and tools that apply to any domain where models must be built from observational data. The code in the current repository is organised by Chapters and presents an applied perspective on modeling of real complex systems.

## How to

In the following lines, we report the main steps to download, access and run the code provided in the current GitHub repo.

#### Cloning the GitHub repository
In order to clone the current GitHub repository, the user is required to have Git locally installed. If this is not the case, follow the instructions at https://github.com/git-guides/install-git.

Once you have Git locally installed and correctly set up, clone the following repository typing `git clone https://github.com/FinancialComputingUCL/DataDrivenModeling.git`.

#### Python installation
All the provided code is written using the Python programming language. The user is required to have a Python version installed locally. If this is not the case, follow the following steps to obtain it.
- Access the URL: https://www.python.org/downloads/.
- Download the latest stable version of the language (`3.11.4` at the writing time). 
- Follow the prompted installation steps to correctly finalise the process.
- Double check everything was correctly installed typing `python --version` in a new Terminal. The prompted Python's version should coincide with the one you previously decided to download.

#### Required packages' installation
Using Python, packages can be managed in many different ways. We advise the user to use `virtualenv` to easily manage project' specific dependencies (i.e. packages).

To create a new virtual environment, open a new Terminal in the chosen directory and follow these steps:
- Type `which virtualenv`
	- _if_ `virtualenv not found` message is prompted:
		- Install `virtualnv` typing `pip3 install virtualenv`.
		- Double check everything was correctly installed typing `which virtualenv` command.
	- _else_:
		- Skip to the next step.
- Create a new virtual environment typing `virtualenv <name_of_your_environment>`. If you have multiple Python versions installed locally, be sure to specify the Python's version to be used to create the new virtual environment (e.g. `virtualenv -p /usr/bin/python3.11.4 <name_of_your_environment>`).
- Source the newly created virtual environment typing `source <name_of_your_environment>/bin/activate`.
- Install the packages required to run the code provided in the current GitHub repo typing `pip3 install -r requirements.txt`.

To temporarily deactivate your environment, type `deactivate`.
To permanently delete your environment, type `sudo rm -rf <name_of_your_environment>`.

#### Running the code
The majority of the code provided in the current GitHub repo is in the form of Jupyter Notebooks. Once you run all the previously listed steps, you can run each Notebook in the following way:
- Access the Chapter's folder you are interested in (e.g., `cd ./Chapter_5`).
- Type `juyter notebook`.
- Choose the `.ipynb` you are interested in and use the graphical interface to run all or specific cells.