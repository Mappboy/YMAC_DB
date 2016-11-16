"""
Utility functions should go in here
"""
import os
from datetime import timedelta


def emit_week(day):
    """
    Given a day calculate from the Sunday - to the past Monday
    :param day: must be datetime object
    :return:
    """
    day_of_week = day.weekday()

    # tosunday
    to_beginning_of_week = timedelta(days=day_of_week)
    beginning_of_week = day - to_beginning_of_week - timedelta(days=1)

    to_end_of_week = timedelta(days=-6)
    end_of_week = beginning_of_week + to_end_of_week

    return (end_of_week, beginning_of_week)



def removeEmptyFolders(path, removeRoot=True):
    '''
    Function to remove empty folders
    :param path:
    :param removeRoot:
    :return:
    '''
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                removeEmptyFolders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and removeRoot:
        print("Removing empty folder:", path)
        os.rmdir(path)
