# pyASCimport

An importer of .asc eyelink files into easily manageable dataframes

## Environment and dependencies

First create a suitable environment with conda by running:

''
conda create env -f environment.yml
''

Alternatively, you can make your own conda environment and then run dependencies with:

''
python import_libraries.py
''

## Usage

Once the environment is created, you just need to run the main script with

''
python readASC.py
''

You will be prompted with the relative path of your file and asked for which df and therefore metrics you want to extract/save

## Convert from .edf to .asc

In case your files are not in .asc, you can convert them by running:

''
python run_edf2asc.py 
''

You will be prompted with the relative path of your file and a call will be made to the edf2asc executable from EyeLink softwares.

