from flask import Flask, request
import json
import scrape as s

global json_dict 

'''def read_file(): 
    global json_dict 
    json_dict = {} 
    with open("./result.json", 'r') as f:
        for line in f.readlines():
            _dict= json.loads(line)
            json_dict[_dict['Name']] = _dict['Entity']'''
        
        
        #print(json_dict)'''

app = Flask(__name__)

@app.route('/')
def index():
    code='''<form style="font-size:10px;" method="POST" action = "/result">
        Input url  <input style="font-size:10px;" type="text" name="url"><br><br>
        Input element   <input style="font-size:10px;" type='text' name ="element"><br><br>
        Input attr:class_  <input style="font-size:10px;" type='text' name ='class_'><br><br>
        Input attr:id_  <input style="font-size:10px;" type='text' name='id_'> <br><br>
        Input path_to_file  <input style="font-size:10px;" type ='text' name ='path'><br><br>
        <input type ="Submit"><br><br>
        
        </form >
        <form style="font-size:10px;" method="POST" action = "/standard_search">
        For standard website data extraction  <a href="/standard_search">Click here</a>
        </form>
        '''
    return code
@app.route('/result',methods=['POST'])
def result():
    url=request.form["url"]
    element=request.form["element"]
    class_=request.form["class_"]
    id_=request.form["id_"]
    path=request.form["path"]
    #json_file = {"Oz": "Person", "Jake": "Person"}
    #print(req_data)
    d={'url':url,'element':element,'class_':class_,'id_':id_,'path':path}
    s.extracted_csv(d)
    return '''<h1 style="font-size:10px;">
            The csv is extracted in folder "{}".
            </h1>
            <a href="/">Home</a>
            '''.format(path)

@app.route('/standard_search',methods=['GET','POST'])
def index1():
    code='''<form style="font-size:10px;" method="POST" action = "/standard_result">
        Input url  <input style="font-size:10px;" type="text" name="url"><br><br>
        Input path_to_file  <input style="font-size:10px;" type ='text' name ='path'><br><br>
        <input type ="Submit"><br><br>
        <a href="/">Home</a>
        '''
    return code
@app.route('/standard_result',methods=['POST'])
def standard_result():
    url=request.form["url"]
    path=request.form["path"]
    
    #d={'url':url,'element':element,'class_':class_,'id_':id_,'path':path}
    s.standard_extract(url,path)
    return '''<h1 style="font-size:10px;">
            The csv is extracted in folder "{}".
            </h1>
            <a href="/">Home</a>
            '''.format(path)




if __name__ == "__main__":
    #read_file() 
    app.run(debug=True, port=5000)
