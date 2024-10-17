import os

# Definir a estrutura de divisões e os produtos baseados no caminho que você especificou
divisoes = {
    "CAMINHADA": ["130G ULTRALEVE", "DIFFUSE 5"],
    "CASUAL": ["CLIC", "EROS", "FLUTUA"],
    "CHINELOS": ["ANGRA", "CARAIVA"],
    "INFANTIL": ["DYNAMIC INFANTIL", "EROS INFANTIL"],
    "TREINO": ["SONORO 3", "QUADRA BR1"]
}

# Caminho base para as imagens
base_path = r"C:\Users\renat\OneDrive\Área de Trabalho\COLEÇÃO 2025 OLY - UA"

# Função para gerar cartões de produtos dinamicamente com base nos dados
def generate_product_cards(division, products):
    product_cards = ""
    for product in products:
        # Caminho para o diretório de cada produto
        product_dir = os.path.join(base_path, division, product['modelo'])
        if os.path.exists(product_dir):
            # Listar todas as imagens no diretório
            imagens = [img for img in os.listdir(product_dir) if img.endswith(".jpg") or img.endswith(".jpeg")]
            for img in imagens:
                product_cards += f"""
                <div class="produto">
                    <img src="{product_dir}/{img}" alt="{product['modelo']} - {img}">
                    <div class="info-produto">
                        <h3>{product['modelo']}</h3>
                        <p>Artigo: {product['artigo']}</p>
                        <p>Cor: {img[8:-4]}</p> <!-- Extrai a cor a partir do nome da imagem -->
                    </div>
                    <div class="grade-tamanho">
                        <label for="quantidade">Quantidade (mínimo 12 pares):</label>
                        <input type="number" class="quantidade" min="12" value="12">
                    </div>
                </div>
                """
    return product_cards

# Template HTML para o catálogo por divisões
html_template = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Catálogo Interativo Olympikus</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .catalogo {{ display: flex; flex-wrap: wrap; }}
        .produto {{ border: 1px solid #ddd; padding: 10px; margin: 10px; width: 300px; }}
        .produto img {{ width: 100%; }}
        .info-produto {{ margin-top: 10px; }}
        .grade-tamanho {{ margin-top: 10px; }}
        label {{ margin-right: 10px; }}
        .quantidade {{ width: 50px; }}
    </style>
</head>
<body>
    <h1>Catálogo de Produtos Olympikus - {division}</h1>
    <div class="catalogo">
        {products}
    </div>
</body>
</html>
"""

# Função para gerar catálogo interativo completo por divisão
def generate_full_catalog():
    for division, models in divisoes.items():
        # Simulação de dados de produtos por divisão e modelo
        products = [{"artigo": f"{str(i).zfill(8)}", "modelo": model} for i, model in enumerate(models, start=10000000)]

        # Gerar os cartões de produtos
        product_cards_html = generate_product_cards(division, products)

        # Gerar o HTML final com base na divisão e produtos
        final_html = html_template.format(division=division, products=product_cards_html)

        # Caminho onde será salvo o arquivo HTML
        output_html_path = f"catalogo_interativo_olympikus_{division.lower()}.html"

        # Escrever o arquivo HTML
        with open(output_html_path, "w", encoding="utf-8") as file:
            file.write(final_html)

        print(f"Catálogo gerado com sucesso para {division}: {output_html_path}")

# Gerar o catálogo completo
generate_full_catalog()
