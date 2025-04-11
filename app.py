import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import PyPDF2
from deep_translator import (GoogleTranslator,
                             ChatGptTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def traduzir_texto(texto):
    tradutor = GoogleTranslator(source='auto', target='pt')
    partes = [texto[i:i+5000] for i in range(0, len(texto), 5000)]
    traduzido = []
    for parte in partes:
        try:
            trad = tradutor.translate(parte)
            traduzido.append(trad)
        except Exception as e:
            print(f"Erro na tradução: {e}")
            traduzido.append("[Texto não traduzido]")
    return ' '.join(traduzido)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            return "Nenhum arquivo enviado!"
        
        arquivo = request.files['pdf']
        if arquivo.filename == '':
            return "Nenhum arquivo selecionado!"
        
        if arquivo and arquivo.filename.endswith('.pdf'):
            filename = secure_filename(arquivo.filename)
            caminho_pdf = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            arquivo.save(caminho_pdf)
            
            # Extrair texto do PDF
            texto_total = []
            with open(caminho_pdf, 'rb') as f:
                leitor = PyPDF2.PdfReader(f)
                for pagina in leitor.pages:
                    texto = pagina.extract_text()
                    if texto:
                        texto_total.append(texto)
            
            texto_total = '\n'.join(texto_total)
            texto_traduzido = traduzir_texto(texto_total)
            
            # Salvar tradução
            caminho_txt = os.path.join(app.config['UPLOAD_FOLDER'], 'traducao.txt')
            with open(caminho_txt, 'w', encoding='utf-8') as f:
                f.write(texto_traduzido)
            
            # Limpar o PDF após uso
            os.remove(caminho_pdf)
            
            return send_file(
                caminho_txt,
                as_attachment=True,
                download_name='traducao.pdf',
                mimetype='application/pdf'
            )
    
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
