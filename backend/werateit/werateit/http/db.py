from quantumcore.storages.mongoobjectstore import MongoObjectStore
import pymongo
import uuid
import copy
import array

class Domain(object):
    """data model for mongodb"""

    domain = u"" # the domain to rate
    ratings = {} # sub documents containing the ratings consisting of {userid: rating} mappings
    rating = None # the official rating

    _attribs = ['_id', 'domain','ratings','rating']
    _defaults = {
            'ratings' : {},
            'rating' : None,
    }
    def __init__(self, _id=None, _store = None, **kwargs):
        """initialize the database object class. """
        data = copy.copy(self._defaults)

        # update defaults with kwargs
        data.update(kwargs)

        # store dictionary as attributes
        for a,v in data.items():
            setattr(self, a, data[a])

        # now some manual storage of internal attributes
        if _id is None:
            _id = unicode(uuid.uuid4())
        self._id = _id
        self._store = _store

    def _to_dict(self):
        """serialize this object to a dictionary"""
        d={}
        for attrib in self._attribs:
            if attrib=='_id' and self._id is None:
                continue
            d[attrib] = getattr(self, attrib, u'')
        return d
    
    @classmethod
    def from_dict(cls, d, store):
        """create an entry from the data given in d"""
        d = dict([(str(a),v) for a,v in d.items()])
        d['_store']=store
        return cls(**d)

    def set_id(self, id_):
        self._id = id_

    def get_id(self):
        return self._id

    oid = property(get_id, set_id)

    def set_rating(self, userid, rating):
        """store a new rating"""
        # store it
        self.ratings[userid] = rating

        # compute the rating value
        all = array.array("i",self.ratings.values())
        rating = None
        rating_count = 0
        for r in [0,6,12,16,18]:
            c = all.count(r)
            if c>rating_count:
                rating_count = c
                rating = r
            elif c==rating_count: # the same as the last max
                rating = None
            else: # lower, so ignore it
                pass

        self.rating = rating


class Domains(MongoObjectStore):
    """a domain content manager"""

    data_class = Domain

