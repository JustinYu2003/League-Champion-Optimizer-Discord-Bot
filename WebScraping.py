from urllib.request import urlopen

#SECTION 1
#URL
url = "http://olympus.realpython.org/profiles/aphrodite"

#Get HTTPResponseObject
page = urlopen(url)

#Read the page to get a sequence of bytes, then decode it into string using UTF-8
html_bytes = page.read()
html = html_bytes.decode("utf-8")

#Print the HTML result
print(html)

#Find the title, using .find(), find the start and ending tags of title, and slice the string between it
title_index = html.find("<title>")
start_index = title_index + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]
print(title)

#----------------------------------------------------------
print("\n---------------------------------")

#SECTION 2, same as section 1 but more difficult url
#Doesn't work because <title> isn't there, instead has <title >
url = "http://olympus.realpython.org/profiles/poseidon"
page = urlopen(url)
html = page.read().decode("utf-8")
start_index = html.find("<title>") + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]
print(title)

#----------------------------------------------------------
print("\n---------------------------------")

#Section 3, use REGEX to solve the issue
import re
url = "http://olympus.realpython.org/profiles/dionysus"
page = urlopen(url)
html = page.read().decode("utf-8")

pattern = "<title.*?>.*?</title.*?>"
match_results = re.search(pattern, html, re.IGNORECASE)
title = match_results.group()
title = re.sub("<.*?>", "", title) # Remove HTML tags

print(title)

#----------------------------------------------------------
print("\n---------------------------------")

#Section 4, try it on 
url = "http://olympus.realpython.org/profiles/dionysus"
page = urlopen(url)
html = page.read().decode("utf-8")

for string in ["Name: ", "Favorite Color:"]:
    #Find the starting index after the :5
    string_start_idx = html.find(string)
    text_start_idx = string_start_idx + len(string)

    #Find the next index of the next html bracket and use that to find the ending index of the text
    next_html_tag_offset = html[text_start_idx:].find("<")
    text_end_idx = text_start_idx + next_html_tag_offset

    #Slice it and print it
    raw_text = html[text_start_idx : text_end_idx]
    clean_text = raw_text.strip(" \r\n\t")
    print(clean_text)

#----------------------------------------------------------
print("\n---------------------------------")

#Section 5, Beautiful Soup
from bs4 import BeautifulSoup

url = "http://olympus.realpython.org/profiles/dionysus"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

#Automatically gets rid of html tags
print(soup.get_text())

#Get all the img tags, <img src="/static/dionysus.jpg"/>
#name property returns HTML tag type
#Properties such as src can be gotten as well
image1, image2 = soup.find_all("img")
print(image1.name)
print(image1["src"])

#Some html tags can be accessed by itself, also with its string in it
print(soup.title)
print(soup.title.string)