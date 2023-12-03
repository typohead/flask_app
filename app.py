
from flask import Flask, render_template,request,send_file
import subprocess
import os
app = Flask(__name__)

#setting python file directory as flask's working directory
working_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(working_directory)


#the root route of the website
@app.route('/')
def firstfn():
    return render_template('index.html')

#
#   User enters the message via a form , the action of the form is set to /submit and flasks routes the data here to /submit route
#
@app.route('/submit', methods=['POST'])
def messageSubmitted():
    message= request.form['message']  # request.form returns a dictonary where indexes are the name of the input tags

    if(message == ""):
        return "<h1>Empty data entered</h1>"


    # We have a template cpp file which ouputs "Hello Message " on the screen 
    # We generate a new file program.cpp in which the string "Message" is replaced by the text given by the user

    root_directory= os.path.dirname(os.path.abspath(__file__))
    target_directory_template= os.path.join(root_directory,"template.cpp")
    target_directory_generated_file= os.path.join(root_directory,"program.cpp")

    #open template.cpp , replace "message" string in the template with the text given by user and write this new data into a new file named program.cpp
    
    file = open(target_directory_template,'r')
    file_data= file.read()
    new_file_data= file_data.replace('"message"',f'"{message}"') # replaces the stringt "message" with user message
    
    #creating the new program.cpp
    file = open(target_directory_generated_file,'w')
    file.write(new_file_data)
    file.close()
    
    #output = "Compilation successful"

    #now compiling the program file and generate a output.exe
    #cpp file compiled by using cross platform mingw64 compiler , which compiles cpp file to .exe ( in a linux environment)
    
    subprocess.run(["/usr/bin/x86_64-w64-mingw32-g++", "-o","/home/ritik/flask_app/output.exe","/home/ritik/flask_app/program.cpp"])

    #suprocess modules is used to fire terminal commands , every argument is space separated and joined to make the command
    # here 1st argument : name of compiler 
    #3: output file 
    #4: input file 

    #resultant_exe=os.path.join(root_directory,"output.exe")

    #Return the generated .exe file to the user 
    return send_file( os.path.join(root_directory,"output.exe") , as_attachment=True)
    
    #return output

if(__name__=="__main__"):
    app.run(debug=False)
