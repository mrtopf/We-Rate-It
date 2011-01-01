import sys
import os
import pkg_resources
import pymongo
import logbook
import datetime
import db

from quantumcore.storages import AttributeMapper

def setup(**kw):
    """initialize the setup"""
    settings = AttributeMapper()
    
    settings['secret_key'] = "czs7s8c6c8976c89c7s6s8976cs87d6" #os.urandom(20)
    settings['log'] = logbook.Logger("werateit")
    settings.update(kw)
    settings.mdb = mdb = pymongo.Connection().werateit
    settings.domain_db = db.Domains(mdb, "domains")
    return settings






