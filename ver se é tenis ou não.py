import cv2
import os

# Caminho da pasta com as imagens
caminho_pasta_imagens = r'C:\Users\renat\OneDrive\Área de Trabalho\python\imagens_extraidas'

# Lista todas as imagens na pasta
arquivos_imagens = os.listdir(caminho_pasta_imagens)

# Itera sobre cada arquivo de imagem e tenta carregar e exibir
for arquivo_imagem in arquivos_imagens:
    caminho_completo = os.path.join(caminho_pasta_imagens, arquivo_imagem)
    
    # Tenta carregar a imagem
    imagem = cv2.imread(caminho_completo)
    
    # Verifica se a imagem foi carregada corretamente
    if imagem is None:
        print(f"Não foi possível carregar a imagem: {caminho_completo}")
    else:
        print(f"Imagem carregada com sucesso: {caminho_completo}")
        
        # Exibe a imagem
        cv2.imshow('Imagem', imagem)
        
        # Aguarda o usuário pressionar uma tecla para fechar a janela
        cv2.waitKey(0)
        cv2.destroyAllWindows()
