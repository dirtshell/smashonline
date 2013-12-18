import web
import uuid
import datetime
import pytz

db = web.database(dbn='sqlite', db='smashbook.db')


def getMatches():
    return db.select('matches', order='id')
    
def getMatch(id):
    try:
        return db.select('matches', where='id=$id', vars=locals())[0]
    except IndexError:
        return None
        
def newMatch(title, net_code, password=None):
    unique_key = str(uuid.uuid4()).upper().replace('-','')  # Generate a unique key
    unique_key = unique_key[0:10]   # Truncate to a 10 char long random string
    ip = web.ctx['ip']   # Get the IP of the request
    
    db.insert('matches', # Send it to the database
        title=title, 
        net_code=net_code, 
        created_on=datetime.datetime.utcnow(), 
        unique_key=unique_key, 
        ip=ip,      
        timezone=timezone,
        password=password,)