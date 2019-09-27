from flask import render_template, jsonify, request, session
import os
import json
from msgbus import parsethemsgbus
from werkzeug.utils import secure_filename
from msgbus.forms import UploadFile, SelectDeselect
from msgbus import app

generate_signature = {}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'log'


@app.route("/", methods=['GET', 'POST'])
def upload_file():
    global generate_signature
    print(generate_signature)
    generate_signature.clear()
    uploadForm = UploadFile()
    if uploadForm.changeFile.data:
        f = uploadForm.file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        app.config['FILENAME'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        app.config['PID_INFO'] = parsethemsgbus.get_for_filename_all_pids(app.config['FILENAME'])
        app.config['ALL_INFO_ABOUT_FILE'], app.config['FIELDS'] = parsethemsgbus.make_everything(app.config['FILENAME'])

    return render_template("home.html", form=uploadForm, file=app.config['FILENAME'])


@app.route('/view_pid/<variable>')
def view_pid(variable):
    global generate_signature
    generate_signature.clear()
    fields = list(app.config['FIELDS'])
    controlForm = SelectDeselect()
    return render_template("view_pid.html", process=app.config['ALL_INFO_ABOUT_FILE'][variable], fields=fields,
                           pid=variable, form=SelectDeselect)


@app.route("/print_pids/", methods=['GET', 'POST'])
def print_pids():
    if app.config['FILENAME'] != "":
        myList = app.config['PID_INFO']
    else:
        myList = ""
    return jsonify({'data': render_template('ceva.html', myList=myList)})


@app.route("/clear_pids", methods=['POST'])
def change_file():
    return "ceva"


@app.route("/get_events", methods=['POST'])
def get_events():
    global generate_signature
    my_event_list = generate_signature
    if request.method == "POST":
        raw_string = str(request.data, encoding='UTF-8')
        raw_string = raw_string.replace("\'", "\"")
        dic = json.loads(raw_string)
        print(dic['event_name'])
        if dic['event_name']  in generate_signature:
            generate_signature[dic['event_name']].append(dic)
        else:
            generate_signature[dic['event_name']] = []
            generate_signature[dic['event_name']].append(dic)
        for item in generate_signature[dic['event_name']]:
            print(f'{item}')
    return ""


@app.route("/delete_event", methods=['POST'])
def delete_event():
    global generate_signature
    raw_event = str(request.data, encoding='UTF-8')
    raw_event = raw_event.replace("\'", "\"")
    raw_event = json.loads(raw_event)
    for event in generate_signature[raw_event['event_name']]:
        if event == raw_event:
            generate_signature[raw_event['event_name']].remove(event)
            break
    print(generate_signature)
    return ""
