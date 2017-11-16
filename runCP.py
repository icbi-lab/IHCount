import os
import sys
import csv
import errno
import curses
import fnmatch
import pandas as pd


# Variables
fileName = os.path.basename(__file__)


flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
rootDir = os.getcwd()

while True:
    my_input = raw_input(
    "**************************************************************************************************************\n"+
    "WHAT WOULD YOU LIKE TO DO? (Please enter:\n"+
    "q to QUIT,\n"+
    "h for HELP,\n"+
    "d for DEPENDENCIES\n"+
    "or\n"+
    "STEP 1 [preprocess] to convert and tile image files"+"\n\n"+
    "INTERMEDIATE STEP: TRAIN IN ILASTIK and GENERATE PROBABILITY MAPS"+"\n\n"+
    "STEP 2 [files2list] to create an image filelist for CellProfiler"+"\n\n"+
    "STEP 3 [count] to run CellProfiler"+"\n\n"+
    "STEP 4 [summarise] to format CellProfiler result table \n\n"+
    ">>>  ")

    if my_input == 'h':
         print ("    New Folder/\n"+
                "           -- runCP.py\n"+
                "           -- bftools/\n"+
                "           -- IHCount.cppipe\n"+
                "           -- image_1.[scn,svs...]\n"+
                "           -- image_1.tiles/\n"+
                "               -- fileList.txt\n"+
                "               -- tile_1.tif\n"+
                "               -- tile_2.tif\n"+
                "           -- image_2.[scn,svs...]\n"+
                "           -- image_2.tiles/\n"+
                "****************************************************************\n"+
                "****************************************************************\n\n"+
                "STEP 1 [preprocess] to convert and tile image files"+"\n\n"+
                "INTERMEDIATE STEP: TRAIN IN ILASTIK and GENERATE PROBABILITY MAPS"+"\n\n"+
                "STEP 2 [files2list] to create an image filelist for CellProfiler"+"\n\n"+
                "STEP 3 [count] to run CellProfiler"+"\n\n"+
                "STEP 4 [summarise] to format CellProfiler result table \n\n")

    
    elif my_input == "preprocess":
        for dirName, subdirList, fileList in os.walk(rootDir):
            for f in fileList:
                print os.getcwd()
                if f.endswith(".scn") or f.endswith(".svs"):
                    os.system("mkdir " + f[:-4] + ".tiles")
                    os.system("./bftools/showinf -nopix " + f)
                    # # choose series interactively or insert number for variable series in CONVERTING COMMAND! Comment raw_input for series!!
                    series = raw_input("Which series?  ")
                    print "CONVERTING..."
                    os.system("./bftools/bfconvert -tilex 512 -tiley 512 -series " + series + " -compression LZW " + f + " " + f[:-4]+".tif")
                    print "TILING..."
                    os.system("./bftools/bfconvert -debug -tilex 2000 -tiley 2000 "+ f[:-4] + ".tif " + f[:-4] + ".tiles/" + f[:-4] + ".X%x.Y%y.tile.tissue.tif")
   
        for root, dirs, files in os.walk(rootDir, topdown=True):
            for folder in dirs:
                if folder.endswith(".tiles"):
                    p = os.path.join(root, folder)
                    os.chdir(p)
                    i=0
                    for filename in os.listdir(os.getcwd()):
                        if fnmatch.fnmatch(filename, '*.tile.tissue.tif'):
                            i+=1
                            print 'FILE CONVERTING TO PNG'
                            os.system('../bftools/bfconvert -merge ' + filename +' '+ filename[:-4]+".png")
                            #os.system('rm '+ filename)
                            print 'FILE CONVERTED!'
                    print i
    
    

    elif my_input == "files2list":
        print os.getcwd()
        for dirName, subdirList, fileList in os.walk(rootDir):
            print subdirList
            for d in subdirList:
                if d.endswith(".tiles"):
                    os.chdir(d)
                    print "CREATE FILELIST"
                    for dirName, subdirList, fileList in os.walk(os.getcwd()):
                        try:
                            os.remove(os.getcwd()+"/fileList.txt")
                        except OSError:
                            pass
                        for f in fileList:
                            print f
                            with open(os.getcwd()+"/fileList.txt", "a+") as file_obj:
                                if f.endswith("tissue.tif"):
                                    file_obj.write(os.path.abspath(f)+'\n')
                                elif f.endswith("positives.tif"):
                                    file_obj.write(os.path.abspath(f)+'\n')
                                elif f.endswith("nuclei.tif"):
                                    file_obj.write(os.path.abspath(f)+'\n')

                    os.chdir("..")


    elif my_input == 'count':
        cppipe =raw_input("Which cppipe file schould be used? Type full file name:  ")
        print os.getcwd()
        for dirName, subdirList, fileList in os.walk(os.getcwd()):
            for f in fileList:
                if f.endswith('.cppipe'):
                    pipeDir = dirName
            if dirName.endswith('.tiles'):
                try:
                    os.system('cellprofiler -c -r -o '+os.path.join(dirName,'results')+' -p '+ os.path.join(pipeDir,cppipe) +' --file-list '+os.path.join(dirName,'fileList.txt'))
                except OSError:
                    pass


    elif my_input == 'summarise':
        if os.path.exists('results_count.csv'):
            print 'results_count.csv already exists!'
        else:
            with open('results_count.csv', 'wb') as outcsv:
                writer = csv.DictWriter(outcsv, fieldnames = [
                    'PathName_nuclei','Count_Potivies',
                    'Count_Nuclei',
                    'AreaOccupied_AreaOccupied_ThreshArea',
                    'AreaOccupied_Perimeter_ThreshArea',
                    'AreaOccupied_TotalArea_ThreshArea'
                    ])
                writer.writeheader()
                print os.getcwd()


        for dirName, subdirList, fileList in os.walk(os.getcwd()):
            if dirName.endswith("result"):
                os.chdir(dirName)
                print os.getcwd()
                print "summarise result table"
                try:
                    data = pd.read_csv('result_Image.csv')
                    data.groupby(
                            ['PathName_nuclei']
                        )[
                            'Count_Potivies',
                            'Count_Nuclei',
                            'AreaOccupied_AreaOccupied_ThreshArea',
                            'AreaOccupied_Perimeter_ThreshArea',
                            'AreaOccupied_TotalArea_ThreshArea'
                        ].sum().to_csv('../../results_count.csv', mode='a', header=False)

                except OSError:
                    pass


    elif my_input not in ("preprocess","files2list","count","summarise","h","q"):
        print "Please enter preprocess, files2list, count, summarise, h or q"
    elif my_input == "q":
        break