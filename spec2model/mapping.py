from rdflib import ConjunctiveGraph
import csv
import os
import requests
import sys

# Loading Functions

def load_tsv(filename):
    '''load a tsv file using the csv default provided reader!

       Parameters
       ==========
       filename: the file name to load, will return list (rows) of
       lists (columns)
    '''
    rows = []
    with open(filename,'r') as tsv:
        content = csv.reader(tsv, delimiter='\t')
        for row in content:
            if row:
                rows.append(row)

    return rows


# RDF Functions

def __get_class_name(temp_uri):
    return temp_uri.replace("http://schema.org/","")


def __add_property(props_dic, prop_desc):
    sdo_uri="http://schema.org/"
    if prop_desc['prop_name'] in props_dic:
        t_prop_name = prop_desc['prop_name']
        props_dic[t_prop_name]['exp_type'].append(prop_desc['exp_type'].replace(sdo_uri,""))
    else:
        props_dic[prop_desc['prop_name']]=prop_desc
        props_dic[prop_desc['prop_name']]['exp_type'] = [prop_desc['exp_type'].replace(sdo_uri,"")]
    return props_dic


def __get_class_props(class_name, graph):
    print("Quering properties of  %s in Schema.org" % class_name)

    qres = graph.query("""prefix schema: <http://schema.org/>
                        select distinct * where {
                            ?property schema:domainIncludes  schema:%s .
                            ?property schema:rangeIncludes  ?exp_type .
                            ?property rdfs:label ?prop_name.
                            ?property rdfs:comment ?description
                        }""" % class_name)
    temp_dic = {}

    for row in qres:
        labels=row.labels.keys()
        labels_dic = {}
        print('Parsing %s property.' % row['prop_name'])
        for label in labels:
            labels_dic[label] = str(row[label]).replace('<a href=\"/docs/', '<a href=\"http://schema.org/docs/')
        temp_dic=__add_property(temp_dic, labels_dic)

    return temp_dic


def __get_parent_type(class_name, graph):

    print("Find parent type of %s in Schema.org" % class_name)

    qres = graph.query("""prefix schema: <http://schema.org/>
                          select ?supclass where{
                          ?class rdfs:label ?label .
                          ?class rdfs:subClassOf ?supclass .
                          filter (?label='%s')
                        }""" % class_name)
    resp_arr=[]

    for row in qres:
        resp_arr.append(str(row['supclass']))
    return resp_arr[0].replace('http://schema.org/', '')


def __get_properties(class_name, graph, properties):

    if(class_name=='Thing'):
        properties[class_name]=__get_class_props(class_name, graph)
        return properties
    else:
        temp_props = __get_class_props(class_name, graph)
        properties[class_name] = temp_props
        parent_type = __get_parent_type(class_name, graph)
        __get_properties(parent_type, graph, properties)


def get_properties_in_hierarchy(type_name):
    query_type = type_name
    g = ConjunctiveGraph()
    g.parse('http://schema.org/version/latest/schema.jsonld', format='json-ld')
    props_dic={}
    __get_properties(query_type, g, props_dic)
    return props_dic


def get_hierarchy(props_dic):
    type_hierarchy = []
    for h_type in props_dic:
        type_hierarchy.append(h_type)
    return type_hierarchy


def get_expected_type(expected_types):
    '''Function that receives an string with expected types
       and generates an array with each expected type
    '''
    expected_types = expected_types.strip()
    expected_types = expected_types.replace('\n', '')
    expected_types = expected_types.replace(' OR ', ' ')
    expected_types = expected_types.replace(' or ', ' ')
    expected_types = expected_types.replace(',', '')
    list_of_types = expected_types.split(" ")
    i = 0
    for etype in list_of_types:
        list_of_types[i] = etype.strip()
        i += 1

    return list_of_types


def _parse_controlled_vocabulary(temp_cont_vocab):
    cv_parsed = {'terms':[] , 'ontologies':[]}
    element_list = temp_cont_vocab.split(',')
    for element in element_list:
        if ':' in element:
            temp_onto = element.split(":",1)
            ontology = {}
            ontology['name'] = temp_onto[0].strip()
            ontology['url'] = temp_onto[1].strip()
            cv_parsed['ontologies'].append(ontology)
        elif element != '':
            element = element.replace('LIST - ', '').strip()
            temp_term = {}
            temp_term['name'] = element
            cv_parsed['terms'].append(temp_term)
    return cv_parsed


def get_row_value(field, row, headers, clean=True):
    value = ''
    for i in range(0, len(row)):
        if headers[i] == field:
            value = row[i]
            break
    
    if clean is True:
        value = value.strip().replace('\n', '')
    return value

def get_dict_from_row(row, headers):

    props = {}

    # Set Bioschemas attributes
    props['bsc_dec'] = get_row_value('BSC Description', row, headers)
    props['marginality'] = get_row_value('Marginality', row, headers)
    props['cardinality'] = get_row_value('Cardinality', row, headers)
    temp_cont_vocab = get_row_value('Controlled Vocabulary', row, headers)
    props['controlled_vocab'] = _parse_controlled_vocabulary(temp_cont_vocab)

    # Set schema.org attributes
    props['name'] = get_row_value('Property', row, headers)
    props['expected_type'] = get_row_value('Expected Type', row, headers) 
    props['expected_type'] = get_expected_type(props['expected_type'])
    props['sdo_desc'] = get_row_value('Description', row, headers)
    print (props['name'] + ':' + props['sdo_desc'] +'\n')
    if props['sdo_desc'] is None:
        props['sdo_desc'] = ' ';

    return props


def get_property_in_hierarchy(sdo_props, mapping_property):
    prop_type="new_sdo"
    for hierarchy_level in sdo_props:
        if mapping_property['name'] in sdo_props[hierarchy_level].keys():
            prop_type = hierarchy_level
            mapping_property['sdo_desc'] = sdo_props[hierarchy_level][mapping_property['name']]['description']
    return {'type':prop_type, 'property': mapping_property}


def get_formatted_props(sdo_props, mapping_props, spec_name, spec_type):
    all_props= []
    bsc_props = []

    # if type only get new properties from mapping file
    if(spec_type == "Type" or spec_type == "type"):
        for mapping_property in mapping_props:
            bsc_props.append(mapping_property['name'])
            temp_prop=get_property_in_hierarchy(sdo_props, mapping_property)
            if temp_prop['type'] == "new_sdo":
                temp_prop['property']['parent'] = spec_name
            all_props.append(temp_prop['property'])
        for sdo_prop in sdo_props:
            # now get all props from schema & make them such that _layout can use them
            for sdo_prop_prop in sdo_props[sdo_prop].keys():
                if sdo_props[sdo_prop][sdo_prop_prop]['prop_name'] not in bsc_props:
                    sdo_props[sdo_prop][sdo_prop_prop]['parent'] = sdo_prop
                    sdo_props[sdo_prop][sdo_prop_prop]['name'] = sdo_props[sdo_prop][sdo_prop_prop]['prop_name']
                    # sdo_props[sdo_prop][sdo_prop_prop]['bsc_dec'] = sdo_props[sdo_prop][sdo_prop_prop]['description']
                    sdo_props[sdo_prop][sdo_prop_prop]['sdo_desc'] = sdo_props[sdo_prop][sdo_prop_prop]['description']
                    sdo_props[sdo_prop][sdo_prop_prop]['expected_type'] = sdo_props[sdo_prop][sdo_prop_prop]['exp_type']
                    all_props.append(sdo_props[sdo_prop][sdo_prop_prop])
                else:
                    for i in all_props:
                        if i['name'] == sdo_props[sdo_prop][sdo_prop_prop]['prop_name']:
                            i['parent'] = sdo_prop
        return {'properties': all_props}

    # if profile
    for mapping_property in mapping_props:
        temp_prop=get_property_in_hierarchy(sdo_props, mapping_property)
        if temp_prop['type'] == "new_sdo":
            temp_prop['property']['parent'] = spec_name
        else:
            temp_prop['property']['parent'] = temp_prop['type']
        all_props.append(temp_prop['property'])

    return {'properties': all_props}


def get_mapping_properties(bioschemas_file):
    '''get_mapping_properties
       use the bioschemas field file and the specification type to
       return a list of type properties. The bioschemas file 
       should already be validated for correct headers.

       Parameters
       ==========
       bioschemas_file: the <Template> - Bioschemas.tsv file
    '''

    rows = load_tsv(bioschemas_file)
    headers = rows[0]
    type_properties = []
    
    for r in range(1,len(rows)):
        row = rows[r]
        
        # If we want to do checks for empty cells, do it here

        # If Expected Type, Marginality, and Cardinaity isn't empty 
        if row[1] != "" and rows[6] != "" and rows[7] != "":
            property_dict = get_dict_from_row(row, headers)
            type_properties.append(property_dict)

    return type_properties


class MappingParser:
    metadata = {}

    def __init__(self, metadata=None):
        if metadata != None:
            self.metadata = metadata

    def set_metadata(self, metadata):
        self.metadata = metadata


    def check_url(self, spec_url):
        '''check_url doesn't exit if the address isn't found, etc.
           it just adds the string "err_404" as metadata given these cases.
        '''
        if spec_url is None: 
            return "err_404"

        response = requests.get(spec_url)
        if response.status_code == 404:
            return "err_404"
        else:
            return spec_url

    def get_description(self, spec_file=None):

        if not spec_file:
            spec_file = self.metadata['specification_file']

        # Read in both, these are already validated
        spec_sheet = load_tsv(spec_file)

        # Generate values in advance
        name = self.metadata['name']
        gh_base = 'https://github.com/BioSchemas/specifications/tree/master'
        use_cases_url = self.metadata['use_cases_url']

        description = {}
        description['name'] = name
        print("Parsing %s Workbook" % description['name'])

        description['status'] = self.metadata['status']
        description['spec_type'] = self.metadata['spec_type']

        # Github Future Links
        description['gh_folder'] = '%s/%s' % (gh_base, name)
        description['gh_examples']= '%s/%s/examples' % (gh_base, name)
        description['gh_tasks'] = 'https://github.com/BioSchemas/bioschemas/labels/type%3A%20'+ name

        description['edit_url']='%s/%s/specification.html' % (gh_base, name)
        description['use_cases_url'] = self.check_url(use_cases_url)
        description['version'] = self.metadata['version']
        description['parent_type'] = self.metadata.get('parent_type', 'Thing')

        # Parse specification file
        description['subtitle'] = spec_sheet[1][1]
        description['description'] = spec_sheet[1][2]
        return description

    def get_mapping(self, spec_sheet=None, 
                          bioschemas_sheet=None):
        '''get a mapping, meanng the full properties given a specification sheet
           and a bioschemas sheet. If files aren't provided, the defaults defined
           at self.defaults.paths are used.

           Parameters
           ==========
           spec_sheet: the sheet with basic information (description, name, etc.)
           bioschemas_sheet: sheet (tsv) with bioschemas fields
        '''

        print("Parsing %s." % self.metadata['name'])

        spec_description = self.get_description(spec_sheet)
        if bioschemas_sheet is None:
            bioschemas_sheet = self.metadata['bioschemas_file']

        try:
            ptype = spec_description['parent_type']
            sdo_props = get_properties_in_hierarchy(ptype)
        except IndexError as e:
            print('Error finding parent structure! Is %s a valid entity?' %ptype)
            sys.exit(1)

        spec_description['hierarchy'] = get_hierarchy(sdo_props)
        spec_description['hierarchy'].reverse()
        print_hierarchy = ' > '.join(spec_description['hierarchy'])
        print("Prepared schema.org properties for hierarchy %s" % print_hierarchy)
        print("Classifing %s properties" % spec_description['name'])
        mapping_props = get_mapping_properties(bioschemas_sheet)

        formatted_props = get_formatted_props(sdo_props, 
                                              mapping_props, 
                                              spec_description['name'], 
                                              spec_description['spec_type'])

        spec_description.update(formatted_props)

        return spec_description
