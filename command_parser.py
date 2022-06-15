

def command_validator(string):
    if (len(str.split(string)) != 4):
       return False
    cList = str.split(string)
    atBot = cList[0]
    if atBot != "<@984815715544617011>" :
        return False 
    return True 




