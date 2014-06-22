import requests

# set results file
SAVEFILE = "results.txt"
# set page list file name
FILENAME = "pages.txt"
# set domain string for replacement
REPLACE = "http://virginiabeachwebdevelopment.com/"
# set new domain string
NEWURL = "http://virginiabeachwebdevelopment.com/"

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
