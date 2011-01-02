from werateit.framework import Handler, Application
from werateit.framework.decorators import json
from logbook import Logger
from logbook import FileHandler
import uuid
import db
import datetime

import setup

class Register(Handler):
    """register new users"""

    @json()
    def post(self):
        userid = unicode(uuid.uuid4())
        self.settings.mdb.users.insert({'userid' : userid})
        return {'userid' : userid}

class Domain(Handler):
    """register new users"""

    @json()
    def get(self, domain):
        domains = self.settings.domain_db.find({'domain' : domain})
        if domains == []:
            rating = None
        else:
            rating = domains[0].rating
        return {'rating' : rating}

    def post(self, domain):
        userid = self.request.form['userid']
        rating = int(self.request.form['rating'])
        if rating not in (0,6,12,16,18):
            return self.error("rating wrong")
        
        domains = self.settings.domain_db.find({'domain' : domain})
        if domains==[]:
            dobj = db.Domain(domain = domain)
            _id = self.settings.domain_db.put(dobj)
            dobj = self.settings.domain_db[_id]
        else:
            dobj = domains[0]
        dobj.set_rating(userid, rating)

        self.settings.domain_db.update(dobj)

        # save in the rating log
        self.settings.mdb.ratings.insert({
            'userid' : userid,
            'rating' : rating,
            'domain' : domain,
            'ts' : datetime.datetime.now(),
        })

        # process ratings
        return self.get(domain)

class App(Application):

    logfilename = "/tmp/werateit.log"
    
    def setup_handlers(self, map):
        """setup the mapper"""
        with map.submapper(path_prefix="/1") as m:
            m.connect(None, "/register", handler=Register)
            m.connect(None, "/domains/{domain}", handler=Domain)
        self.logger = Logger('app')

def main():
    port = 9991
    app = App(setup.setup())
    return webserver(app, port)

def backend_factory(global_config, **local_conf):
    settings = setup.setup(**local_conf)
    return App(settings)

def webserver(app, port):
    import wsgiref.simple_server
    wsgiref.simple_server.make_server('', port, app).serve_forever()

if __name__=="__main__":
    main()

