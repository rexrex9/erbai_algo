
from flask import request
from utils.log_utils import logger
def getArgs(t):
    a = None
    d = request.json
    if d:
        a = d.get(t)
    if a == None:
        a = request.args.get(t)
    if a == None :
        a = request.form.get(t)
    if a==None:
        a = request.headers.get(t)
    return a

def getArgsMore(t):
    t = getArgs(t)
    logger.info(t)
    return t