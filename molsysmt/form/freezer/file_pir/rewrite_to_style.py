def rewrite_to_style(filename, style=None):

    if style == 'modeller':
        fff = open(filename,"r")
        content = fff.readlines()
        fff.close()

        fff = open(filename,"w")
        fff.writelines(content[0])
        fff.write("sequence:::::::::")
        fff.writelines(content[1:])
        fff.close()

        pass
    else:
        pass

