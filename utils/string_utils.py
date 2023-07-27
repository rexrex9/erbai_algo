import json
import re

def isNone(d):
    return d==None or d=='' or d==[] or d=={} or d==set() or d==()

def get_int(s,defalt):
    return int(s) if s is not None and s!='' else defalt

def get_braces_as_json(s):
    s = s.replace('\n','')
    result = re.findall(r"\{(.+?)\}",s.strip())
    print(result[0].strip())
    if len(result)>0:
        return json.loads("{"+result[0].strip()+"}")
    else:
        return {}

def sum_dict(d):
    return sum([float(i) for i in d.values()])
def is_punctuation(text):
    punctuation_pattern = r'[^\w\s]'
    punctuation_matches = re.findall(punctuation_pattern, text)
    return not isNone(punctuation_matches)

def get_content_between_two_keys(key1,key2,text):
    match = re.search(r"(?i)(?<={}).*?(?={})".format(key1,key2), text)
    if match:
        demo_text = match.group(0)
        return demo_text
    else:
        return ""

def get_content_after_keys(key1,text):
    match = re.search(r"(?i)(?<={}).*".format(key1), text)
    if match:
        demo_text = match.group(0)
        return demo_text
    else:
        return -1



