import PyPDF2
from deep_translator import GoogleTranslator

def traduzir_texto(texto):
    tradutor = GoogleTranslator(source='auto', target='pt')
    # Divide o texto em partes de até 5000 caracteres
    partes = [texto[i:i+5000] for i in range(0, len(texto), 5000)]
    traduzido = []
    for parte in partes:
        try:
            trad = tradutor.translate(parte)
            traduzido.append(trad)
        except Exception as e:
            print(f"Erro ao traduzir: {e}")
    return ' '.join(traduzido)

caminho_pdf = "/storage/emulated/0/Cursos/english.pdf"

try:
    with open(caminho_pdf, "rb") as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        texto_total = []
        for pagina in leitor.pages:
            texto = pagina.extract_text()
            if texto:
                texto_total.append(texto)
        texto_total = '\n'.join(texto_total)
    
    texto_traduzido = traduzir_texto(texto_total)
    
    with open("traducao.txt", "w", encoding="utf-8") as f:
        f.write(texto_traduzido)
    
    print("Tradução salva em 'traducao.txt'")

except FileNotFoundError:
    print("Arquivo PDF não encontrado!")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
