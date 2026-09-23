from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/estudantes')
def estudantes():
    return render_template('estudantes.html')

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

@app.route('/inscricoes')
def inscricoes():
    return render_template('inscricoes.html')

if __name__ == '__main__':
    app.run(debug=True)
