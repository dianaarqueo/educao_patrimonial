# app.py - CÓDIGO FINAL PARA STREAMLIT

import streamlit as st
import random

# --- 0. FUNÇÃO PARA INJETAR ESTILO CSS ---
def adicionar_estilo_css():
    """Injeta CSS personalizado para fundo, fontes e layout."""
    
    # URL de uma imagem de fundo (ex: papel antigo ou mapa)
    # ATENÇÃO: Use URLs HTTPS de imagens públicas (ex: Imgur, Pixabay, etc.)
    # Esta é uma URL de exemplo. Você pode trocar por uma de sua preferência.
    BACKGROUND_URL = "https://i.imgur.com/k6rQx5j.png" # Exemplo: textura de pergaminho/mapa

    css = f"""
    <style>
    /* 1. Fundo do Aplicativo (Main App Container) */
    [data-testid="stAppViewContainer"] {{
        background-image: url("{BACKGROUND_URL}");
        background-size: cover;
        background-attachment: fixed; /* Mantém o fundo fixo ao rolar */
    }}

    /* 2. Fundo da Barra Lateral (Sidebar) */
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 250, 240, 0.7); /* Bege claro semi-transparente */
        border-right: 2px solid #a0522d; /* Borda marrom */
    }}

    /* 3. Fundo do Conteúdo Principal (para melhorar a leitura) */
    .main > div {{
        background-color: rgba(255, 255, 255, 0.6); /* Fundo branco semi-transparente */
        padding: 20px;
        border-radius: 10px;
    }}
    
    /* 4. Fontes e Cores */
    html, body, [class*="css"] {{
        font-family: Georgia, serif; /* Fonte clássica/serif */
        color: #333333; /* Texto em cinza escuro */
    }}
    
    /* Títulos */
    h1, h2, h3, h4, h5, h6 {{
        color: #5d4037; /* Marrom escuro */
        font-family: 'Times New Roman', serif;
        border-bottom: 2px solid #5d4037;
        padding-bottom: 5px;
    }}

    /* Estilo da Palavra Secreta */
    code {{
        background-color: #f0e68c; /* Cor de papiro/ouro claro */
        color: #8b4513; /* Marrom para destaque */
        padding: 5px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 1.2em;
    }}
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- 1. Dicionário de Palavras e Dicas FINAL ---
DICIONARIO_ARQUEOLOGIA = {
    "Fácil": {
        "VESTIGIO": "Qualquer traço ou marca da presença humana deixada no passado.",
        "ESCAVACAO": "Método principal de trabalho de campo para retirar artefatos do solo.",
        "CULTURA": "O conjunto de hábitos, crenças e vestígios materiais de uma sociedade.",
        "RUINA": "O que resta de uma construção antiga, frequentemente o foco de estudo.",
        "HISTORIA": "A disciplina que a Arqueologia ajuda a reescrever, focada no passado humano.",
        "CERAMICA": "Objeto feito de argila cozida, muito comum em sítios antigos.",
        "CAMADA": "Cada nível de solo que representa um período de tempo diferente (estratigrafia).",
        "SITIO": "Termo para o local onde se encontra um conjunto de vestígios arqueológicos.",
        "MUSEU": "Onde os artefatos são catalogados, estudados e expostos ao público.",
        "ARTEFATO": "Qualquer objeto modificado ou fabricado por seres humanos."
    },
    "Médio": {
        "ESTRATIGRAFIA": "Estudo das camadas (níveis) do solo para entender a cronologia dos depósitos.",
        "PINTURA RUPESTRE": "Arte deixada nas cavernas ou rochas, geralmente da Idade da Pedra.",
        "CONSERVACAO": "Conjunto de práticas para proteger artefatos e sítios da degradação.",
        "TIPOLOGIA": "Classificação de artefatos por tipo e forma.",
        "PROSPECCAO": "Busca sistemática de sítios arqueológicos antes da escavação.",
        "JAZIDA": "Local de concentração de minérios, fósseis ou vestígios arqueológicos.",
        "SEPULTAMENTO": "Vestígio de enterro humano ou animal.",
        "RADIOCARBONO": "Método de datação que usa o isótopo de carbono 14.",
        "LITICO": "Relativo a objetos ou ferramentas feitas de pedra.",
        "TOPOGRAFIA": "O estudo e mapeamento detalhado da superfície terrestre de um sítio."
    },
    "Difícil": {
        "TRADICAO": "Costumes e práticas passadas de geração em geração dentro de um grupo cultural.",
        "ASSENTAMENTO": "Local onde uma comunidade humana se estabeleceu e deixou vestígios de moradia.",
        "TAFONOMIA": "Estudo de como os organismos se tornam fósseis.",
        "ETNOARQUEOLOGIA": "Estudo de sociedades vivas para criar analogias e entender o passado.",
        "ANTROPOFAGIA": "Prática cultural de consumir carne humana, cujos vestígios são estudados.",
        "PALEOPATOLOGIA": "Estudo de doenças e ferimentos em restos humanos antigos.",
        "ACERVO": "O conjunto total de objetos e documentos de uma coleção ou museu.",
        "TERMOLUMINESCENCIA": "Método de datação baseado na emissão de luz por minerais aquecidos (como cerâmica).",
        "CONTEXTO": "A posição e a relação dos vestígios no sítio, crucial para a interpretação.",
        "PALEOAMBIENTE": "O ambiente em que viviam as sociedades passadas."
    },
    "Específico": {
        "Clássica": {
            "EGIPTOLOGIA": "Subárea dedicada ao estudo do Antigo Egito.",
            "PAPIRO": "Material de escrita usado no Egito e Roma, feito de planta.",
            "HELENISTICO": "Período entre a morte de Alexandre, o Grande, e o domínio romano.",
            "TUMULO": "Construção destinada a sepultamento.",
            "HERCULANO": "Cidade romana destruída e preservada pela erupção do Vesúvio."
        },
        "Subaquática": {
            "NAUFRAGIO": "Restos de embarcações submersas, principal foco de estudo desta área.",
            "NAVIO": "O objeto principal de estudo na Arqueologia Marítima.",
            "ANCORA": "Objeto de ferro ou chumbo usado para fixar embarcações ao fundo do mar.",
            "MARITIMA": "Relativo ao mar, especialização em ambientes aquáticos.",
            "INTERFACE": "A zona de transição entre a água e o sedimento onde os vestígios se encontram."
        },
        "Zooarqueologia": {
            "OSTEOLOGIA": "O estudo dos ossos.",
            "FAUNA": "Os restos de animais encontrados em um sítio.",
            "ESQUELETO": "A estrutura óssea completa de um ser humano ou animal.",
            "DIETA": "O que as pessoas comiam, inferido pelo estudo dos restos de alimentos e animais.",
            "DOMESTICACAO": "Processo chave para entender a transição do Paleolítico para o Neolítico."
        },
        "Geoarqueologia": {
            "SEDIΜENTO": "Material depositado pelo vento ou água, onde se encontram vestígios.",
            "SOLO": "A matriz onde os artefatos são encontrados.",
            "GEOLOGIA": "Ciência que estuda a Terra, crucial para esta subárea.",
            "PEDOLOGIA": "Estudo da formação do solo.",
            "MICROMORFOLOGIA": "Análise da microestrutura das camadas do solo, muitas vezes sob microscópio."
        }
    }
}

# --- 2. Funções de Lógica e Estado ---

def iniciar_sessao():
    """Inicializa as variáveis de estado do Streamlit."""
    if 'palavra_secreta' not in st.session_state:
        st.session_state.palavra_secreta = None
        st.session_state.dica_atual = ""
        st.session_state.palavra_mostrada = []
        st.session_state.letras_tentadas = set()
        st.session_state.tentativas_restantes = 6
        st.session_state.jogo_terminado = False

def escolher_palavra_e_dica(dificuldade, subarea=None):
    """Seleciona a palavra e dica."""
    if dificuldade == "Específico":
        palavras_e_dicas = DICIONARIO_ARQUEOLOGIA["Específico"].get(subarea, {})
    else:
        palavras_e_dicas = DICIONARIO_ARQUEOLOGIA.get(dificuldade, {})

    if palavras_e_dicas:
        palavra_secreta = random.choice(list(palavras_e_dicas.keys()))
        dica = palavras_e_dicas[palavra_secreta]
        return palavra_secreta, dica
    return None, None

def iniciar_novo_jogo(dificuldade, subarea=None):
    """Reseta o jogo e seleciona uma nova palavra."""
    palavra, dica = escolher_palavra_e_dica(dificuldade, subarea)

    if palavra:
        st.session_state.palavra_secreta = palavra
        st.session_state.dica_atual = dica
        st.session_state.palavra_mostrada = ["\_"] * len(palavra)
        st.session_state.letras_tentadas = set()
        st.session_state.tentativas_restantes = 6
        st.session_state.jogo_terminado = False
        st.success(f"Nova Escavação Iniciada! Categoria: {dificuldade}" + (f" ({subarea})" if subarea else ""))
    else:
        st.error("Erro ao selecionar a palavra.")

def processar_palpite():
    """Lógica de verificação de palpite (letra ou palavra)."""
    if st.session_state.jogo_terminado or not st.session_state.palavra_secreta:
        return

    palpite = st.session_state.palpite_input.upper().strip()
    st.session_state.palpite_input = "" # Limpa o campo após o processamento

    if not palpite:
        return

    # Adivinhar Letra
    if len(palpite) == 1 and palpite.isalpha():
        if palpite in st.session_state.letras_tentadas:
            st.warning(f"Você já tentou a letra '{palpite}'.")
            return
        
        st.session_state.letras_tentadas.add(palpite)
        acertou = False
        
        palavra = st.session_state.palavra_secreta
        for i, letra_secreta in enumerate(palavra):
            if letra_secreta == palpite:
                st.session_state.palavra_mostrada[i] = palpite
                acertou = True

        if not acertou:
            st.session_state.tentativas_restantes -= 1
            st.error(f"A letra '{palpite}' NÃO está na palavra.")
        else:
            st.success(f"Acerto! A letra '{palpite}' foi encontrada.")
            
    # Adivinhar Palavra Completa
    elif len(palpite) > 1 and palpite.isalpha():
        if palpite == st.session_state.palavra_secreta:
            st.session_state.palavra_mostrada = list(st.session_state.palavra_secreta)
            st.session_state.jogo_terminado = True
        else:
            st.session_state.tentativas_restantes -= 1
            st.error("Palavra incorreta!")
    else:
        st.warning("Entrada inválida. Digite uma única letra ou a palavra completa.")

    # Verificar Fim do Jogo
    if st.session_state.tentativas_restantes <= 0 or "\_" not in st.session_state.palavra_mostrada:
        st.session_state.jogo_terminado = True
        st.rerun() # Força a atualização para mostrar o resultado final

# --- 3. Interface Streamlit Principal (Função Main) ---

def main():
    iniciar_sessao()
    
    st.title("🔎 Jogo de Adivinhação Arqueológica")
    st.markdown("Desvende os mistérios da Arqueologia acertando a palavra secreta!")

    # --- Controles de Início de Jogo (Sidebar) ---
    st.sidebar.header("Novo Jogo (Escavação)")

    dificuldades = list(DICIONARIO_ARQUEOLOGIA.keys())
    dificuldade_escolhida = st.sidebar.selectbox("1. Escolha a Dificuldade:", dificuldades)

    subarea_escolhida = None
    if dificuldade_escolhida == "Específico":
        subareas = list(DICIONARIO_ARQUEOLOGIA["Específico"].keys())
        subarea_escolhida = st.sidebar.selectbox("2. Escolha a Subárea:", subareas)

    if st.sidebar.button("Iniciar Novo Jogo"):
        iniciar_novo_jogo(dificuldade_escolhida, subarea_escolhida)
        st.rerun()

    # --- 4. Exibição do Jogo ---
    
    if st.session_state.palavra_secreta:
        # Exibir o estado atual
        palavra_formatada = " ".join(st.session_state.palavra_mostrada)
        st.markdown(f"## 🪨 Palavra: `{palavra_formatada}`")
        
        st.info(f"**DICA:** {st.session_state.dica_atual}")
        
        st.markdown(f"**Tentativas Restantes:** {st.session_state.tentativas_restantes} / 6")
        st.markdown(f"**Letras Tentadas:** {', '.join(sorted(list(st.session_state.letras_tentadas)))}")

        if not st.session_state.jogo_terminado:
            # Campo de Palpite
            st.text_input("Sua Escavação (letra ou palavra):", 
                           key="palpite_input", 
                           on_change=processar_palpite)
            st.caption("Pressione Enter após digitar seu palpite.")

        else:
            # Mensagem de Fim de Jogo
            if "\_" not in st.session_state.palavra_mostrada:
                st.balloons()
                st.success(f"🎉 VITÓRIA! Você desvendou o sítio arqueológico! A palavra era: **{st.session_state.palavra_secreta}**")
            else:
                st.error(f"😭 DERROTA! O vestígio foi perdido. A palavra era: **{st.session_state.palavra_secreta}**")
                
    else:
        st.info("Use o painel 'Novo Jogo' na barra lateral para começar a explorar!")

if __name__ == "__main__":
    main()
