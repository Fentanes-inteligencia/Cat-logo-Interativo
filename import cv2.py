import cv2

# Caminho da imagem (substitua por uma imagem que você sabe que existe)
img_path = r'C:\Users\renat\OneDrive\Área de Trabalho\python\imagens_extraidas\image_9.jpeg'

# Tentando carregar a imagem
img = cv2.imread(img_path)

# Verificação se a imagem foi carregada corretamente
if img is None:
    print("Imagem não encontrada! Verifique o caminho e o nome do arquivo.")
else:
    print("Imagem carregada com sucesso!")
    
    # Exibir a imagem usando OpenCV
    cv2.imshow('Imagem Carregada', img)
    
    # Espera até que qualquer tecla seja pressionada
    cv2.waitKey(0)
    
    # Fechar todas as janelas abertas do OpenCV
    cv2.destroyAllWindows()
