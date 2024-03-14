import os, sys

#from controlVB import read_Vcc_R
from website import create_app
from flask import send_from_directory, request

# Obtém o diretório atual do script
current_dir = os.path.dirname(__file__)
# Adiciona o diretório ctrl_hardware ao caminho de busca de módulos do Python
ctrl_hardware_dir = os.path.join(current_dir, 'ctrl_hardware')
sys.path.append(ctrl_hardware_dir)

app = create_app()
app.config['SECRET_KEY'] = 'thisisasecretkey'

@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory("images", filename)

# Definição dos bits a serem transmitidos

#Rota para receber o parâmetro binário e usar no shift_register.py
@app.route('/atualizar_shift_register', methods=['GET'])
def atualizar_shift_register():
    parametro = request.args.get('parametro','')
    # Remove o prefixo '0b' se presente
    if parametro.startswith('0b'):
        parametro = parametro[2:]     

    # Chama a função SRoutput do shift_register.py passando o parâmetro binário
    #SRoutput(int(parametro,2)) #Converte o parâmetro binário para inteiro
    return f'Parâmetro binário {parametro} passado com sucesso!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #efenido para executar em todos os ip's disponíveis pela rede
