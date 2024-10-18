from flask import Flask, render_template

app = Flask(__name__)

# Exemplo de dados que você pode passar para o template
produtos = [
    {"produto": "Tênis 1", "codigo": "1234", "cores": [{"abrev": "BR", "nome": "Branco", "numeracao": {38: 5, 39: 3}}]},
    {"produto": "Tênis 2", "codigo": "5678", "cores": [{"abrev": "PR", "nome": "Preto", "numeracao": {40: 6, 41: 4}}]}
]

@app.route('/')
def catalogo():
    return render_template('catalogo.html', produtos=produtos)

if __name__ == '__main__':
    app.run(debug=True)
