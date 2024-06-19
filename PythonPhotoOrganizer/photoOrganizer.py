"""Script to organizer pictures in a directory based on the year the were taken

Organizes all the pictures in the current directory of the script by creating a subdirectory for each year that has at least
one picture taken in that date

Can be imported as a module to use the functions

Usage: 
    python photoOrganizer.py

Author: Arhernav
"""

import os
from PIL import Image
from PIL.ExifTags import TAGS
import sys
import time
import shutil




def organize():
    """Main method to organize the pictures
    """
    print("Organizando directorio: ", os.getcwd()) 
    
    #Preparation
    currentDir= os.getcwd() #Current directory
    currentFiles = os.listdir(currentDir) #All files in currentDir including sub directories
    subDir = [dir for dir in currentFiles if os.path.isdir(dir)] # All sub directories. For faster check in case of many subdirectories

    for file in currentFiles: 
        # Divide in 2 cases
        if os.path.isdir(file): continue #skip directories

        #Get date
        #jpg and jpeg have exif
        #gif and png dont
        if file.endswith('.jpg') or file.endswith('.jpeg'):
            try: 
                takenYear = getYear(file)
            except AttributeError:
                takenYear = getAltYear(file)
            except KeyError:
                takenYear = getAltYear(file)
            except: 
                print('Error on file: ', file)
                continue

        elif file.endswith('.gif') or file.endswith('.png'):
            takenYear = getAltYear(file)
        else: 
            print('Ommited file: ', file)
            continue

        ##Once we have date
        if takenYear in subDir:
            shutil.move(file, os.path.join(takenYear, file))
            print(file, os.path.join(takenYear, file), 'Dir')
        else:
            if not os.path.exists(takenYear): os.mkdir(takenYear) #double check in case
            subDir = subDir + [takenYear]
            print('Created ' + takenYear)
            print(file, os.path.join(takenYear, file), 'noDIr')
            shutil.move(file, os.path.join(takenYear, file))


def getYear(path):
    """Returns a string with the picture date
    param: 
        path - str: Path to the file (Assumed to exist)
    return: 
        str - Year the photo was taken according to exif data
    raises: 
        AttributeError: when image has no exif data
        KeyError: When image has no date
    """
    exif = Image.open(path)._getexif()
    if not exif:
        raise AttributeError(f'Image {path} does not have EXIF data.')
    if 36867 not in exif:
        raise KeyError(f'Image {path} does not have date data.')
    date = exif[36867].replace(':',' ').split()
    return date[0]

    



def getAltYear(path):
    """ When an image does not have a taken date, we compare the creation and modified date of the file
    param: 
        path: str - Path to the file (Assumed to exist)
    return: 
        str - modified year if modified is before created; else created year
    """
    modified = os.path.getmtime(path)
    created = os.path.getctime(path)
    if modified < created: 
        date = time.localtime(modified)
        return str(date[0])
    else: 
        date = time.localtime(created)
        return str(date[0])
    


def main():
    """Main method in case of exanding the program in the future
    """
    print("Usar directorio ", os.getcwd(), "?")
    if input("") == "Yes":
        organize()

if __name__ == "__main__":
    main()
