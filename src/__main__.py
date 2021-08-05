import sys
import argparse
import src.data.purpleair_data_retriever as data_retriever


def download(start=None, end=None, **kwargs):
    # data_retriever.main(start=start,end=end)
    print(start)
    print(end)
    

def main():
    parser = argparse.ArgumentParser(prog='bomp')
    subparsers =  parser.add_subparsers()
    
    parser_download =  subparsers.add_parser('download')
    parser_download.add_argument('-s','--start-date', type=str, dest='start',help='Start date of data.')
    parser_download.add_argument('-e','--end-date', type=str, dest='end', help='End date of data.')
    parser_download.set_defaults(func=download)

    
    parser_version =  subparsers.add_parser('version')
    parser_version.add_argument('-stafrt', type=str)
    parser_version.add_argument('-enfd', type=str)

    args = parser.parse_args()
    args.func(**vars(args)) # This will also pass an unused func variable, but **kwargs takes care of it.

if __name__ == '__main__':
    sys.exit(main())