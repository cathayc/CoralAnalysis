from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from analyzeObj import analyzeObject, analyzeFD
from coralObject import *

import zipfile
import os
import shutil
import winshell
import time

gauth = GoogleAuth()
gauth.LoadCredentialsFile("D:\Members\Cathy\mycreds.txt")
drive = GoogleDrive(gauth)

coral_file_directory = 'D:\Members\Cathy\coralFiles'
jessica_file_directory = 'D:\Members\Cathy\JessicaCoralFiles'
drive_input_id = '14twSsD2RWNGXTXWDJ3i745fA0HbKBfnb'
drive_output_file_id = '11ZrwyPtHLqCkfrClcg_46AjS9HLtC3Jw'
output_filepath = 'D:\Members\Cathy\coralAnalysis\driveOutputDataCombined.txt'
output_file_header = "File Name: | Surface Area (mm^2) | Volume (mm^3) | myFD | OnlineFD | FileFD | numVertices | boundLength | boundWidth | boundHeight | myX | myY\n"

def main():	
    # First, download all coral files and execute it on Jessica's program
    downloadAllCoralFiles(drive_input_id, coral_file_directory)

    # Wait till user is done with running Jessica's program
    user_done = "n"
    while user_done != "y":
        user_done = input("Done running Jessica's program on every coral? (y/n)")
    
    # Move all jessica's file to a new directory
    print("Going to move all Jessica's file to Jessica's directory: {}".format(jessica_file_directory))
    moveToDirectory('.txt', coral_file_directory, jessica_file_directory)

    # Zip coral file directory and compare the size change
    zip_coral_file_path = coral_file_directory+'.zip'
    if os.path.exists(zip_coral_file_path):
        print("Zipped coral files already exist at: " + zip_coral_file_path)
    else:
        unzippedDirectorySize = get_size(coral_file_directory)
        shutil.make_archive('..\\coralFiles', 'zip', '..\\coralFiles')
        zippedDirectorySize = os.stat(zip_coral_file_path).st_size
        print("Current coral file directory size: {}\nNew coral file directory size: {}\nSpace saved: {:.0%}".format(unzippedDirectorySize, zippedDirectorySize, (unzippedDirectorySize-zippedDirectorySize)/unzippedDirectorySize))

    # Iterate all zipped files and analyze the coral
    iterateAndAnalyzeZip(zip_coral_file_path)

def iterateAndAnalyzeZip(zip_coral_file_path):
    extracted_location = ""
    # Start timer to analyze performance
    
    with zipfile.ZipFile(zip_coral_file_path, 'r') as zip_ref:
        for coral_name in zip_ref.namelist():
            start_time = time.time()
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

            # Now that the file is extracted, run analysis on the file
            print("File is extracted. About to analyze.")
            currentCoral = analyzeObject(extracted_location)
            print(obtainCurrentCoralData(currentCoral))
            writeAndUploadData(currentCoral, output_filepath, drive_output_file_id)
            
            # Finally, delete the file
            removeFile(extracted_location)
            end_time = time.time()
            print("Analysis time: {}".format(end_time-start_time))

def writeAndUploadData(currentCoral, output_filepath, drive_output_file_id):
    info_to_append = ""

    # Open local file
    with open(output_filepath, 'a') as outputFile:
        if os.path.getsize(output_filepath) == 0:
            info_to_append = "File Name: | Surface Area (mm^2) | Volume (mm^3) | myFD | OnlineFD | FileFD | numVertices | boundLength | boundWidth | boundHeight | myX | myY\n"
        coralName = currentCoral.coralName
        sa = currentCoral.surfaceArea
        vol = currentCoral.volume
        myFD = currentCoral.myFD
        onlineFD  = currentCoral.onlineFD
        fileFD =  currentCoral.fileFD
        numV = currentCoral.numVertices
        boundLength, boundWidth, boundHeight = currentCoral.findBoundBox()
        myX, myY = currentCoral.myXY
        info_to_append += "{} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {}\n".format(coralName, sa, vol, myFD, onlineFD, fileFD, numV, boundLength, boundWidth, boundHeight, myX, myY)

        # Write to local file first
        outputFile.write(info_to_append)
    
    # Update drive file
    drive_file = drive.CreateFile({'id': drive_output_file_id})
    content  = drive_file.GetContentString()
    content = content + info_to_append
    drive_file.SetContentString(content)
    drive_file.Upload()

def downloadAllCoralFiles(drive_id, coral_file_directory):
    # Get the list of files from shared Coral Model drive
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(drive_id)}).GetList()

    for file in file_list:
        if file['title'].startswith('Copy of'):
            # Extracted file to be analyzed location
            coral_file_path = ""

            # Download zipped file and obtain file path
            path_to_zip_file, title, file_already_exists = downloadZipFile(file)
            
            # If coral file doesn't already exist in directory, unzip file
            if file_already_exists:
                print("Skipping this download and extract.\n")
            else:
                with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                    # Determine the desired and extract .obj file
                    extractFileName = determineExtractFileName(zip_ref)
                    filename = os.path.basename(extractFileName)
                    print("filename: " + filename)
                    # skip directories 
                    if not filename:
                        continue

                    # copy file (taken from zipfile's extract)
                    source = zip_ref.open(extractFileName)
                    target = open(os.path.join(coral_file_directory, '{}.obj'.format(title)), "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
                    
                    #zip_ref.extract(extractFileName, 'D:\Members\Cathy')
                    
                    print("Coral file path: {}\n".format(target))

                # Now that the file is extracted, delete the zip file
                removeFile(path_to_zip_file)

def removeFile(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist. File path: " + path)
 
#   Sometimes there are multiple simplified versions of the coral.
#   Determine the most simplified .obj file name
def determineExtractFileName(zip_ref):
    listOfFiles = zip_ref.namelist()
    objFileNames = [fileName for fileName in listOfFiles if fileName.endswith('obj')]
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
        print("The file already exists: {}".format(destination))

    # Check if extracted coral file already exists in coral directory
    elif os.path.exists('{}\\{}'.format(coral_file_directory, title)) or os.path.exists('{}\\{}.obj'.format(coral_file_directory, title)):
        print('The specific coral file already exists in directory: {}\\{}'.format(coral_file_directory, title))
        file_already_exists = True

    else:
        print("Trying to download {}".format(title))
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(destination)
        print('file {} downloaded!'.format(title))
    
    # Return destination of the file
    return destination, title, file_already_exists

#   Make all files without an extension an .obj file
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

#   Move all files of a certain extension from current directory to new directory
#   Usage: move all files run by processOBJ to a new folder
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
        fileFD = currentCoral.fileFD
        [boundingLength, boundingWidth, boundingHeight]=currentCoral.findBoundBox()
        return str(coralName) + " | " + str(sa) + " | " + str(volume)   + " | " + str(numVertices)   + str(numEdges)   +  " | " + str(numFaces)   + " | " + str(onlineFD) + " | " + str(fileFD) + " | " + str(analysisTime) +"\n"

if __name__ == "__main__":
    #main()
    #currentCoral = analyzeObject('D:\Members\Cathy\coralFiles\Acropora grandus - 1056.obj')
    #print(obtainCurrentCoralData(currentCoral))
    #writeAndUploadData(currentCoral, output_filepath, drive_output_file_id)
    iterateAndAnalyzeZip(coral_file_directory+'.zip')