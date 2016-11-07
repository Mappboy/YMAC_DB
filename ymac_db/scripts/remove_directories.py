#! /usr/bin/env python
"""
Module to remove empty folders recursively. Can be used as standalone script or be imported into existing script.
Need to make sure we are only checking folders that contain 'Heritage Survey' or 'Pre 2013 Final Reports'
"""

import os
import sys

def remove_empty_folders(path,removeRoot=True):
    """Function to remove empty folders"""
    if not os.path.isdir(path) or "2016" in path:
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and removeRoot:
        print("Removing empty folder:", path)
        # os.rmdir(path)


def usageString():
    """Return usage string to be output in error cases"""
    return u'Usage: {0:s} directory [removeRoot]'.format(sys.argv[0])


if __name__ == "__main__":
    removeRoot = True
    claim_dir = r"Z:\\Claim Groups\\"

    for f in os.listdir(claim_dir):
        hs = os.path.join(claim_dir,f,"Heritage Surveys")
        pre = os.path.join(claim_dir,f,"Pre 2013 Final Reports")
        if os.path.isdir(hs):
            remove_empty_folders(hs, removeRoot)
        if os.path.isdir(pre):
            remove_empty_folders(pre, removeRoot)