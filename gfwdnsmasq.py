# Modified from http://autoddvpn.googlecode.com/svn/trunk/grace.d/gfwListgen.py
#!/usr/bin/env python

from os.path import expanduser
import urllib
import base64
import string

gfwlist = 'http://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt'
# some sites can be visited via https or is already in known list
oklist = ['flickr.com','amazon.com','twimg.com']
print "fetching gfwList ..."
d = urllib.urlopen(gfwlist).read()
print("gfwList fetched")
data = base64.b64decode(d)
lines = string.split(data, "\n")

gfwlistfile = open(expanduser('./')+'gfwlist.txt', 'wa')
for l in lines:
	gfwlistfile.write(l+'\n')
gfwlistfile.close()

newlist = []

for l in lines:
	if len(l) == 0:
	        continue
	if l[0] == "!":
	        continue
	if l[0] == "@":
	        continue
	if l[0] == "[":
	        continue
	l = string.replace(l, "||","").lstrip(".")
	l = string.replace(l, "|https://","")
	l = string.replace(l, "|http://","")
	# strip everything from "/" to the end
	if l.find("/") != -1:
	        l = l[0:l.find("/")]
	if l.find("%2F") != -1:
	        continue
	if l.find("*") != -1:
	        continue
	if l.find(".") == -1:
	        continue
	if l in oklist:
	        continue
	newlist.append(l)

newlist = list(set(newlist))
newlist.sort()

# generate dnsmasq configuration
gfwdn = open(expanduser('./')+'gfwdomains.conf', 'wa')

for l in newlist:
        gfwdn.write('server=/'+l+'/8.8.8.8\n')
#        gfwdn.write('ipset=/'+l+'/vpn\n')

gfwdn.close()
