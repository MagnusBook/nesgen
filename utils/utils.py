import argparse


def get_args():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        '-c', '--config',
        metavar='C',
        default='None',
        help='The Configuration file'
    )
    argparser.add_argument(
        '-p', '--preprocess',
        action='store_true',
        help='Determines if statematrices should be created. This must be done the first time'
    )
    args = argparser.parse_args()
    return args
