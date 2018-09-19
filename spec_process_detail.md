# Bioschemas Specification Process
This repository will help people interested in defining a Bioschemas Specification. Here you will find all the templates and documentation needed to be familiar with the Specification Process. This process starts with the Use Case Study and finish with the RDFa generation.

![Bioschemas Specification Process](../master/docs/img/specification_process.jpg)
> If you want to modify the flow chart, change the image file called **specification_process.jpg** in the *docs > img* folder.


In the following README you have an explanation of the process needed to create a Bioschemas Specification. There are 3 steps:
1. Use Case Study
1. Mapping
1. Specification

> For this explanation, the **Bioschemas Tool Specification** will be used as an example.

## USE CASE STUDY
> Section under construction.

## MAPPING

Once you have defined Use Cases you should start to consider what properties are needed to describe the data from your use case. Please try to reuse existing Schema.org properties (and definitions) where possible. It may be benficial to try and extend (or specialise) an existing Schema.org Type.  You may find reading other Bioschemas.org specifications useful.

To record the decisions your team has reached follow these steps:

1. Make a copy of the [mapping template](https://drive.google.com/open?id=0Bw_p-HKWUjHoQ2RkUUthWVd3RG8) naming the file **<SPECIFICATION_NAME> mapping**. This mapping file should be placed in a folder called **<SPECIFICATION_NAME>**, which should be located in the gDrive folder *bioschemas > specifications*
  > Copy the spreadsheet file not the text document file.

2. Open the Mapping template and you will find the following structure.

![Bioschemas Tools Mapping empty file](../master/docs/img/mapping_empty_file.png)
  + **schema.org**: These columns are copy-pasted from a schema.org type definition page.
    - **Property:** Name of the property from the selected schema.org type.
    - **Expected Type:** Expected type for the property suggested by schema.org selected type.
    - **Description:**: Description of the property from the schema.org vocabulary for the selected type.
  + **bioschemas:** These columns are defined for the properties that will be in the Bioschemas Specification file.
    - **BSC Description:** If is considered an additional description for the property, here can be aded an additional text that complements the schema.org description.
    - **Marginality:** The template gives three options for the property specification of the new Bioschemas Type: Minimum, Recommended or Optional. 
    - **Cardinality:**	The template gives you the two possible cardinalities in a Bioschemas Specification (ONE or Many).
    - **Controlled Vocabulary:** 
      This field contains a list of terms or ontologies that provide values for this property.
      
  - **USE CASE GENERAL INFORMATION**
    + **USE CASE NAME**
    + **USE CASE URL**
    + **CONTRIBUTOR1, CONTRIBUTOR2,...**: List of Contributors that worked in the description of this Use Case.
  - **USE CASE SPECIFIC INFORMATION** 
    + **Name:** Name for the Use Case (This field is only needed to double check or compare the diferent names that this property has across the different Use Cases, and with this define the BioSchema property name).
    + **Content Example:** Example of the Use Case.
    + **UseCase:** Three possible options for the mapping: 
      - **Match:** If the use case matches with a Schema.org property.
      - **No Match:** If the property doesn't match with the Schema.org Property.
      - **Partial Match**: If the Use Case Property doesn't match perfectly but is a close connection with the Schema.org property.
      
3. Go to the schema.org and find the definition of the type you want to reuse in the Bioschemas Structure.
In their Use Case Study, the Tools Specification identified that the Schema.org Type [SoftwareApplication](http://schema.org/SoftwareApplication) was the best fit for their use cases.
![Schema.org Type Definition](../master/docs/img/schema_org_type.png)

4. Copy the Type definition table, starting from the first Property, but **do not copy the table headers**.
For the Tool example, SoftwareApplication should look like this:

![Copy Schema.org Type Definition](../master/docs/img/schema_org_type_copy.png)

5. Then paste into your mapping Spreadsheet starting in **A7 Cell**.
For the Tools Specification you would have something like this:

![Pasting Schema.org Type Definition to the mapping Template](../master/docs/img/schema_org_paste_template.png)


6. Fill all the Use Cases for this Specification.
For the Tools Specification you would have something like this:
![Filling the Use Cases in the Mapping Template](../master/docs/img/fill_mapping_template_UC.png)

  > The template gives you diferent colours for the Use Case Matching (Dark blue for Match, light blue for Partial Match and light orange for No Match).

7. Fill the Bioschemas Fields
  + **bioschemas:** These columns are defined for the properties that will be in the Bioschemas Specification file.
    1. **BSC Description:** A short description of what this propery describes.
    1. **Marginality:** The template gives three options for the property specification of the new Bioschemas Type: Minimum, Recommended or Optional. 
    1. **Cardinality:**	The template gives you the two possible cardinalities in a Bioschemas Specification (ONE or Many).
    1. **Controlled Vocabulary (CV):**  This field contains a list of terms and/or ontologies. A *term* is just text that represents the value expected and an *ontology* is described using the form: *ontology_name : ontology_uri*.

      **Examples:**

      - **Term list**
            ```term1, term2, term3```

      - **Ontology list**
            ```uberon: http://purl.obolibrary.org/obo/uberon.owl, emap: http://purl.obolibrary.org/obo/emap.owl```

      - **Mixed list**
            ```uberon: http://purl.obolibrary.org/obo/uberon.owl, term1, onto2:http: //onto2.com, term2, emap: http://purl.obolibrary.org/obo/emap.owl, term3``` 
            For the Tools Specification you would have something like this.
               ![Fill the Bioschemas Fields](../master/docs/img/bioschemas_mapping.png)

8. Go to the **Bioschemas fields** sheet to view the summary of your mapping
For the Tools Specification you would have something like this:

![Mapping Summary](../master/docs/img/mapping_summary.png)


## SPECIFICATION

Your mapping file is converted into a specification that can be displayed on the Bioschema's web pages by the **map2model** process. To discover more about it please read [map2model repository](https://github.com/BioSchemas/map2model).


>Find a detailed description of this process in [Specifications Repository](https://github.com/BioSchemas/specifications).

