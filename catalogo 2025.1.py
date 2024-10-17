import os
import pandas as pd

# Caminhos base para as imagens e a saída
base_path = r"C:\Users\renat\OneDrive\Área de Trabalho\COLEÇÃO 2025 OLY - UA"
output_folder = r"C:\Users\renat\OneDrive\Área de Trabalho\PROJETOS\catalogo_olympikus"
precos_file = r"C:\Users\renat\OneDrive\Área de Trabalho\PROJETOS\modelo e preço.xlsx"

# Carregar planilha de preços e tamanhos
df_precos = pd.read_excel(precos_file)

# Função para listar todas as subpastas dentro de uma divisão automaticamente
def listar_modelos(division_path):
    try:
        return [folder for folder in os.listdir(division_path) if os.path.isdir(os.path.join(division_path, folder))]
    except FileNotFoundError:
        return []

# Função para verificar se um valor é numérico
def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Função para obter o preço e tamanhos baseados no artigo
def obter_preco_e_tamanhos(artigo):
    if is_numeric(artigo):
        try:
            produto_info = df_precos[df_precos['Artigo'] == int(artigo)].iloc[0]
            preco = produto_info['preço']
            tamanhos = produto_info['Tamanho']  # Certifique-se de que a coluna se chama "Tamanho"
            tamanho_min, tamanho_max = map(int, tamanhos.split("/"))  # Exemplo: "34/44"
            return preco, (tamanho_min, tamanho_max)
        except (IndexError, ValueError):
            return 0.0, (33, 48)
    else:
        return 0.0, (33, 48)

# Função para gerar cartões de produtos
def generate_product_cards(division, products):
    product_cards = ""
    for product in products:
        # Caminho para o diretório de cada produto
        product_dir = os.path.join(base_path, division, product['modelo'])
        if os.path.exists(product_dir):
            # Listar todas as imagens no diretório
            imagens = [img for img in os.listdir(product_dir) if img.lower().endswith((".jpg", ".jpeg", ".png"))]
            for img in imagens:
                artigo = img[:8]  # 8 primeiros dígitos do nome do arquivo
                cor = img[8:-4]  # Parte após os 8 dígitos e antes da extensão
                preco, (tamanho_min, tamanho_max) = obter_preco_e_tamanhos(artigo)  # Obter o preço e tamanhos

                # Definindo a quantidade mínima
                quantidade_minima = 6 if preco != 0.0 and preco > 150 else 12

                # Garantir que 'preco' seja numérico para o atributo data; definir como 0 se não disponível
                try:
                    preco_val = float(preco)
                except (ValueError, TypeError):
                    preco_val = 0.0

                # Gerando os inputs para cada tamanho disponível
                tamanhos_input = ""
                for tamanho in range(tamanho_min, tamanho_max + 1):
                    tamanhos_input += f"""
                        <div style="display: flex; align-items: center; margin-bottom: 5px;">
                            <label for="tamanho_{artigo}_{tamanho}" style="width: 30px;">{tamanho}</label>
                            <input type="number" id="tamanho_{artigo}_{tamanho}" name="tamanho_{tamanho}" value="0" min="0" style="width: 50px; margin-left: 5px;" data-tamanho="{tamanho}">
                        </div>
                    """

                # Adicionando o botão "Adicionar ao Carrinho" e atributos de dados necessários
                product_cards += f"""
                <div class="produto" data-artigo="{artigo}" data-preco="{preco_val}" data-modelo="{product['modelo']}" data-cor="{cor}">
                    <img src="{product_dir}/{img}" alt="{product['modelo']} - {cor}">
                    <div class="info-produto">
                        <h3>{product['modelo']}</h3>
                        <p>Artigo: {artigo}</p>
                        <p>Cor: {cor}</p>
                        <p>Preço: R$ {preco_val:.2f}</p>
                        <p>Tamanhos disponíveis: {tamanho_min}/{tamanho_max}</p>
                    </div>
                    <div class="grade-tamanho">
                        <label for="quantidade">Quantidade (mínimo {quantidade_minima} pares):</label>
                        <input type="number" class="quantidade" min="{quantidade_minima}" value="{quantidade_minima}">
                    </div>
                    <div class="tamanhos">
                        {tamanhos_input}
                    </div>
                    <p class="multiple-indicator"></p>
                    <p>Total deste produto: R$ <span class="produto-total">0.00</span></p>
                    <button class="add-to-cart">Adicionar ao carrinho</button>
                </div>
                """
    return product_cards

# Template HTML para o catálogo de divisão
division_template = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Catálogo Interativo Olympikus - {division}</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .catalogo {{ display: flex; flex-wrap: wrap; }}
        .produto {{ border: 1px solid #ddd; padding: 10px; margin: 10px; width: 300px; }}
        .produto img {{ width: 100%; }}
        .info-produto {{ margin-top: 10px; }}
        .grade-tamanho {{ margin-top: 10px; }}
        .tamanhos {{ margin-top: 10px; }}
        label {{ margin-right: 10px; }}
        .quantidade {{ width: 50px; }}
        /* Estilos para o resumo do carrinho */
        #cart-summary {{
            position: fixed;
            top: 10px;
            right: 10px;
            border: 1px solid #ddd;
            padding: 10px;
            background: #fff;
            width: 300px;
            max-height: 80vh;
            overflow-y: auto;
        }}
        #cart-summary h2 {{ margin-top: 0; }}
        #cart-items div {{ margin-bottom: 5px; }}
        /* Estilos para o botão de checkout */
        #checkout-button {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 15px 30px;
            background-color: #28a745;
            color: #fff;
            border: none;
            font-size: 18px;
            cursor: pointer;
        }}
        #checkout-button:hover {{
            background-color: #218838;
        }}
        /* Estilo para o indicador de múltiplo de 6 */
        .multiple-indicator {{
            font-weight: bold;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <h1>Catálogo de Produtos Olympikus - {division}</h1>
    
    <!-- Exibição do Resumo do Carrinho -->
    <div id="cart-summary">
        <h2>Carrinho</h2>
        <div id="cart-items"></div>
        <p>Total do pedido: R$ <span id="cart-total">0.00</span></p>
    </div>
    
    <div class="catalogo">
        {products}
    </div>
    <a href="index.html">Voltar para o início</a>

    <!-- Botão para ir ao Checkout -->
    <a href="checkout.html"><button id="checkout-button">Finalizar Pedido</button></a>

    <!-- JavaScript para Funcionalidade do Carrinho -->
    <script>
        var cart = {{}};

        // Função para salvar o carrinho no localStorage
        function saveCart() {{
            localStorage.setItem('cart', JSON.stringify(cart));
        }}

        // Função para carregar o carrinho do localStorage
        function loadCart() {{
            var savedCart = localStorage.getItem('cart');
            if (savedCart) {{
                cart = JSON.parse(savedCart);
                updateCartDisplay();
            }}
        }}

        function updateCartDisplay() {{
            var cartItemsDiv = document.getElementById('cart-items');
            cartItemsDiv.innerHTML = '';
            var totalPedido = 0;
            for (var key in cart) {{
                if (cart.hasOwnProperty(key)) {{
                    var item = cart[key];
                    var itemTotal = item.preco * item.totalQuantity;
                    totalPedido += itemTotal;

                    // Detalhes dos tamanhos e quantidades
                    var sizesDetails = '';
                    for (var tamanho in item.sizes) {{
                        sizesDetails += 'Tamanho ' + tamanho + ': ' + item.sizes[tamanho] + ' pares<br>';
                    }}

                    cartItemsDiv.innerHTML += '<div><strong>' + item.modelo + ' - ' + item.cor + '</strong><br>' +
                        sizesDetails +
                        'Quantidade total: ' + item.totalQuantity + ' pares<br>' +
                        'Total do produto: R$ ' + itemTotal.toFixed(2) + '</div><hr>';
                }}
            }}
            document.getElementById('cart-total').innerText = totalPedido.toFixed(2);
        }}

        function calculateProductTotal(productDiv) {{
            var preco = parseFloat(productDiv.getAttribute('data-preco'));
            var totalQuantity = 0;
            var tamanhoInputs = productDiv.querySelectorAll('.tamanhos input[type="number"]');
            tamanhoInputs.forEach(function(input) {{
                var quantidade = parseInt(input.value) || 0;
                if (quantidade > 0) {{
                    totalQuantity += quantidade;
                }}
            }});
            var produtoTotal = preco * totalQuantity;
            productDiv.querySelector('.produto-total').innerText = produtoTotal.toFixed(2);

            // Chamar a função para verificar múltiplo de 6
            checkMultipleOfSix(productDiv);
        }}

        // Função para verificar se a quantidade total é múltiplo de 6
        function checkMultipleOfSix(productDiv) {{
            var totalQuantity = 0;
            var tamanhoInputs = productDiv.querySelectorAll('.tamanhos input[type="number"]');
            tamanhoInputs.forEach(function(input) {{
                var quantidade = parseInt(input.value) || 0;
                totalQuantity += quantidade;
            }});

            var multipleIndicator = productDiv.querySelector('.multiple-indicator');
            if (totalQuantity % 6 === 0 && totalQuantity > 0) {{
                multipleIndicator.textContent = 'Quantidade total é múltiplo de 6.';
                multipleIndicator.style.color = 'green';
            }} else {{
                var remaining = 6 - (totalQuantity % 6);
                if (remaining < 0) {{
                    remaining += 6;
                }}
                multipleIndicator.textContent = 'Adicione mais ' + remaining + ' pares para atingir um múltiplo de 6.';
                multipleIndicator.style.color = 'red';
            }}
        }}

        function addToCart(event) {{
            var productDiv = event.target.closest('.produto');
            var artigo = productDiv.getAttribute('data-artigo');
            var preco = parseFloat(productDiv.getAttribute('data-preco'));
            var modelo = productDiv.getAttribute('data-modelo');
            var cor = productDiv.getAttribute('data-cor');
            var quantidadeMinima = parseInt(productDiv.querySelector('.quantidade').getAttribute('min'));
            var totalQuantity = 0;
            var sizes = {{}};

            var tamanhoInputs = productDiv.querySelectorAll('.tamanhos input[type="number"]');
            tamanhoInputs.forEach(function(input) {{
                var tamanho = input.getAttribute('data-tamanho');
                var quantidade = parseInt(input.value) || 0;
                if (quantidade > 0) {{
                    sizes[tamanho] = quantidade;
                    totalQuantity += quantidade;
                }}
            }});

            if (totalQuantity < quantidadeMinima) {{
                alert('A quantidade mínima para este produto é ' + quantidadeMinima + ' pares.');
                return;
            }}

            // Verificar se a quantidade total é múltiplo de 6
            if (totalQuantity % 6 !== 0) {{
                alert('A quantidade total deve ser um múltiplo de 6.');
                return;
            }}

            // Adicionar ou atualizar o item no carrinho
            cart[artigo] = {{
                artigo: artigo,
                preco: preco,
                modelo: modelo,
                cor: cor,
                sizes: sizes,
                totalQuantity: totalQuantity
            }};

            saveCart(); // Salvar o carrinho no localStorage
            updateCartDisplay();
        }}

        // Adicionar event listeners aos botões "Adicionar ao Carrinho" e inputs de quantidade
        document.addEventListener('DOMContentLoaded', function() {{
            loadCart(); // Carregar o carrinho ao iniciar a página

            var addToCartButtons = document.querySelectorAll('.add-to-cart');
            addToCartButtons.forEach(function(button) {{
                button.addEventListener('click', addToCart);
            }});

            var tamanhoInputs = document.querySelectorAll('.tamanhos input[type="number"]');
            tamanhoInputs.forEach(function(input) {{
                input.addEventListener('input', function(event) {{
                    var productDiv = event.target.closest('.produto');
                    calculateProductTotal(productDiv);
                }});
            }});
        }});
    </script>
</body>
</html>
"""

# As demais funções permanecem as mesmas

# Função para gerar uma página HTML para cada divisão
def generate_division_page(division, products):
    # Gerar o HTML com os produtos da divisão
    division_html = division_template.format(division=division, products=generate_product_cards(division, products))
    
    # Caminho do arquivo HTML da divisão
    division_html_path = os.path.join(output_folder, f"{division.lower()}.html")
    
    # Salvar a página da divisão
    with open(division_html_path, "w", encoding="utf-8") as file:
        file.write(division_html)
    
    print(f"Página da divisão '{division}' gerada com sucesso: {division_html_path}")

# Função para gerar links para as divisões na página inicial
def generate_index_page(division_names):
    division_links = ""
    for division in division_names:
        division_links += f'<div class="divisao"><a href="{division.lower()}.html">{division}</a></div>'
    
    # Gerar o HTML da página inicial
    index_html = f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Catálogo Interativo Olympikus</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .divisoes {{ display: flex; flex-wrap: wrap; }}
            .divisao {{ border: 1px solid #ddd; padding: 20px; margin: 20px; width: 200px; text-align: center; }}
        </style>
    </head>
    <body>
        <h1>Catálogo de Produtos Olympikus</h1>
        <div class="divisoes">
            {division_links}
        </div>
    </body>
    </html>
    """
    
    # Caminho do arquivo HTML da página inicial
    index_html_path = os.path.join(output_folder, "index.html")
    
    # Salvar a página inicial
    with open(index_html_path, "w", encoding="utf-8") as file:
        file.write(index_html)
    
    print(f"Página inicial gerada com sucesso: {index_html_path}")

# Função para gerar a página de checkout (mantida conforme a versão anterior)
def generate_checkout_page():
    # ... o conteúdo da função permanece o mesmo ...
    pass  # Mantenha a função existente ou atualize se necessário

# Função para gerar o catálogo completo
def generate_full_catalog():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Lista de divisões e seus modelos
    divisao_paths = ["CAMINHADA", "CORRIDA", "CASUAL", "CHINELOS", "INFANTIL", "TREINO"]

    for division in divisao_paths:
        # Caminho para a divisão
        division_path = os.path.join(base_path, division)
        
        # Listar todos os modelos (subpastas) dentro da divisão
        models = listar_modelos(division_path)

        # Simulação de dados de produtos por divisão e modelo
        products = [{"artigo": f"{str(i).zfill(8)}", "modelo": model} for i, model in enumerate(models, start=10000000)]

        # Gerar a página da divisão
        generate_division_page(division, products)

    # Gerar a página inicial
    generate_index_page(divisao_paths)

    # Gerar a página de checkout
    generate_checkout_page()

# Gerar o catálogo completo
generate_full_catalog()
