from spec2model.file_manager import FolderDigger
from spec2model.mapping import MappingParser
from spec2model.validator import FolderValidator
import frontmatter
import os
import sys
from io import BytesIO

class FrontMatterParser:
    md_files_path = ''
    bsc_parser = ''
    bsc_spec_list = ''

    def __init__(self, input_folder='specifictions', 
                       output_folder='docs/spec_files/',
                       config_file_path='spec2map/configuration.yml'):

        '''defaults here are intended for running in spec2map repository. 
           Use via run.py to edit for your needs.
        '''
        self.__check_input_folder(input_folder)
        self.md_files_path = output_folder
        self.file_manager = FolderDigger(config_file_path)
        self.parser = MappingParser()

    def __check_input_folder(self, input_folder):
        '''check for the existence of the input folder, and ensure full path
           
           Parameters
           ==========
           input_folder: path (relative or full) to input folder with specification
           subdirectories.
        '''
        self.input_folder = os.path.abspath(input_folder)
        if not os.path.exists(input_folder):
            print('Cannot find %s' % input_folder)
            sys.exit(1)
        print('Found input folder %s' % input_folder)

    def __get_specs_list(self):
        '''return listing of specs, meaning loaded workbooks. The workbooks should
           already be validated by the file manager, and so we don't do it here.
           Each entry in the specs_list is a dictionary that includes paths to:
           mapping_file, bioschemas_file, specification_file, and authors_file.
        '''
        all_specs = dict()

        for name, params in self.specs_list.items():

            self.parser.set_metadata(params)
            all_specs[name] = self.parser.get_mapping()

        return all_specs

    def __get_specification_post(self, spec_dict, skip_fields=None):
        '''for a spec_workbook, which is a dictionary with "name" "workbook" and "params"
           derive the post material, an html file that is mostly yaml metadata
 
           Parameters
           ==========
           spec_dict: a dictionary with:
               name: the name of the folder (and Specification)
               workbook: the loaded workbook (or file to it)
               params: the original values in the configuration.yml for the folder
        '''
        spec_metadata = {}
        spec_post = frontmatter.Post('')

        # Skip over set of pre-defined fields
        if not skip_fields:
            skip_fields = []

        if not isinstance(skip_fields,list):
            skip_fields = [skip_fields]

        for spec_field in spec_dict:
            if spec_field not in skip_fields:
                spec_metadata[spec_field] = spec_dict[spec_field]

        spec_post.metadata = spec_metadata
        return spec_post

    def __create_spec_folder_struct(self, spec_name):
        '''create a spec folder and subdirectory for examples for a 'spec_name'
           only if it doesn't exist.

           Parameters
           ==========
           spec_name: the name of the specification
        '''
        # Individual specification folder under "docs/spec_files"
        spec_dir = os.path.join(self.md_files_path, spec_name)

        # Create if doesn't exist
        if not os.path.exists(spec_dir):
            os.makedirs(spec_dir)

        # Equivalent for "examples" subfolder
        spec_exp_dir = os.path.join(spec_dir, 'examples')
        if not os.path.exists(spec_exp_dir):
            os.makedirs(spec_exp_dir)

            with open(os.path.join(spec_exp_dir, "README.md"), "w") as example_file:
                example_file.write("## %s coding examples. \n" % spec_name)
                example_file.write("Folder that stores JSON-LD, RDFa or microdata examples.\n")
                example_file.write(">Examples will be added in a future map2model release.\n")            
                print("%s file structure created." % spec_name)

        # Either way, return the specification directory
        return spec_dir

    def __write_README(self, spec_md_folder, spec_dict):
        '''write a README for a particular spec_md_folder
 
           Parameters
           ==========
           spec_md_folder: a folder where a specification README should be written
           spec_dict: a dictionary with:
               name: the name of the folder (and Specification)
               workbook: the loaded workbook (or file to it)
               params: the original values in the configuration.yml for the folder
        '''
        spec_md_file_path = os.path.join(spec_md_folder, 'README.md')
        with open(spec_md_file_path, "w") as readme:
 
            # Look up some fields
            name = spec_dict['name']
            version = spec_dict['version']
            spec_type = spec_dict['spec_type']
            hierarchy = spec_dict['hierarchy']
            description = spec_dict['description'] 
            subtitle = spec_dict['subtitle'].strip()

            readme.write("## %s specification v. %s \n\n" % (name, version))
            readme.write("**%s** \n\n" % spec_type)

            for i_pos, step_hier in enumerate(reversed(hierarchy)):
                readme.write(step_hier)
                if i_pos < len(hierarchy)-1:
                    readme.write(" > ")
            if spec_type == "Type":
                readme_file.write(" > %s" % name)
            readme.write("\n\n**%s** \n" % subtitle)
            readme.write("\n# Description \n")
            readme.write("%s \n" % description)
            readme.write("# Links \n")
            readme.write("- [Specification](http://bioschemas.org/bsc_specs/%s/specification/)\n" % name)
            readme.write("- [Specification source](specification.html)\n")
            readme.write("- [Coding Examples](%s)\n" % spec_dict['gh_examples'])
            readme.write("- [GitHUb Issues](%s)\n" % spec_dict['gh_tasks'])
            readme.write("> These files were generated using [map2model](https://github.com/BioSchemas/map2model) Python Module.")
        
    def parse_front_matter(self):

        # Dictionary of the entries in configuration.yml with folder name as index
        self.specs_list = self.file_manager.get_specification_list(self.input_folder)
        all_specs = self.__get_specs_list()

        for spec_name, spec_dict in all_specs.items():

            # Create frontmatter post object with basic metadata
            temp_spec_post = self.__get_specification_post(spec_dict)

            if spec_dict['spec_type'] == 'Type':
                temp_spec_post.metadata['layout'] = 'new_type_detail'
            else:
                temp_spec_post.metadata['layout'] = 'new_spec_detail'

            md_fm_bytes = BytesIO()
            temp_spec_post.metadata['version'] = str(temp_spec_post.metadata['version'])
            frontmatter.dump(temp_spec_post, md_fm_bytes)
            spec_name = temp_spec_post.metadata['name']

            # Create folder structure (examples) and README.md
            spec_dir = self.__create_spec_folder_struct(spec_name)
            self.__write_README(spec_dir, spec_dict)

            # Write the final markdown frontmatter to specification.html
            with open(os.path.join(spec_dir, 'specification.html'), 'w') as outfile:
                temp_str = str(md_fm_bytes.getvalue(),'utf-8')
                outfile.write(temp_str)
                outfile.close()

            print ('%s MarkDown file generated.' % temp_spec_post.metadata['name'])

        print('Generation Process Complete. Output files are in %s' % self.md_files_path)
