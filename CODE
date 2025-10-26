# app.py - CÓDIGO PRINCIPAL PARA STREAMLIT

import streamlit as st
import random

# --- 1. Dicionário de Palavras ---
DICIONARIO_ARQUEOLOGIA = {
    # ... (Copie e cole seu dicionário completo aqui) ...
    "Fácil": [
        "VESTIGIO", "ESCAVACAO", "CULTURA", "RUINA", "HISTORIA",
        "CERAMICA", "CAMADA", "SITIO", "MUSEU", "PRE HISTORIA", "ARTEFATO"
    ],
    "Médio": [
        "ESTRATIGRAFIA", "PINTURA RUPESTRE", "DATAÇAO", "TIPOLOGIA",
        "PROSPECCAO", "JAZIDA", "SEPULTAMENTO", "RADIOCARBONO",
        "LITICO", "INDUSTRIA"
    ],
    "Difícil": [
        "TRADIÇAO", "PERCUTOR", "TAFONOMIA", "ETNOARQUEOLOGIA",
        "ANTROPOFAGIA", "PALEOPATOLOGIA", "ACERVO", "DATACAO",
        "CONTEXTO", "PALEOAMBIENTE"
    ],
    "Específico": {
        "Clássica": [
            "EGIPTOLOGIA", "PAPIRO", "HELENISTICO", "TUMULO", "HERCULANO"
        ],
        "Subaquática": [
            "NAUFRAGIO", "NAVIO", "ANCORA", "MARITIMA", "INTERFACE", "SONAR"
        ],
        "Zooarqueologia": [
            "OSTEOLOGIA", "FAUNA", "ESQUELETO", "DIETA", "DOMESTICACAO"
        ],
        "Geoarqueologia": [
            "SEDIΜENTO", "SOLO", "GEOLOGIA", "PEDOLOGIA", "MICROMORFOLOGIA"
        ]
    }
}

# --- 2. Funções de Lógica e Estado ---

# Inicializa o estado da sessão (como variáveis globais no Streamlit)
if 'palavra_secreta' not in st.session_state:
    st.session_state.palavra_secreta = None
    st.session_state.palavra_mostrada = []
    st.session_state.letras_tentadas = set()
    st.session_state.tentativas_restantes = 6
    st.session_state.jogo_terminado = False

def iniciar_novo_jogo(dificuldade, subarea=None):
    """Escolhe a palavra e reseta o estado do jogo."""
    if dificuldade == "Específico":
        palavras = DICIONARIO_ARQUEOLOGIA["Específico"].get(subarea)
        if not palavras:
            st.error("Subárea inválida. Selecione novamente.")
            return

        palavra = random.choice(palavras)
    else:
        palavra = random.choice(DICIONARIO_ARQUEOLOGIA.get(dificuldade, []))

    if not palavra:
        st.error("Dificuldade inválida. Selecione novamente.")
        return

    st.session_state.palavra_secreta = palavra
    st.session_state.palavra_mostrada = ["\_"] * len(palavra)
    st.session_state.letras_tentadas = set()
    st.session_state.tentativas_restantes = 6
    st.session_state.jogo_terminado = False

def processar_palpite(palpite):
    """Processa a letra/palavra e atualiza o estado."""
    palpite = palpite.upper().strip()

    if not palpite or st.session_state.jogo_terminado:
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
            st.error(f"A letra '{palpite}' NÃO está na palavra. Restam {st.session_state.tentativas_restantes} tentativas.")
            
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
        
# --- 3. Interface Streamlit (Função Main) ---

st.title("🔎 Jogo de Adivinhação Arqueológica")
st.markdown("Desvende os mistérios da Arqueologia acertando a palavra secreta!")

# --- Controles de Início de Jogo (Sidebar) ---
st.sidebar.header("Novo Jogo")

dificuldades = list(DICIONARIO_ARQUEOLOGIA.keys())
dificuldade_escolhida = st.sidebar.selectbox("1. Escolha a Dificuldade:", dificuldades)

subarea_escolhida = None
if dificuldade_escolhida == "Específico":
    subareas = list(DICIONARIO_ARQUEOLOGIA["Específico"].keys())
    subarea_escolhida = st.sidebar.selectbox("2. Escolha a Subárea:", subareas)

if st.sidebar.button("Iniciar Escavação (Novo Jogo)"):
    iniciar_novo_jogo(dificuldade_escolhida, subarea_escolhida)

# --- 4. Exibição do Jogo ---

if st.session_state.palavra_secreta:
    # Exibir o estado atual da palavra
    palavra_formatada = " ".join(st.session_state.palavra_mostrada)
    st.markdown(f"## 🪨 Palavra: `{palavra_formatada}`")
    
    # Exibir informações
    st.markdown(f"**Tentativas Restantes:** {st.session_state.tentativas_restantes} / 6")
    st.markdown(f"**Letras Tentadas:** {', '.join(sorted(list(st.session_state.letras_tentadas)))}")

    if not st.session_state.jogo_terminado:
        # Campo de Palpite
        palpite_input = st.text_input("Sua Escavação (letra ou palavra):", key="palpite_input")
        
        if st.button("Tentar Palpite"):
            processar_palpite(palpite_input)
            st.session_state.palpite_input = "" # Limpa o campo após o clique

        # Reexibir a palavra após o palpite (para atualizar a UI)
        st.experimental_rerun()

    else:
        # Mensagem de Fim de Jogo
        if "\_" not in st.session_state.palavra_mostrada:
            st.balloons()
            st.success(f"🎉 VITÓRIA! Você desvendou o sítio arqueológico! A palavra era: **{st.session_state.palavra_secreta}**")
        else:
            st.error(f"😭 DERROTA! O vestígio foi perdido. A palavra era: **{st.session_state.palavra_secreta}**")
            
else:
    st.info("Use o painel 'Novo Jogo' na barra lateral para começar a explorar!")
