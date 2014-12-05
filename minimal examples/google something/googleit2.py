# code from http://code.google.com/p/pygoogle/

from pygoogle import pygoogle
g = pygoogle('the haunted palace wikipedia')
g.pages = 1
print '*Found %s results*'%(g.get_result_count())
url_links = g.get_urls()
print "top result:", url_links[0]
