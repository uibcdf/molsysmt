import os

for filename in os.listdir('./_autosummary'):
    file=open('./_autosummary/'+filename,'r')
    content=file.read()
    file.close()
    name=filename[:-4] # without '.rst'
    length_name=len(name)
    new_name=str.join('.',filename.split('.')[1:-1])
    length_new_name=len(new_name)
    new_content=new_name+'\n'+length_new_name*'='+content[(length_name*2+2):]
    file=open('./_autosummary/'+filename,'w')
    file.write(new_content)
    file.close
