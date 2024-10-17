import fitz  # PyMuPDF
import os

# Caminho do PDF
pdf_path = r'C:\Users\renat\OneDrive\Área de Trabalho\Motando catalogo de tenis interativo\CATÁLOGO_Tênis 2024_novo_baixa_12.08.pdf'

# Diretório para salvar as imagens extraídas
output_dir = r'C:\Users\renat\OneDrive\Área de Trabalho\python\imagens_extraidas'
os.makedirs(output_dir, exist_ok=True)

# Abrir o PDF
doc = fitz.open(pdf_path)

# Contador de imagens
image_count = 0

# Iterar sobre as páginas do PDF
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    images = page.get_images(full=True)

    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]  # Extensão da imagem (png, jpg, etc.)
        
        # Nome da imagem salva
        image_filename = f"image_{page_num+1}_{img_index}.{image_ext}"
        image_path = os.path.join(output_dir, image_filename)
        
        # Salvar a imagem
        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)
        
        image_count += 1

print(f"{image_count} imagens extraídas para {output_dir}")
