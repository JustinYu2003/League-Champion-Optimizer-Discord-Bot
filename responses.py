import random
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import django
from django.template import Template, Context
from django.conf import settings
import imgkit
import discord

#Use django to turn the data into an html file
# https://stackoverflow.com/questions/6748559/generating-html-documents-in-python
settings.configure(TEMPLATES=[{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['.'], # if you want the templates from a file
    'APP_DIRS': False, # we have no apps
},])
django.setup()

def handle_response(message):
    p_message = message.lower()

    if p_message == 'hello':
        return "Hey there!"
    
    if p_message == 'roll':
        return str(random.randint(1, 6))
    
    if p_message == '!help':
        return "`This is a help message that you can modify`"
    
    # return "I don't know what you said"




    #Filter out the name from the argument
    championName = re.sub(r'[^\w\s]', '', message)
    print(championName)
    #Special case
    if "renata" in championName:
        championName = "renata"

    url = "https://www.op.gg/champions/" + championName + "/build"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    #Get the champion icon
    championIcon = soup.find_all("img", {"class": "champion-img"})

    #Get Main and aside box
    main = soup.find_all("main")
    aside = soup.find_all("aside")

    #Split those boxes into the respective divs
    mainSoup = BeautifulSoup(str(main[0]), "html.parser") 
    threeBoxes = mainSoup.find_all(lambda x: x.name == 'div' and x.find_parent("div") is None)
    runesDiv = threeBoxes[0]
    skillPrioDiv = threeBoxes[1]
    buildDiv = threeBoxes[2]

    asideSoup = BeautifulSoup(str(aside[0]), "html.parser") 
    sideBoxes = asideSoup.find_all(lambda x: x.name == 'div' and x.find_parent("div") is None)
    summsDiv = sideBoxes[0]

    #Runes
    #First image = Rune Branch
    #Next 12 = Main Rune tree, get the 4 non grayscaled
    #Next Image = Second Rune Branchranch
    #Next 9 Secondary Branch, 2 runes
    #Next 9 = Additional Stats
    runeSoup = BeautifulSoup(str(runesDiv), "html.parser")
    rows = runeSoup.find_all("div", {"class": "row"})

    mainBranch = []
    for i in range(0, 5):
        rowSoup = BeautifulSoup(str(rows[i]), "html.parser")
        images = rowSoup.find_all("img")
        for i in range(len(images)):
            if "grayscale" not in images[i]["src"]:
                mainBranch.append(images[i])

    asideBranch = []
    for i in range(5, 9):
        rowSoup = BeautifulSoup(str(rows[i]), "html.parser")
        images = rowSoup.find_all("img")
        for i in range(len(images)):
            if "grayscale" not in images[i]["src"]:
                asideBranch.append(images[i])

    additionalBranch = []
    for i in range(9, 12):
        rowSoup = BeautifulSoup(str(rows[i]), "html.parser")
        images = rowSoup.find_all("img")
        for i in range(len(images)):
            if "grayscale" not in images[i]["src"]:
                additionalBranch.append(images[i])

    #Skills
    skillSoup = BeautifulSoup(str(skillPrioDiv), "html.parser")
    images = skillSoup.find_all("img")

    skillPrio = []
    for i in range(len(images)):
        if "icon-arrow" not in images[i]["src"]:
            skillPrio.append(images[i])

    #Starting Items, Boots, Build, found using table tag
    buildSoup = BeautifulSoup(str(buildDiv), "html.parser")
    tables = buildSoup.find_all("table")

    startTable = tables[0]
    bootTable = tables[1]
    buildTable = tables[2]

    #Get the parent of the starting item rows, then save each row's images by row
    startSoup = BeautifulSoup(str(startTable), "html.parser")
    startRows = startSoup.find_all("div", {"class": "css-nk1dsu e1rgp2h81"})

    startingItemRows = []
    for i in range(len(startRows)):
        rowI = BeautifulSoup(str(startRows[i]), "html.parser")
        startingItemRows.append(rowI.find_all("img"))

    #Boots will always be alone 
    bootSoup = BeautifulSoup(str(bootTable), "html.parser")
    bootImages = bootTable.find_all("img")

    #Get the parent of the build rows, then save each row's build by row
    buildSoup = BeautifulSoup(str(buildTable), "html.parser")
    buildRows = buildSoup.find_all("div", {"class": "css-37vh9h e1rgp2h81"})

    buildItemRows = []
    for i in range(len(buildRows)):
        rowI = BeautifulSoup(str(buildRows[i]), "html.parser")
        buildItemRows.append(rowI.find_all("img"))

    #Summs, split into two pairs of two
    summSoup = BeautifulSoup(str(summsDiv), "html.parser")
    images = summSoup.find_all("img")

    summs = []
    for i in range(len(images)):
        summs.append(images[i])

    #Turn the html tags into strings
    #Turn the html tags into strings
    mainRuneString = ""
    for i in range(len(mainBranch)):
        mainRuneString += str(mainBranch[i]) + "\n"

    sideRuneString = ""
    for i in range(len(asideBranch)):
        sideRuneString += str(asideBranch[i]) + "\n"

    additionalRuneString = ""
    for i in range(len(additionalBranch)):
        additionalRuneString += str(additionalBranch[i]) + "\n"

    start1String = ""
    for i in range(len(startingItemRows[0])):
        start1String += str(startingItemRows[0][i]) + "\n"

    start2String = ""
    for i in range(len(startingItemRows[1])):
        start2String += str(startingItemRows[1][i]) + "\n"

    buildStrings = ["", "", "", "", ""]
    for i in range(5):
        for j in range(len(buildItemRows[i])):
            buildStrings[i] += str(buildItemRows[i][j]) + "\n"

    # #Use django to turn the data into an html file
    # # https://stackoverflow.com/questions/6748559/generating-html-documents-in-python
    # settings.configure(TEMPLATES=[{
    #     'BACKEND': 'django.template.backends.django.DjangoTemplates',
    #     'DIRS': ['.'], # if you want the templates from a file
    #     'APP_DIRS': False, # we have no apps
    # },])
    # django.setup()

    with open("template.html", 'r') as file:
        template = file.read()

    t = Template(template)
    c = Context({"championIcon": str(championIcon[0]),
                "mainBranch": mainRuneString,
                "asideBranch": sideRuneString,
                "additionalBranch": additionalRuneString,
                "startingItems1": start1String,
                "startingItems2": start2String,
                "boots1": str(bootImages[0]),
                "boots2": str(bootImages[1]),
                "build1": buildStrings[0],
                "build2": buildStrings[1],
                "build3": buildStrings[2],
                "build4": buildStrings[3],
                "build5": buildStrings[4],})

    # return t.render(c)
    with open("result.html", 'w') as file:
        file.write(t.render(c))
    imgkit.from_file("result.html", "result.jpg")

    with open('result.jpg', 'rb') as f:
        picture = discord.File(f)
        
    return picture