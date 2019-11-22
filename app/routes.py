from flask import render_template, request
from app import app
from .pidball import PIDBall

@app.route('/')
@app.route('/presentation')
def presentation():
    return render_template('presentation.html')

@app.route('/pid', methods=['GET'])
def show_pid():
    params = {
            's_0': float(request.args.get('s_0', '10')),
            'sp': float(request.args.get('sp', '5')),
            'v_0': float(request.args.get('v_0', '0')),
            'dt': float(request.args.get('dt', '0.01')),
            't_f': float(request.args.get('t_f', '1')),
            'k_p': float(request.args.get('k_p', '1500')),
            'k_i': float(request.args.get('k_i', '300')),
            'k_d': float(request.args.get('k_d', '50')),
            }

    pid = PIDBall(params)
    data = pid.run()
    return render_template('pid.html', data=data, params=params)
