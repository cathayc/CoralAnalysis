""" 
*** DEPRECATED AS OF MAY 13, 2024 ****
No longer supports google drive file downloads

This file allows user to analyze from Google Drive by 
1. Logging into drive with the credential file
2. Downloading all the files onto the computer with a Zip filee
3. Iterating through all the files (download one, analyze it, write information on an output file, then delete the original file) with analyzeObj
4. Uploading the result file onto Drive.

Cathy was primarily working with her directory, D:\Members\Cathy
Feel free to change that directory to whatever it is that you'd like.
This file primarily uses DownloadAllCoralFiles, which downloads each individually, runs analysis, upload result, then delete. 
You can go ahead and disregard DownloadCoralFile. It was used earlier in testing.
"""

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from helpers import analyzeObject, analyzeFD
from coralObject import *

import zipfile
import os
import shutil
import winshell
import time
import xlsxwriter
import csv

gauth = GoogleAuth()
gauth.LoadCredentialsFile("D:\Members\Cathy\mycreds.txt")
drive = GoogleDrive(gauth)

coral_file_directory = 'D:\Members\Cathy\coralFiles'
drive_input_id = '14twSsD2RWNGXTXWDJ3i745fA0HbKBfnb'
output_filepath = 'D:\Members\Cathy\coralAnalysis\driveOutputDataCombined.txt'
drive_output_file_id = ''

def main():
    #first, request the information we need. If the user has already specified in the variable declarations, then this isn't necessary
    requestInformation()
    #Then, download all coral files in the drive
    downloadAllCoralFiles(drive_input_id, coral_file_directory)

"""
    Requesting the information from the user.
    Information requested:
        drive_input_id
        coral_file_directory
        output_filepath
        output_filepath (whether user wants to write the result to drivee. If they do, then ask for drive_output_file_id)
"""
def requestInformation():
    global coral_file_directory, output_filepath, drive_input_id, drive_output_file_id
    infoRequested = input("Press y if the input is already specified, and n if not: ")
    if infoRequested=='n':
        drive_input_id = input("The ID of your input drive folder: ")
        coral_file_directory = input("Where would you like your downloaded corals to be stored: ")
        output_filepath = input("What would you like your output filepath to be: ")
        writeToDrive = input("Would you like to write your output to a file on drive? (y/n) ")
        if writeToDrive == 'y':
            drive_output_file_id = input("Drive output file ID (If you regretted this decision, input n): ")
        if writeToDrive == 'n':
            drive_output_file_id = ''

"""
    Given then coral file directory, each coral file (in file_list), then run the analysis on them. 
"""
def downloadAllCoralFiles(drive_id, coral_file_directory):
    # Get the list of files from shared Coral Model drive
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(drive_id)}).GetList()

    for file in file_list:
        if file['title'].startswith('Copy of'):

            # Download zipped file and obtain file path
            path_to_zip_file, title, file_already_exists = downloadZipFile(file)
            
            # If coral file doesn't already exist in directory, unzip file
            if file_already_exists:
                print("Skipping this download and extract.\n")
            else:
                with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                    # Determine the desired and extract .obj file (lowest resolution)
                    extractFileName = determineExtractFileName(zip_ref)
                    filename = os.path.basename(extractFileName)
                    print("The desired file to extract: " + filename)
                    # skip directories 
                    if not filename:
                        continue

                    # copy file (taken from zipfile's extract)
                    source = zip_ref.open(extractFileName)
                    targetpath = os.path.join(coral_file_directory, '{}.obj'.format(title))
                    target = open(targetpath, "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
                    
                    #zip_ref.extract(extractFileName, 'D:\Members\Cathy')
                    
                    print("Coral file path: {}\n".format(os.path.abspath(targetpath)))

                    #analyze the coral
                    analyzeFile(targetpath)
                    removeFile(targetpath)

                # Now that the file is extracted, delete the zip file.
                removeFile(path_to_zip_file)
"""
    Given a zip file of all coral files, download 1 single coral file. We do this for every single file in the directory.
"""
def downloadCoralFile(fileNum):
    extracted_location = ""
    zip_coral_file_path = coral_file_directory+'.zip'
    with zipfile.ZipFile(zip_coral_file_path, 'r') as zip_ref:
        for coral_name in zip_ref.namelist():
            if coral_name.endswith('{}.obj'.format(fileNum)):
                filename = os.path.basename(coral_name)
                print("filename: " + filename)
                # skip directories 
                if not filename:
                    continue

                # copy file (taken from zipfile's extract)
                source = zip_ref.open(coral_name)
                target = open(os.path.join('D:\Members\Cathy', coral_name), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
                extracted_location = target.name
                print("Coral file path: {}\n".format(extracted_location))

                # Show that filee is extracted.
                print("File is extracted.")

"""
    Iterate through the coral files in the zip file to run analysis.
"""
def iterateAndAnalyzeZip(zip_coral_file_path):
    extracted_location = ""
    
    with zipfile.ZipFile(zip_coral_file_path, 'r') as zip_ref:
        for coral_name in zip_ref.namelist():
            filename = os.path.basename(coral_name)
            print("filename: " + filename)
            # Skip directories 
            if not filename:
                continue

            # Copy file (taken from zipfile's extract)
            source = zip_ref.open(coral_name)
            target = open(os.path.join('D:\Members\Cathy', coral_name), "wb")
            with source, target:
                shutil.copyfileobj(source, target)
            extracted_location = target.name
            print("Coral file path: {}\n".format(extracted_location))

            # Now that the file is extracted, run analysis on the file
            print("File is extracted. About to analyze.")
            currentCoral = analyzeObject(extracted_location)
            print(obtainCurrentCoralData(currentCoral))

            # Write the data obtained from running analysis on the coral onto the specified file
            writeAndUploadData(currentCoral)
            
            # Finally, delete the file
            removeFile(extracted_location)

def analyzeFile(filepath):
    currentCoral = analyzeObject(filepath)
    print(obtainCurrentCoralData(currentCoral))
    writeAndUploadData(currentCoral)

def obtainCurrentCoralData(currentCoral):
    if currentCoral==None:
        return "File not found, please try another file!\n"
    else:
        coralName = currentCoral.coralName
        sa=currentCoral.surfaceArea
        volume=currentCoral.volume
        numVertices = currentCoral.numVertices
        numEdges = currentCoral.numEdges
        numFaces = currentCoral.numFaces
        analysisTime = currentCoral.analysisTime
        onlineFD = currentCoral.onlineFD
        reichartFD = currentCoral.reichartFD
        [boundingLength, boundingWidth, boundingHeight]=currentCoral.findBoundBox()
        return str(coralName) + " | " + str(sa) + " | " + str(volume)   + " | " + str(numVertices)   + str(numEdges)   +  " | " + str(numFaces)   + " | " + str(onlineFD) + " | " + str(reichartFD) + " | " + str(analysisTime) +"\n"

def writeAndUploadData(currentCoral):
    info_to_append = ""

    # Open local file
    with open(output_filepath, 'a') as outputFile:
        if os.path.getsize(output_filepath) == 0:
            info_to_append = "File Name: | Surface Area (mm^2) | Volume (mm^3) | bucketFD | FileFD | numVertices | boundLength | boundWidth | boundHeight | myX | myY\n"
        coralName = currentCoral.coralName
        sa = currentCoral.surfaceArea
        vol = currentCoral.volume
        bucketFD = currentCoral.bucketFD
        reichartFD =  currentCoral.reichartFD
        numV = currentCoral.numVertices
        boundLength, boundWidth, boundHeight = currentCoral.findBoundBox()
        myX, myY = currentCoral.bucketXY
        info_to_append += "{} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {}\n".format(coralName, sa, vol, bucketFD, reichartFD, numV, boundLength, boundWidth, boundHeight, myX, myY)

        # Write to local file first
        outputFile.write(info_to_append)
        print("Successfully wrote to output file")
    
    # Update drive file
    #drive_file = drive.CreateFile({'id': drive_output_file_id})
    #content  = drive_file.GetContentString()
    #content = content + info_to_append
    #drive_file.SetContentString(content)
    #drive_file.Upload()




def removeFile(path):
    if os.path.exists(path):
        os.remove(path)
        print("The file is removed. Original file path: " + path)
    else:
        print("The file does not exist. File path: " + path)
 
"""
    Sometimes there are multiple simplified versions of the coral. This method determines the most simplified .obj file name
"""
def determineExtractFileName(zip_ref):
    listOfFiles = zip_ref.namelist()
    objFileNames = [fileName for fileName in listOfFiles if fileName.endswith('.obj')]
    objFileNames.sort()
    if len(objFileNames) == 0:
        return ""
    else:
        return objFileNames[-1]

#   Download the zip coral file
#   Returns file path """
def downloadZipFile(file):
    title = file['title'].strip('Copy of').strip('.zip')
    file_id = file['id']
    destination = "D:\Members\Cathy\{}.zip".format(title)
    file_already_exists = False
    
    # Check if zip file already exists
    if os.path.exists(destination):
        file_already_exists = True
        print("The file already exists: {}".format(destination))

    # Check if extracted coral file already exists in coral directory
    elif os.path.exists('{}\\{}'.format(coral_file_directory, title)) or os.path.exists('{}\\{}'.format(coral_file_directory, title)):
        print('The specific coral file already exists in directory: {}\\{}'.format(coral_file_directory, title))
        file_already_exists = True

    else:
        print("Trying to download {}".format(title))
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(destination)
        print('file {} downloaded as zip!'.format(title))
    
    # Return destination of the file
    return destination, title, file_already_exists

"""
   Move all files of a certain extension from current directory to new directory
   Usage: move all files run by processOBJ to a new folder
"""
def moveToDirectory(file_extension, current_directory, new_directory):
    for file in os.listdir(current_directory):
        if not os.path.isfile(current_directory + "\\" +file):
            continue

        head, tail = os.path.splitext(file)
        if tail=='.txt':
            src = os.path.join(current_directory, file)
            dst = os.path.join(new_directory, file)

            if not os.path.exists(dst): # check if the file doesn't exist
                print("{} moved from {} to {}".format(file, current_directory, new_directory))
                os.rename(src, dst)

"""
   Sometimes the download isn't all in .obj. Make all files without an extension an .obj file
"""
def makeAllObj (current_directory):
    root = current_directory
    for file in os.listdir(current_directory):
        print(file)
        if not os.path.isfile(current_directory + "\\" +file):
            continue

        head, tail = os.path.splitext(file)
        if not tail:
            src = os.path.join(root, file)
            dst = os.path.join(root, file + '.obj')

            if not os.path.exists(dst): # check if the file doesn't exist
                os.rename(src, dst)

#   Returns the size of the directory in gigabytes
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                #print('{} has size {}'.format(f, os.path.getsize(fp)))
                total_size += os.path.getsize(fp)
    # Convert from bytes to gigabytes
    return total_size/ 1073741824

if __name__ == "__main__":
    main()