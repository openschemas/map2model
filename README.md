# OpenSchemas map2model

![docs/img/openbases.png](docs/img/openbases.png)

This version of **map2model** is a simplified version of Python module 
derived from the [Bioschemas Groups](http://bioschemas.org/groups/). It will help you
to create an OpenSchema intended for submission to [schemas.org](schemas.org), with
a focus on tech / hpc specifications that might not fall cleanly under strictly 
biological sciences, but support open science.

**map2model** retrieves properties and Bioschemas fields (Marginality, Cardinality and Controlled Vocabularies) from Bioschemas mapping files (in the [specifications](specifications)) folder, then classifies properties into two groups:
1. **Extended properties:** Properties that are part of the extended schema.org Type.
1. **New properties:** Properties that are new to the schema.org vocabulary or are completely new to schema.org.

After classifying the properties, **map2model** generates a Markdown file that can be interpreted by Bioschemas.org's web site thereby updating the Bioschemas.org web pages.

Comments on each specification should be done through the *GitHub issues* tool within the [bioschemas repository](https://github.com/BioSchemas/bioschemas). This enables tracking, commenting on and executing of corrections.

![map2model workflow](docs/img/map2model_workflow.png)
> If you want to modify the Flow Chart open the [xml file](docs/img/map2model_workflow.xml) and name it `map2model_workflow.png` in the *doc > img*.

## Usage

### Requirements

Before starting, please ensure you have the following installed:
1. Git [https://git-scm.com/downloads](https://git-scm.com/downloads)
1. Python 3  [https://www.python.org/downloads/](https://www.python.org/downloads/)
1. Pip [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)


### Executing map2model

Clone the **map2model** repository: ```git clone https://github.com/OpenSchemas/map2model.git```

```bash
git clone https://github.com/OpenSchemas/map2model.git
cd map2model
```

Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

If you want to add a specification, add an entry to [spec2model/configuration.yml]. This file tells map2model which specifications exist. To create a new specification, the section that you need to add includes:

```
- name: NameOfMySpec
  status: revision
  spec_type: Profile
  use_cases_url:
  version: 0.2.0
  parent_type: CreativeWork
```

Importantly, the following expectations will be tested:

  1. you have created a `_NameOfMySpec` folder under [specifications](specifications)
  2. you have created your mapping files and added them to this folder. We provide a [Google Drive sheets template](https://docs.google.com/spreadsheets/d/1Ty69GRzc3xuvfpEIRHjfl_9L25MNFfrKXCdwrpxYslo/edit?usp=sharing) that you can use to do this, and simply export each sheet as .tsv (tab separated values). This means that four files should go into your `_NameOfMySpec` folder. For detailed instruction, see [the Specification Creation](#create-a-specification) section below.
  3. You will be able to run validation functions over these files to check their quality.

While your specification is a draft, the name of the folder will start with an underscore (`_NameOfMySpec`). When you are done, remove the underscore (`NameOfMySpec`).

When you are finished with your spec, run the script to generate files in *map2model > docs > spec_files*. Check that your folder is present! Next, you will want to open a pull request (PR) to update the repository.

Coming soon, we will have full instructions for:

 - updating specifications
 - creating new specifications
