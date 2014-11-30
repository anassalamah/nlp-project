from pygoogle import pygoogle
g = pygoogle('quake 3 arena')
g.pages = 5
print '*Found %s results*'%(g.get_result_count())
g.get_urls()
