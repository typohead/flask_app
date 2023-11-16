from flask import Flask, render_template,request,jsonify
import subprocess
import os
app = Flask(__name__)

#it may happen that flask directory is not out python file directory , so setting our python file directory as flask's working directory
working_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(working_directory)
@app.route('/')
def firstfn():
    return render_template('index.html')

# flask fetches the user provided message an i route it here , then I save it as a txt file that can be opened by the cpp file that i have already written
@app.route('/submit', methods=['POST'])
def messageSubmitted():
    message= request.form['message']  #the request.form returns a dictonary where indexes are the name of the input tags

    if(message == ""):
        return "<h1>Empty data entered</h1>"

    root_directory= os.path.dirname(os.path.abspath(__file__))
    target_directory_template= os.path.join(root_directory,"template.cpp")
    target_directory_generated_file= os.path.join(root_directory,"program.cpp")
    #open template.cpp , replace the user message with the message in the file and write this new data into a new file named program.cpp
    file = open(target_directory_template,'r')
    file_data= file.read()
    new_file_data= file_data.replace('"message"',f'"{message}"')
    file.close()

    #creating the new program.cpp
    file = open(target_directory_generated_file,'w')
    file.write(new_file_data)
    file.close()
    output = "Compilation successful"

    #now compiling the program file and generate a output.exe
    subprocess.run(["x86_64-w64-mingw32-g++", "-o","output.exe","program.cpp"]) 
    return output

if(__name__=="__main__"):
    app.run(debug=False)