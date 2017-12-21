__author__ = 'Administrator'

def Some(obj):
    try:
        obj
        return obj
    except:
        return 'None'

abc = {}
abc['abc'] = 1
print( Some(abc['ews']) )


