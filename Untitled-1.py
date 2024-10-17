import tensorflow as tf
import numpy as np
import cv2
import os
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.applications import MobileNetV2

# Caminho das imagens extraídas
image_dir = r'C:\programacao'
output_dir = r'C:\Users\renat\OneDrive\Área de Trabalho\python\imagens_tenis'  # Apenas imagens de tênis
os.makedirs(output_dir, exist_ok=True)

# Carregar o modelo MobileNetV2 pré-treinado
model = MobileNetV2(weights='imagenet')

# Função para verificar se a imagem é de um tênis
def is_sneaker(image_path):
    # Tentar abrir a imagem
    image = cv2.imread(image_path)
    
    # Verificar se a imagem foi carregada corretamente
    if image is None:
        print(f"Não foi possível carregar a imagem: {image_path}")
        return False

    # Redimensionar a imagem
    image = cv2.resize(image, (224, 224))  # Redimensionar para o tamanho esperado pelo MobileNet
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = preprocess_input(np.array(image, dtype=np.float32))
    image = np.expand_dims(image, axis=0)  # Expandir para o formato esperado pelo modelo
    
    # Fazer a predição
    predictions = model.predict(image)
    decoded = decode_predictions(predictions, top=3)[0]
    
    # Verificar se o modelo reconhece como "sneaker" ou "running_shoe" e aplicar threshold de 0.5
    for i, (_, label, score) in enumerate(decoded):
        if label in ['sneaker', 'running_shoe'] and score > 0.5:  # Threshold de confiança ajustado
            print(f"Imagem {os.path.basename(image_path)} classificada como tênis com confiança {score:.2f}")
            return True
    return False

# Processar as imagens e salvar apenas as de tênis
image_count = 0
for image_file in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_file)
    
    if is_sneaker(image_path):
        # Salvar a imagem de tênis
        output_path = os.path.join(output_dir, image_file)
        cv2.imwrite(output_path, cv2.imread(image_path))
        image_count += 1

print(f"{image_count} imagens de tênis salvas em {output_dir}")
