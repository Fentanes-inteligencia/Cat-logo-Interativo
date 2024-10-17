import pandas as pd
import folium
from geopy.geocoders import Nominatim

# Função para obter coordenadas com base na cidade
def get_lat_lon(city):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.geocode(city + ', Bahia, Brazil')
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Não foi possível obter coordenadas para {city}")
            return None, None
    except Exception as e:
        print(f"Erro ao tentar obter coordenadas para {city}: {e}")
        return None, None

# Carregar o arquivo CSV com a base de dados organizada
file_path = r"C:\Users\renat\OneDrive\Área de Trabalho\Olympikus importante\Cadastro_de_Clientes_Organizado.csv"
df_base = pd.read_csv(file_path)

# Filtrar as colunas necessárias
df_clientes = df_base[['Cliente', 'Razão Social', 'Grupos', 'Cidade']]

# Remover duplicatas, se houver
df_clientes = df_clientes.drop_duplicates(subset=['Cidade', 'Cliente'])

# Obter coordenadas para cada cidade
df_clientes[['Latitude', 'Longitude']] = df_clientes['Cidade'].apply(lambda x: pd.Series(get_lat_lon(x)))

# Criar o mapa centralizado na Bahia
map_bahia = folium.Map(location=[-13.001, -41.502], zoom_start=7)

# Adicionar marcadores para cada cliente
for _, row in df_clientes.dropna(subset=['Latitude', 'Longitude']).iterrows():
    popup_info = f"Razão Social: {row['Razão Social']}<br>Grupo: {row['Grupos']}<br>Cliente Nº: {row['Cliente']}"
    folium.Marker(location=[row['Latitude'], row['Longitude']], popup=popup_info).add_to(map_bahia)

# Salvar o mapa em um arquivo HTML no diretório correto
output_file = r"C:\Users\renat\OneDrive\Área de Trabalho\python\map_bahia_clients_renato.html"
map_bahia.save(output_file)

print(f"Mapa gerado e salvo como '{output_file}'. Verifique na pasta se o arquivo foi criado.")
