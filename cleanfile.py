import subprocess
import time

#opens Audacity and waits a few seconds so audcacitypipetest is happy.
#be sure to enable Preferences/Modules/mod-script-pipe in Audacity!

subprocess.Popen('C:\Program Files\Audacity\Audacity.exe')
time.sleep(5)


import audacitypipetest as pipe_test
import eyed3  #see: https://github.com/audacity/audacity/issues/1696 for why this is all necessary
import os
import shutil



# PATH is the folder of files to be imported/exported.
PATH = "D:/path/to/mp3/folder"
# Image location for ID3 tag
imagefile = "C:/path/to/ID3/tage/image.png"
audacity_output_folder = "C:/path/to/Audacity/macro-output/folder"



# Audacity processing
def run_commands(INFILE):
    filename = ('"' + str(os.path.join(PATH, INFILE + '.mp3')) + '"')
    pipe_test.do_command(f"Import2: Filename={filename}") 
    pipe_test.do_command('Macro_cleanfile:')


# Platform specific file name and file path.
while not os.path.isdir(PATH):
    PATH = os.path.realpath(input('Path to test folder: '))
    if not os.path.isdir(PATH):
        print('Invalid path. Try again.')


#Get files from folder
file = os.listdir(PATH)
for f in file:
    if f.endswith('mp3'):
        INFILE = f
        while not os.path.isfile(os.path.join(PATH, INFILE)):
            INFILE = input('Name of input mp3 file: ')
            INFILE = os.path.splitext(INFILE)[0] + '.mp3'
            if not os.path.isfile(os.path.join(PATH, INFILE)):
                print(f"{os.path.join(PATH, INFILE)} not found. Try again.")
            else:
                print(f"Input file: {os.path.join(PATH, INFILE)}")
        # Remove file extension.
        INFILE = os.path.splitext(INFILE)[0]
    
        # Get ID3 info
        audiofile = eyed3.load(os.path.join(PATH, INFILE + '.mp3'))
        if (audiofile.tag == None):
            audiofile.initTag()

        # Delete comments because they double up
        # https://github.com/nicfit/eyeD3/issues/111
        for comment in audiofile.tag.comments:

            audiofile.tag.comments.remove(comment.description)
    
        audiofile.tag.save()      

        year = audiofile.tag.recording_date
        comment = u"Comment goes"
        albumartist = audiofile.tag.album_artist
        image = open(imagefile,"rb").read()

        # Apply the macro()
        run_commands(INFILE)  

        # Save ID3 tag info to the cleaned file 
        audiofile = eyed3.load(os.path.join(audacity_output_folder, INFILE + '.mp3'))
   
        audiofile.tag.recording_date = year
        audiofile.tag.comments.set(comment) 
        audiofile.tag.album_artist = albumartist
        audiofile.tag.images.set(3,image,"image/png",u"Alt-Image-Title") #https://tuxpool.blogspot.com/2013/02/how-to-store-images-in-mp3-files-using.html

        audiofile.tag.save()


# Close audacity the hard way
subprocess.call(["taskkill","/F","/IM","Audacity.exe"])
os.kill



# Rename as filename_1 and move to original folder (PATH)
while not os.path.isdir(audacity_output_folder):
    audacity_output_folder = os.path.realpath(input('Path to Audacity macro output folder: '))
    if not os.path.isdir(audacity_output_folder):
        print('Invalid path. Try again.')

folder = os.listdir(audacity_output_folder)
for f in folder:
    INFILE = f
    while not os.path.isfile(os.path.join(audacity_output_folder, INFILE)):
        INFILE = input('Name of mp3 file: ')
        INFILE = os.path.splitext(INFILE)[0] + '.mp3'
        if not os.path.isfile(os.path.join(audacity_output_folder, INFILE)):
            print(f"{os.path.join(audacity_output_folder, INFILE)} not found. Try again.")
        else:
            print(f"Input file: {os.path.join(audacity_output_folder, INFILE)}")
    # Remove file extension.
    INFILE = os.path.splitext(INFILE)[0]
    
    shutil.move(os.path.join(audacity_output_folder, INFILE + ".mp3"), os.path.join(PATH, INFILE + "_1.mp3"))
