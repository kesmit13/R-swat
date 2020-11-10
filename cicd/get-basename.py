#!/usr/bin/env python

'''
Return the basename for the package

If no release is specified, only the short version of the basename is returned.

    R-swat-{version}

If a release is specified, the complete basename is returned. If no platform is
specified, the platform the program is running on is used.

    R-swat-{version}+{release}-{platform}

'''

import argparse
import glob
import os
import platform
import re
import sys


def get_platform():
    ''' Return the Anaconda platform name for the current platform '''
    plat = platform.system().lower()
    if 'darwin' in plat:
        return 'osx-64'
    if plat.startswith('win'):
        return 'win-64'
    if 'linux' in plat:
        machine = platform.machine().lower()
        if 'x86' in machine:
            return 'linux-64'
        if 'ppc' in machine:
            return 'linux-ppc64le'
    return 'unknown'


def print_err(*args, **kwargs):
    ''' Print a message to stderr '''
    sys.stderr.write(*args, **kwargs)
    sys.stderr.write('\n')


def main(args):
    ''' Main routine '''

    version = None
    tk_version = None

    init = glob.glob(os.path.join(args.root, 'DESCRIPTION'))[0]
    with open(init, 'r') as init_in:
        for line in init_in:
            m = re.search(r'''^Version\s*:\s*(\S+)''', line)
            if m:
                version = m.group(1)

            m = re.search(r'''^TKVersion\s*:\s*(\S+)''', line)
            if m:
                tk_version = m.group(1)
                if tk_version == 'none':
                    tk_version = 'REST-only'

    if version:
        if args.full:
            print('R-swat-{}+{}-{}'.format(version, tk_version, args.platform))
        else:
            print('R-swat-{}'.format(version))
        return 0

    print_err('ERROR: Could not find DESCRIPTION file.')

    return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.strip())

    parser.add_argument('root', type=str, metavar='<directory>', nargs='?', default='.',
                        help='root directory of R package')

    parser.add_argument('--platform', '-p', type=str, metavar='<platform>',
                        choices=['linux-64', 'osx-64', 'win-64', 'linux-ppc64le'],
                        default=get_platform(),
                        help='platform of the resulting package')
    parser.add_argument('--full', '-f', action='store_true',
                        help='return the full variant of the basename '
                             'including TK version and platform')

    args = parser.parse_args()

    sys.exit(main(args) or 0)
