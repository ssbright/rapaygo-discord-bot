

def command_validator(string):
    if (len(str.split(string)) != 4):
       return False
    cList = str.split(string)
    atBot = cList[0]
    if atBot != "<@984815715544617011>" and atBot != "<@1016751469900337162>" and atBot != "<@1006706349465423933>":
        print("false validator")
        return False
    return True 

def inquiry_command(string):
    if (len(str.split(string)) != 2):
       return False
    cList = str.split(string)
    atBot = cList[0]
    inquiry = cList[1]
    if atBot != "<@984815715544617011>" and atBot != "<@1016751469900337162>" and atBot != "<@1006706349465423933>":
        return False
    if inquiry == "commands?":
        return 1
    if inquiry == "help":
        return 1
    if inquiry == "status":
        return 2
    return False

def anyother_message(string):
    if len(str.split(string)) >= 1:
        cList = str.split(string)
        atBot = cList[0]
        print(f"this is the string {string}")
        if atBot == "<@984815715544617011>" or atBot == "<@1016751469900337162>" or atBot == "<@1006706349465423933>" :
            if command_validator(string) == False and inquiry_command(string) == False and string != "<@984815715544617011> hello" and string != "<@984815715544617011> Hello" and string != "<@1006706349465423933> hello" and string != "<@1006706349465423933> Hello" and string != "<@1016751469900337162> hello" and string != "<@1016751469900337162> Hello":
                return True
            else:
                return False

        else:
            return False


