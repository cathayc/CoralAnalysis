from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from analyzeFromFile import obtainCurrentCoralData
from analyzeObj import analyzeObject
from coralObject import *

import zipfile
import os
import winshell

gauth = GoogleAuth()
gauth.LoadCredentialsFile("D:\Members\Cathy\mycreds.txt")
drive = GoogleDrive(gauth)

drive_output_file_id = '1dRIvWyhkQQces8LVg9sfLnY9iS9JcQqW'
drive_output_filepath = 'D:\Members\Cathy\coralAnalysis\driveOutputData.txt'

def main():
    # Get the list of files from shared Coral Model drive
    file_list = drive.ListFile({'q': "'14twSsD2RWNGXTXWDJ3i745fA0HbKBfnb' in parents and trashed=false"}).GetList()

    for file in file_list:
        if file['title'].startswith('Copy of Acropora solitaryensis - 2510'):
            # Extracted file to be analyzed location
            coral_file_path = ""

            # Download zipped file and obtain file path
            path_to_zip_file = downloadZipFile(file)
            
            # Unzip file
            with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                # Determine the desired and extract .obj file
                extractFileName = determineExtractFileName(zip_ref)
                zip_ref.extract(extractFileName, 'D:\Members\Cathy')
                coral_file_path = 'D:\Members\Cathy\{}'.format(extractFileName)
                print("Coral file path: {}\n".format(coral_file_path))

            # Now that the file is extracted, delete the zip file
            removeFile(path_to_zip_file)

            # Analyze the coral file and write result
            analyzeAndWrite(coral_file_path, drive_output_filepath)

def analyzeAndWrite(coralFilePath, outputFilePath):
    with open(outputFilePath, 'a') as outputFile:
        if os.path.getsize(outputFilePath) == 0:
            outputFile.write("File Name: | Surface Area (mm^2): | Volume (mm^3): | OnlineFD: | FileFD: | Analysis time (seconds):\n")
        currentCoral = analyzeObject(coralFilePath)
        outputFile.write(obtainCurrentCoralData(coralFilePath, currentCoral))


def removeFile(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist. File path: " + path)

def determineExtractFileName(zip_ref):
    listOfFiles = zip_ref.namelist()
    objFileNames = [fileName for fileName in listOfFiles if fileName.endswith('obj')]
    objFileNames.sort()
    extractFileName = objFileNames[-1]
    return extractFileName

""" Download the zip coral file
    Returns file path """
def downloadZipFile(file):
    title = file['title'].strip('Copy of').strip('.zip')
    file_id = file['id']
    destination = "D:\Members\Cathy\{}.zip".format(title)

    # Check if file already exists
    if os.path.exists(destination):
        print("The file already exists")
    else:
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(destination)
        print('file {} downloaded!'.format(title))
    
    # Return destination of the file
    return destination

if __name__ == "__main__":
    main()