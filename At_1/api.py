from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/calculadora", methods=['POST'])
def calculadora():
    data = request.get_json()

    if not data or 'a' not in data or 'b' not in data or 'operacao' not in data:
        return jsonify({'error': 'Esqueceu colocar um dos dados!'}), 400
    
    numero1 = data['a']
    numero2 = data['b']
    operacao = data['operacao']
    resultado = 0

    if operacao == "soma":
        resultado = numero1 + numero2
    elif operacao == "subtração":
        resultado = numero1 - numero2
    elif operacao == "multiplicação":
        resultado = numero1 * numero2
    elif operacao == "divisão":
        resultado = numero1 / numero2    

    return jsonify({
        "calculadora": {
            'a': numero1,
            'b': numero2,
            'operacao': operacao,
            'resultado': resultado
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
