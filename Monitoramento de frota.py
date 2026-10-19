import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

# AUTENTICACAO
load_dotenv(".env")

s = requests.Session()
token = os.getenv('SPTRANS_TOKEN')

res_auth = s.post(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}"
)
    # BUSCA POR LINHAS
res_linhas = s.get(
        "http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca=675K-10"
    )
linhas = res_linhas.json()
    
if isinstance(linhas, list) and len(linhas) > 0:
        codigo_linha = linhas[0]['cl']
        print(f"Linha encontrada! Código identificador: {codigo_linha}")
        
        # BUSCA POR PARADAS DA LINHA
        res_paradas = s.get(
            f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo_linha}"
        )
        paradas = res_paradas.json()
        
        # BUSCA POR POSIÇÃO DOS ÔNIBUS EM TEMPO REAL
        res_posicao = s.get(
            f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={codigo_linha}"
        )
        posicao = res_posicao.json()
        
        # MAPA
        centro_lat, centro_lon = -23.55052, -46.633308
        if isinstance(paradas, list) and len(paradas) > 0:
            centro_lat, centro_lon = paradas[0]["py"], paradas[0]["px"]
            
        m = Map(location=[centro_lat, centro_lon], zoom_start=13)

        # PIN PARADAS
        if isinstance(paradas, list):
            print(f"Adicionando {len(paradas)} paradas ao mapa")
            for p in paradas:
                Marker(
                    location=[p["py"], p["px"]],
                    popup=f"Parada: {p['np']}",
                    icon=Icon(color='blue', icon='info-sign')
                ).add_to(m)

        # PIN ONIBUS
        if isinstance(posicao, dict) and 'vs' in posicao:
                    veiculos = posicao['vs']
                    print(f"Adicionando {len(veiculos)} ônibus em tempo real ao mapa")
                    for v in veiculos:
                        Marker(
                            location=[v["py"], v["px"]],
                            popup=f"Ônibus: {v['a']}",
                            icon=Icon(color='red', icon='play')
                        ).add_to(m)
        else:
            print("Nenhum ônibus em circulação ativa no momento.")
        
        m.show_in_browser()

else:
    print("Não foi possível encontrar a linha desejada")