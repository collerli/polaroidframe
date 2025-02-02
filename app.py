import streamlit as st
from PIL import Image, ImageDraw
import io

def create_polaroid(image, output_size=(1100, 1400), frame_width=40, bottom_frame_height=100):
    img = image.convert("RGB")
    
    # Calcular o tamanho da imagem a ser ajustado dentro da polaroid
    img_width, img_height = img.size
    frame_width = 40
    bottom_frame_height = 100
    
    # Ajustando as dimensões da imagem para caber na área disponível da polaroid
    available_width = output_size[0] - 2 * frame_width  # Subtrair a moldura esquerda e direita
    available_height = output_size[1] - frame_width - bottom_frame_height  # Subtrair a moldura superior e inferior
    
    aspect_ratio = img_width / img_height
    new_width = available_width
    new_height = int(new_width / aspect_ratio)
    
    if new_height > available_height:
        new_height = available_height
        new_width = int(new_height * aspect_ratio)
    
    # Redimensionar a imagem para que ocupe toda a área disponível, sem distorcer
    img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Criar uma imagem polaroid com a moldura branca e a parte inferior mais larga
    polaroid = Image.new("RGB", output_size, "whitesmoke")
    
    # Calcular a posição para centralizar a imagem na polaroid
    x_offset = (output_size[0] - new_width) // 2
    y_offset = (output_size[1] - new_height - bottom_frame_height) // 2
    
    # Colar a imagem redimensionada na polaroid
    polaroid.paste(img, (x_offset, y_offset))
    
    # Desenhar a moldura ao redor da imagem
    draw = ImageDraw.Draw(polaroid)
    
    # Definindo as coordenadas para a moldura
    frame_box = (frame_width, frame_width, output_size[0] - frame_width, output_size[1] - bottom_frame_height)
    
    # Desenhar a moldura (sem cor para o espaço interno da imagem)
    draw.rectangle(frame_box, outline="white", width=frame_width)
    
    return polaroid

def generate_a4_collage(images, output_file="output_a4.jpg"):
    a4_size = (2480, 3508)  # Tamanho A4 a 300 DPI
    polaroid_size = (1100, 1400)  # Tamanho ajustado das polaroids para 1100x1400
    collage = Image.new("RGB", a4_size, "white")
    
    # Definir posições para as 4 polaroids, ajustando para usar mais da área A4
    positions = [(100, 100), (1380, 100), (100, 1800), (1380, 1800)]
    
    for i, img in enumerate(images):
        polaroid = create_polaroid(img, polaroid_size)
        collage.paste(polaroid, positions[i])
    
    collage.save(output_file, quality=95)
    return collage

st.title("Polaroid A4 Generator")
uploaded_files = st.file_uploader("Upload 4 images", accept_multiple_files=True, type=["jpg", "png"], key="images")

if uploaded_files and len(uploaded_files) == 4:
    images = [Image.open(file) for file in uploaded_files]
    result_image = generate_a4_collage(images)
    
    # Mostrar a imagem gerada
    st.image(result_image, caption="Generated A4 Collage", use_column_width=True)
    
    # Salvar a imagem como JPG e gerar um link para download
    img_bytes = io.BytesIO()
    result_image.save(img_bytes, format="JPEG", quality=95)
    img_bytes.seek(0)
    
    # Botão para download
    st.download_button("Download Collage", data=img_bytes, file_name="output_a4.jpg", mime="image/jpeg")
else:
    st.warning("Please upload exactly 4 images.")
