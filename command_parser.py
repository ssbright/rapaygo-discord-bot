

def command_validator(string):
    if (len(str.split(string)) != 4):
       return False
    cList = str.split(string)
    atBot = cList[0]
    if atBot != "<@984815715544617011>" :
        return False 
    return True 

def inquiry_command(string):
    if (len(str.split(string)) != 2):
       return False
    cList = str.split(string)
    atBot = cList[0]
    inquiry = cList[1]
    if atBot != "<@984815715544617011>" :
        return False
    if inquiry == "commands?":
        return 1
    if inquiry == "help":
        return 1
    return False

def anyother_message(string):
    if command_validator(string) == False and inquiry_command(string) == False and string!="hello":
        return True
    else:
        return False


