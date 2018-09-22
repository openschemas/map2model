# OpenSchemas map2model

![https://github.com/openschemas/spec-template/raw/master/img/hexagon_square_small.png](https://github.com/openschemas/spec-template/raw/master/img/hexagon_square_small.png)

This repository will show you how to use **map2model**, which is a module provided
by [openschemas python](https://www.github.com/openschemas/openschemas-python), and
a simplified version of the now deprecated Python module derived from 
the [Bioschemas Groups](http://bioschemas.org/groups/). It will help you
to create an OpenSchema intended for submission to [schemas.org](schemas.org), with
a focus on technology and research software or high performance computing specifications 
that might not fall cleanly under strictly biological sciences (but support open science).

**map2model** retrieves properties and schema.org (Marginality, Cardinality and Controlled Vocabularies) 
using mapping files (in a specifications folder, see an [example here](https://www.github.com/openschemas/spec-container)) 
then classifies properties into two groups:
1. **Extended properties:** Properties that are part of the extended schema.org Type.
1. **New properties:** Properties that are new to the schema.org vocabulary or are completely new to schema.org.

After classifying the properties, **map2model** generates Markdown file(s) 
that can be interpreted by [openschemas.github.io](https://openschemas.github.io)

![map2model workflow](docs/img/map2model_workflow.png)
> If you want to modify the Flow Chart open the [xml file](docs/img/map2model_workflow.xml) and name it `map2model_workflow.png` in the *doc > img*.

## Contribute a Specification
Do you want to contribute a specification? Your workflow will look like this:

### 1. Start with a Template
Fork the [template repository](https://www.github.com/openschemas/spec-template) and download them to it. You can also see a live example, [soec-container](https://www.github.com/openschemas/spec-container) that also has content in Github Pages. When you connect your forked repository to CircleCI it will use the [schema-builder](https://www.github.com/openschemas/schema-builder) to generate the files as artifacts or back to github pages. You can use the same `schema-builder` container to do this locally.
1. Issue a pull request to the [specifications](https://www.github.com/openschemas/specifications) repository with your contribution! This means:
   - forking the repository, cloning your fork
   - adding your `MySpecification.html` file to the `_specifications` folder
   - opening a pull request for review

We encourage this setup so that each of the specifications is maintained in a modular fashion. You can
maintain your specification (and issues / discussion around it) in its own Git repository,
to ensure modularity and version control of examples and associated documentation. We would be happy to 
create for you an `openschemas/spec-<NAME>` repository here if you want to join the Github organization
and get support from the maintainers within!

### 2. Create your Specification
In the template repository (and here) you will notice tsv files under subfolders of 
the "specifications" folder. This is where you need to create and download your own
files for your new specification! You can create these files easily 
using [Google Sheets](https://docs.google.com/spreadsheets/d/1Ty69GRzc3xuvfpEIRHjfl_9L25MNFfrKXCdwrpxYslo/edit?usp=sharing). 
If this is a new specification, you will want to add an entry to [specifications/configuration.yml]. This file 
tells map2model which specifications exist. Here is an example:

```
- name: NameOfMySpec
  status: revision
  spec_type: Profile
  use_cases_url:
  version: 0.2.0
  parent_type: CreativeWork
```

Next, run map2model! As mentioned above, if you use the template this step will be done for you
in the continuous integration (and you can stop reading here). If you want to do this natively,
on your host, then keep reading.

## Map2Model Usage

This usage details native usage of map2model, which isn't reproducible and not the recommended approach! 
However if you are building software with it, you will need to know this. If not, we recommend first the 
[template](https://www.github.com/openschemas/spec-template) and the docker 
[openschemas/schema-builder](https://www.github.com/openschemas/schema-builder) that 
packages map2model and is used by the template.

### Requirements
These instructions are for local usage.

Before starting, please ensure you have the following installed:
1. Git [https://git-scm.com/downloads](https://git-scm.com/downloads)
1. Python 3  [https://www.python.org/downloads/](https://www.python.org/downloads/)
1. Pip [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)

### Installation

If you want to use the configuration and specification templates provided, first 
clone the **map2model** repository:

```bash
git clone https://github.com/openschemas/map2model.git
cd map2model
```

Next, install openschemas, which provides map2model

```bash
pip install openschemas
```

### 1. Command Line Usage

The Openschemas Python module provides a `map2model` console script that you can 
run. For usage, ask it for help"

```
map2model --help
usage: map2model [-h] [--config CONFIG] [--folder SPECS] [--output OUTFOLDER]
                 [--template TEMPLATE] [--repo REPO]

map2model

optional arguments:
  -h, --help           show this help message and exit
  --config CONFIG      configuration.yml file, defaults to configuration.yml
                       in folder
  --folder SPECS       folder with input specification subfolders
  --output OUTFOLDER   folder to write output specification subfolders
  --template TEMPLATE  template for openschemas.github.io. Should not need
                       change.
  --repo REPO          final repo intended for specifications.
usage: map2model [-h] [--config CONFIG] [--folder SPECS] [--output OUTFOLDER]
                 [--template TEMPLATE] [--repo REPO]

map2model

optional arguments:
  -h, --help           show this help message and exit
  --config CONFIG      configuration.yml file, defaults to configuration.yml
                       in folder
  --folder SPECS       folder with input specification subfolders
  --output OUTFOLDER   folder to write output specification subfolders
  --template TEMPLATE  template for openschemas.github.io. Should not need
                       change.
  --repo REPO          final repo intended for specifications.
```

See the [schema-builder](https://www.github.com/openschemas/schema-builder) for 
good examples of these various arguments. Generally, you will want to tell
the module where your configuration file, input folder, and output folder are.
For example:

```bash
map2model --config specifications/configuration.yml --folder specifications --output docs/spec_files
```

### 1. Python Usage

You can also interact with the module from within python! This example
is provided in [run.py](run.py)

```python
#!/usr/bin/env python3

# This is an example of using map2model, a module provided by
# openschemas-python
# python3 run.py
#
# https://www.github.com/openschemas/openschemas-python
# pip install openschemas
from openschemas.main.map2model import main

# Here is an example to run the parser in python
spec_parser = main(config_yml='specifications/configuration.yml',
                   output='docs/spec_files',
                   folder='specifications')
```

Again, all you need to do is generate the tsv files and add an entry to the configuration.yml,
and we provide a [Google Drive sheets template](https://docs.google.com/spreadsheets/d/1Ty69GRzc3xuvfpEIRHjfl_9L25MNFfrKXCdwrpxYslo/edit?usp=sharing) that you can use to do this. 
Simply export each sheet as .tsv (tab separated values). 
This means that four files should go into your `_NameOfMySpec` folder. While your 
specification is a draft, the name of the folder will start with an underscore 
(`_NameOfMySpec`). When you are done, remove the underscore (`NameOfMySpec`).

When you are finished with your specification, if you run the script here you will generate 
files in *map2model > docs > spec_files*. Check that your folder is present! 

```
tree docs/spec_files
├── Container
│   ├── Container.html
│   ├── Container.yml
│   ├── examples
│   │   └── README.md
│   └── README.md
└── DataCatalog
    ├── DataCatalog.html
    ├── DataCatalog.yml
    ├── examples
    │   └── README.md
    └── README.md
```

If you are generating specifications for contribution, you will next want to 
open a pull request (PR) to update the [specifications](https://www.github.com/openschemas/specifications) repository.
Specifically, add the *.html files to the [_specifications folder](https://github.com/openschemas/specifications/tree/master/_specifications) in this repository.
