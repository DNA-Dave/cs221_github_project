import os
import json
import re
#PATH TO common_stuff DIRECTORY
#I ran this script from my folder via python ./drews_stuff/parseJSON.py. That is, I ran it from just the main project diretory, so that's
#why I called os.getcwd
commonDir = str(os.getcwd()) + "\\"
#I put the CVS file in the common_stuff directory
csvFile = commonDir + 'erey\\feature-extractor.csv'


importantFeatureHeaders = []
########## This part just gets the headers, i.e. important features from the excel file - this is why formatting excel is important
#FORMATTING THE EXCEL HEADERS
# look at the json - if what you want is immediately in "items", just put the exact title into excel
# if what you want is nested, follow the nesting pattern with "." characters. That is, if you are looking for items -> owner -> id, make header owner.id
# if you want a specific part of the string to be removed by algorithm (like weird things at end of URL), put it in parentheses. you can only remove one right now
#TO DO: if necessary, make removing multiple pieces possible
with open(csvFile, "r", encoding="utf-8") as readCSV:
    header = readCSV.readline()
    importantFeatureHeaders = header.split(",")
    importantFeatureHeaders = [w.replace("\n", "") for w in importantFeatureHeaders]
    importantFeatureHeaders[0] = "id"
########## This part does the rest - loops over every JSON and pulls out the imporant features as formatted by excel spreadsheet
#Implements nesting JSON's and removing things from values
tempFileName = commonDir + 'temp.csv' #Temp file to store result
with open(tempFileName, "w+", encoding="utf-8") as writeIn:
    writeIn.write('\t'.join(importantFeatureHeaders) + '\n') #write back in same headers as before

    #### POINTS TO DIRECTORY OF JSON's. For me, it was here. Change it. 
    jsonDir = 'D:\CS221-Data\\repo_names_info\\'#DIRECTORY of JSONS
    ##################### CHANGE LINE ABOVE ################
    advance = 0;
    for f in os.listdir(jsonDir):#loop every JSON
        with open(jsonDir+f, "r", encoding="utf-8") as jsonF:
            data = json.load(jsonF)
            if "items" not in data:#should mean broken
                continue
            itemsList = data["items"]
            cppFound = False#only care about the first fork of language c++
            counter = 0
            while not cppFound and counter < len(itemsList):
                items = itemsList[counter]
                if items["language"]== "C++":
                    cppFound = True 
                else: counter += 1    
            if cppFound:
                for header in importantFeatureHeaders:
                    ####IMPORTANT: cannot have parentheses in feature name - lemme know if it poses issues later
                    toRemove = re.search(r'\((.*)\)', header)
                    if toRemove is not None:
                        toRemove = toRemove.group(0)[1:-1] #get rid of (, )
                        header = header.replace(" (" + toRemove + ")", "")
                    else:
                        toRemove = ""
                    keys = header.split('.')
                    temp = items
                    for key in keys:#naviages to actual value (gets to id in the case of owner.id)
                        if temp[key] == None: # For example if no license present
                            temp = "None"
                            break
                        temp = temp[key]
                    

                    writeIn.write(str(temp).replace(toRemove,""))
                    writeIn.write("\t")
        writeIn.write('\n')
        
        print(str(advance) + "." + f)
        advance+=1;
        
