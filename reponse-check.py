import requests

# set results file
SAVEFILE = "results.txt"
# set page list file name
FILENAME = "pages.txt"
# set domain string for replacement
REPLACE = "http://virginiabeachwebdevelopment.com/"
# set new domain string
NEWURL = "http://virginiabeachwebdevelopment.com/"

<<<<<<< HEAD
class fileWalk:

    def __init__(self):

        # set initial values
        self.replace = raw_input("Domain to be replaced (default: %s) : " % (REPLACE))
        self.newurl = raw_input("New domain (default: %s) : " % (NEWURL))
        self.savefile = raw_input("Results file (default: %s) : " % (SAVEFILE))
        self.filename = raw_input("Links file (default: %s) : " % (FILENAME))

        # set defaults if no user input is provided
        if self.replace == "":
            self.replace = REPLACE

        if self.newurl == "":
            self.newurl = NEWURL

        if self.savefile == "":
            self.savefile = SAVEFILE

        if self.filename == "":
            self.filename = FILENAME

    #clear output file
    def clear_file(self):
        f = open(self.savefile, 'r+')
        f.truncate()

    def walk_file(self):

        self.clear_file()

        # init counters
        REDCNT = 0
        NTFNDCNT = 0
        OKCNT = 0

        # open results file for writing
        fw = open(self.savefile,'w')
        # open link list
        f=open(self.filename,'r')
        # walk through link file
        for line in f.readlines():

            newlink = line.strip().replace(self.replace, self.newurl)
            # get header response
            conn = requests.get(newlink)

            response = conn.status_code
            # record redirected pages
            if response == 301 or response == 302:
                newpage = conn.url
                REDCNT += 1
            else:
                newpage=''

            # record missing pages
            if response == 404:
                NTFNDCNT += 1
            # record found pages
            if response == 200:
                OKCNT += 1
            
            # write to output file
            results = str(response) + "\t" + newlink + "\t" + newpage + "\n"
            fw.write(results)

        # close results file
        fw.close()
        # close link list file
        f.close()

        print "Redirects:" + str(REDCNT)
        print "200 OK:" + str(OKCNT)
        print "404 not found:" + str(NTFNDCNT)
        print "DONE!"

# init file walk class and walk file
new_file = fileWalk()
new_file.walk_file()
=======
#clear output file
f = open(SAVEFILE, 'r+')
f.truncate()
f.close()

# init counters
REDCNT = 0
NTFNDCNT = 0
OKCNT = 0

# open results file for writing
fw = open(SAVEFILE,'w')
# open link list
f=open(FILENAME,'r')
# walk through link file
for line in f.readlines():

    newlink = line.strip().replace(REPLACE, NEWURL)
    # get header response
    conn = requests.get(newlink)
    
    # gather response code
    response = conn.status_code
    
    # record redirected pages
    if response == 301 or response == 302:
        newpage = conn.url
        REDCNT += 1
    else:
        newpage=''

    # record missing pages
    if response == 404:
        NTFNDCNT += 1
    # record found pages
    if response == 200:
        OKCNT += 1
    
    # write to output file
    results = str(response) + "\t" + newlink + "\t" + newpage + "\n"
    fw.write(results)

# close results file
fw.close()
# close link list file
f.close()

print "Redirects:" + str(REDCNT)
print "200 OK:" + str(OKCNT)
print "404 not found:" + str(NTFNDCNT)
print "DONE!"
>>>>>>> FETCH_HEAD
