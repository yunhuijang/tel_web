from flask import Flask, render_template, request
import os
from importer import xes_import, tel_import
from show import show_model, compare_model
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.algo.discovery.transition_system.parameters import *

app = Flask(__name__)

@app.errorhandler(500)
def wrong_log_type(e):
    return render_template("500.html"), 500

@app.route('/')
def file_upload():
    return render_template('file_upload.html', title = "import")

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save('input_data/' + f.filename)
        return render_template('success.html', title = "success")

@app.route('/show model', methods = ['GET', 'POST'])
def show_import():
    path = "input_data"
    file_list = os.listdir(path)
    file_list.sort()
    return render_template('import.html', title = "show" ,files = file_list)

@app.route('/compare model', methods = ['GET', 'POST'])
def comp_import():
    path = "input_data"
    file_list = os.listdir(path)
    file_list.sort()
    return render_template('import.html', title = "compare", files = file_list)

@app.route('/show', methods = ['POST'])
def show():
    parameters = {}
    option = {}

    if request.form['model'] in ['ts', 'sbr']:
        parameters['afreq_thresh'] = int(request.form['afreq'])
        parameters['sfreq_thresh'] = int(request.form['sfreq'])

    model = request.form['model']
    file_name = request.form['file']
    input_file_path = os.path.join("input_data", file_name)
    file_type = request.form['file_type']
    if file_type == 'xes':
        tel = xes_import(input_file_path)
    else:
        tel = tel_import(input_file_path)

    option['model'] = model
    option['file'] = file_name
    option['file_type'] = file_type

    img_file_path, result, max_thresh,  stat = show_model(model, tel, file_name, parameters)

    return render_template('show.html', img_file_path = '../' + img_file_path, result = result, stat = stat, option=option,
                           parameters= parameters, max_thresh = max_thresh)

@app.route('/compare', methods = ['POST'])
def compare():
    parameters = {}
    parameters_2 = {}
    option = {}
    if request.form['model'] in ['ts', 'sbr']:
        parameters['afreq_thresh'] = int(request.form['afreq'])
        parameters['sfreq_thresh'] = int(request.form['sfreq'])
        parameters_2[PARAM_KEY_DIRECTION] = request.form['PARAM_KEY_DIRECTION']
        parameters_2[PARAM_KEY_VIEW] = request.form['PARAM_KEY_VIEW']
        parameters_2[PARAM_KEY_WINDOW] = int(request.form['PARAM_KEY_WINDOW'])

    model = request.form['model']
    file_name = request.form['file']
    input_file_path = os.path.join("input_data", file_name)
    file_type = request.form['file_type']
    if file_type == 'xes':
        tel = xes_import(input_file_path)
    else:
        tel = tel_import(input_file_path)

    log = xes_import_factory.apply(input_file_path)

    option['model'] = model
    option['file'] = file_name
    option['file_type'] = file_type

    img_file_path, img_file_path_2, result, result_2, max_thresh, stat = compare_model(model, file_name, tel, log, parameters, parameters_2)

    return render_template('compare.html', img_file_path = img_file_path, img_file_path_2 = img_file_path_2,
                           option = option, parameters_2 = parameters_2, parameters = parameters, result = result, result_2 = result_2, max_thresh = max_thresh, stat = stat)

# No cacheing at all for API endpoints.
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

app.run()