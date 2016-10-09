#
# Tool for downloading webpages' source code using mechanize
#

import mechanize
import io

def main():

    url = raw_input("Provide page address:")
    browser = mechanize.Browser()
    page = browser.open('http://' +url)
    source_code = page.read()
    with io.FileIO(url + "_source_code.txt", "w") as file:
        file.write(source_code)
    print "Grabbing %s source code and writing to %s_source_code.txt...\n" % (url, url)
    print "[+] Done"
