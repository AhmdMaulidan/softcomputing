import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import json
import genetic_knapsack

app = Flask(__name__)

# --- Configuration ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/uploads')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# --- Database Model ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

# --- Hardcoded Project Data ---
PROJECTS = [
    {
        'id': 'sugeno-calculator',
        'title': 'Kalkulator Fuzzy Sugeno',
        'thumbnail': 'uploads/thumnail-fuzzy.png',
        'description': 'Alat interaktif untuk menghitung logika fuzzy.',
        'endpoint': 'sugeno_calculator'
    },
    {
        'id': 'knapsack-ga',
        'title': 'Algoritma Genetika Knapsack',
        'thumbnail': 'assets/thumnail-knapsack.png',
        'description': 'Menemukan solusi optimal untuk masalah Knapsack menggunakan Algoritma Genetika.',
        'endpoint': 'knapsack_calculator'
    }
]

# --- Routes ---

@app.route('/')
def index():
    tasks = Task.query.all()
    for p in PROJECTS:
        p['link_url'] = url_for(p['endpoint'])
    return render_template('index.html', show_sidebar=False, tasks=tasks, projects=PROJECTS, active_nav='home')

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    tasks = Task.query.all()
    for t in tasks:
        t.link_url = url_for('task_detail', task_id=t.id)
    return render_template('task_detail.html', show_sidebar=True, task=task, 
                           sidebar_items=tasks, sidebar_title='Tugas Materi', active_nav='tugas')

@app.route('/tugas')
def tugas():
    tasks = Task.query.all()
    for t in tasks:
        t.link_url = url_for('task_detail', task_id=t.id)
    return render_template('tugas.html', show_sidebar=True, tasks=tasks, 
                           sidebar_items=tasks, sidebar_title='Tugas Materi', active_nav='tugas')

@app.route('/project')
def project():
    for p in PROJECTS:
        p['link_url'] = url_for(p['endpoint'])
    return render_template('project.html', show_sidebar=True, projects=PROJECTS,
                           sidebar_items=PROJECTS, sidebar_title='Project', active_nav='project')

@app.route('/knapsack_calculator', methods=['GET', 'POST'])
def knapsack_calculator():
    result = None
    error = None
    if request.method == 'POST':
        try:
            max_weight = float(request.form['max_weight'])
            items_json = request.form.get('items_json', '[]')
            user_items = json.loads(items_json)

            if not user_items:
                raise ValueError("Tidak ada item yang ditambahkan.")

            items = [genetic_knapsack.Item(i['name'], i['weight'], i['value']) for i in user_items]
            
            # Panggil solver dari genetic_knapsack.py
            solution = genetic_knapsack.solve(items, max_weight)
            
            # Konversi item result kembali ke dict agar mudah di-render
            solution['selected_items'] = [
                {'name': item.name, 'weight': item.weight, 'value': item.value} 
                for item in solution['selected_items']
            ]
            result = solution

        except (ValueError, KeyError, json.JSONDecodeError) as e:
            error = f"Input tidak valid atau format item salah. Harap periksa kembali. Error: {e}"
        except Exception as e:
            error = f"Terjadi kesalahan tak terduga: {e}"

    for p in PROJECTS:
        p['link_url'] = url_for(p['endpoint'])
        
    return render_template('knapsack_calculator.html', show_sidebar=True, 
                           sidebar_items=PROJECTS, sidebar_title='Project', 
                           active_nav='project', result=result, error=error, 
                           form_data=request.form)

@app.route('/sugeno_calculator', methods=['GET', 'POST'])
def sugeno_calculator():
    calculation = None
    error = None
    if request.method == 'POST':
        try:
            service_quality = float(request.form['service'])
            food_quality = float(request.form['food'])
            rules_json = request.form.get('rules_json', '[]')
            user_rules = json.loads(rules_json)

            # 1. Fuzzifikasi
            fuzz_service = {
                'poor': max(0, 1 - (service_quality / 5) if service_quality <= 5 else 0),
                'good': max(0, (service_quality - 5) / 5 if service_quality > 5 else 0)
            }
            fuzz_food = {
                'poor': max(0, 1 - (food_quality / 5) if food_quality <= 5 else 0),
                'good': max(0, (food_quality - 5) / 5 if food_quality > 5 else 0)
            }
            fuzz_values = {'service': fuzz_service, 'food': fuzz_food}

            # 2. Aturan & Inferensi
            evaluated_rules = []
            for i, rule in enumerate(user_rules):
                val1 = fuzz_values[rule['var1']][rule['set1']]
                rule_text = f"IF {rule['var1']} IS {rule['set1']}"

                if rule['op'] == 'NONE':
                    alpha = val1
                else:
                    val2 = fuzz_values[rule['var2']][rule['set2']]
                    rule_text += f" {rule['op']} {rule['var2']} IS {rule['set2']}"
                    if rule['op'] == 'AND':
                        alpha = min(val1, val2)
                    else: # OR
                        alpha = max(val1, val2)
                
                rule_text += f" THEN tip = {rule['z']} "
                evaluated_rules.append({
                    'name': f'Rule {i+1}',
                    'text': rule_text,
                    'alpha': alpha,
                    'z': float(rule['z'])
                })

            # 3. Defuzzifikasi
            numerator = sum(r['alpha'] * r['z'] for r in evaluated_rules)
            denominator = sum(r['alpha'] for r in evaluated_rules)
            final_tip = numerator / denominator if denominator != 0 else 0
            
            calculation = {
                'inputs': {'service': service_quality, 'food': food_quality},
                'fuzzification': {'service': fuzz_service, 'food': fuzz_food},
                'rules': evaluated_rules,
                'defuzzification': {'numerator': numerator, 'denominator': denominator, 'result': final_tip}
            }

        except (ValueError, KeyError, json.JSONDecodeError) as e:
            error = f"Input tidak valid atau format aturan salah. Harap periksa kembali. Error: {e}"
        except Exception as e:
            error = f"Terjadi kesalahan tak terduga: {e}"

    for p in PROJECTS:
        p['link_url'] = url_for(p['endpoint'])
        
    return render_template('sugeno_calculator.html', show_sidebar=True, 
                           sidebar_items=PROJECTS, sidebar_title='Project', 
                           active_nav='project', calculation=calculation, error=error, 
                           form_data=request.form)

@app.route('/new', methods=['GET', 'POST'])
def new_task():
    # ... (rest of the function is unchanged)
    pass

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # ... (rest of the function is unchanged)
    pass

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    # ... (rest of the function is unchanged)
    pass

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
