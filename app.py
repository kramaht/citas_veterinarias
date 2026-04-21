from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'citas.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            mascota   TEXT NOT NULL,
            propietario TEXT NOT NULL,
            especie   TEXT,
            fecha     TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# ── AGENDA (ruta principal) ──────────────────────────────────────────────────
@app.route('/')
def agenda():
    conn = get_db()
    citas = conn.execute('SELECT * FROM pacientes ORDER BY fecha').fetchall()
    conn.close()
    return render_template('agenda.html', citas=citas)


# ── AGENDAR ──────────────────────────────────────────────────────────────────
@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        mascota    = request.form['mascota']
        propietario = request.form['propietario']
        especie    = request.form['especie']
        fecha      = request.form['fecha']
        conn = get_db()
        conn.execute(
            'INSERT INTO pacientes (mascota, propietario, especie, fecha) VALUES (?, ?, ?, ?)',
            (mascota, propietario, especie, fecha)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('agenda'))
    return render_template('agendar.html')





if __name__ == '__main__':
    init_db()
    app.run(debug=True)
