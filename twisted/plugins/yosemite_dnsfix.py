from twisted.application.service import IServiceMaker
from twisted.names import tap
from twisted.plugin import IPlugin
from zope.interface import implements

def monkeypatch():
    from twisted.names import client
    oldLookup = client.Resolver._lookup
    def newLookup(self, name, cls, type, timeout):
        name += search_domain
        return oldLookup(self, name, cls, type, timeout)
    client.Resolver._lookup = newLookup

monkeypatch()

class ServiceMaker(object):
    implements(IPlugin, IServiceMaker)
    name = 'yosemite_dnsfix'
    tapname = 'yosemite_dnsfix'
    description = 'Fix crippled DNS search domains on OS X Yosemite'
    options = tap.Options
    options.optParameters.append(['search-domain', 's', None, 'Search domain'])
    def makeService(self, config):
        assert config['search-domain']
        global search_domain
        search_domain = config['search-domain']
        return tap.makeService(config)

serviceMaker = ServiceMaker()
