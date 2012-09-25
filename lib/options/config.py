import ConfigParser
from collections import namedtuple
sections = ['dirs','filename_formats']
def subconf(section):
	Conf = namedtuple(section,(k for k,_ in c.items(section)))
	conf = Conf(**dict(c.items(section)))
	return conf
c = ConfigParser.RawConfigParser(allow_no_value=True)
c.readfp(open('config','r'))
PConf = namedtuple('Configuration',sections)
configuration = PConf(**{sect:subconf(sect) for sect in sections})

