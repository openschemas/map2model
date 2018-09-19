#!/usr/bin/env python3

import spec2model.markdown_parser as md_parser
import argparse
import sys
import os

def get_parser():
    parser = argparse.ArgumentParser(description="map2model")

    parser.add_argument("--config", dest='config', 
                         help='configuration.yml file, defaults to configuration.yml in folder', 
                         type=str, default=None)

    parser.add_argument("--folder", dest='specs', 
                         help='folder with input specification subfolders', 
                         type=str, default=None)

    parser.add_argument("--output", dest='outfolder', 
                         help='folder to write output specification subfolders', 
                         type=str, default=None)

    return parser


def main():
    '''entrypoint for run.py script.
    '''

    parser = get_parser()
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    # Set the default specifications folder and configuration
    folder = args.specs
    if not folder:
        folder = 'specifications'

    outfolder = args.outfolder
    if not outfolder:
        outfolder = 'docs/spec_files'

    outfolder = os.path.abspath(outfolder)
    folder = os.path.abspath(folder)

    config = args.config
    if not config:
        config = 'spec2model/configuration.yml'
        
    # Output folder we may need to make
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    print('Configuration file set to %s' % config)
    print('Output folder set to %s' % outfolder)
    print('Input folder set to %s' % folder)

    # Both must exist
    for path in [config, folder]:
        if not os.path.exists(path):
            print('Error, %s not found.' % path)
            sys.exit(1)


    bsc_md_parser = md_parser.FrontMatterParser(input_folder=folder,
                                                output_folder=outfolder,
                                                config_file_path=config)
    bsc_md_parser.parse_front_matter()
    

if __name__ == '__main__':
    main()
