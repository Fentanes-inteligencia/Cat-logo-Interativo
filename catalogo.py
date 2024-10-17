<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Catálogo Interativo</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .catalogo { display: flex; flex-wrap: wrap; }
        .produto { border: 1px solid #ddd; padding: 10px; margin: 10px; width: 300px; }
        .produto img { width: 100%; }
        .info-produto { margin-top: 10px; }
        .grade-tamanho { margin-top: 10px; }
        label { margin-right: 10px; }
        .quantidade { width: 50px; margin-right: 10px; }
        .total { font-weight: bold; margin-top: 20px; }
        .adicionar-btn { margin-top: 10px; padding: 10px 15px; background-color: #28a745; color: white; border: none; cursor: pointer; }
    </style>
    <script>
        let total = 0;

        function adicionarAoCarrinho(preco, idTamanho) {
            const quantidade = document.getElementById(idTamanho).value;
            const subtotal = preco * quantidade;
            total += subtotal;
            document.getElementById("total").innerText = `Total: R$ ${total.toFixed(2)}`;
        }
    </script>
</head>
<body>

    <h1>Catálogo Interativo</h1>

    <div class="catalogo">
        <!-- Produto 1 -->
        <div class="produto">
            <img src="image_1.jpg" alt="Tênis Reverso 2">
            <div class="info-produto">
                <h2>Olympikus Reverso 2</h2>
                <p>Código: 43634202</p>
                <p>Preço: R$ 379,99</p>
                <p>Tamanhos: 34/45</p>
                <p>Peso: 332g</p>
                <p>Indicação: Corrida leve</p>
            </div>

            <!-- Interatividade - Seleção de tamanhos -->
            <div class="grade-tamanho">
                <label for="quantidade34">Tamanho 34:</label>
                <input type="number" id="quantidade34" class="quantidade" min="0" value="0">
                <button class="adicionar-btn" onclick="adicionarAoCarrinho(379.99, 'quantidade34')">Adicionar ao Carrinho</button>
            </div>

            <div class="grade-tamanho">
                <label for="quantidade35">Tamanho 35:</label>
                <input type="number" id="quantidade35" class="quantidade" min="0" value="0">
                <button class="adicionar-btn" onclick="adicionarAoCarrinho(379.99, 'quantidade35')">Adicionar ao Carrinho</button>
            </div>

            <div class="grade-tamanho">
                <label for="quantidade36">Tamanho 36:</label>
                <input type="number" id="quantidade36" class="quantidade" min="0" value="0">
                <button class="adicionar-btn" onclick="adicionarAoCarrinho(379.99, 'quantidade36')">Adicionar ao Carrinho</button>
            </div>
        </div>
    </div>

    <!-- Exibir o valor total -->
    <div class="total">
        <p id="total">Total: R$ 0,00</p>
    </div>

</body>
</html>
