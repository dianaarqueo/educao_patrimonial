import streamlit as st
import random

# --- 1. ESTRUTURA DE DADOS COMPLETA ---
DADOS_ARQUEOLOGIA = {
    "Fácil": {
        "VESTIGIO": "Qualquer marca material de atividade humana deixada no passado.",
        "ESCAVACAO": "O processo de remoção sistemática de solo e registro de achados.",
        "CULTURA": "O conjunto de hábitos, crenças e modos de vida de um grupo.",
        "RUINA": "O que resta de uma estrutura ou edificação antiga destruída.",
        "HISTORIA": "O estudo do passado humano após o surgimento da escrita.",
        "CERAMICA": "Artefato comum feito de argila cozida, como potes e vasos.",
        "CAMADA": "Estrato de solo, areia ou depósitos, essencial para a datação.",
        "SITIO": "O local onde são encontrados e estudados os materiais arqueológicos.",
        "MUSEU": "Local de preservação e exibição de artefatos.",
        "PRE HISTORIA": "O período da humanidade anterior à invenção da escrita.",
        "ARTEFATO": "Qualquer objeto feito ou modificado por humanos."
    },
    "Médio": {
        "ESTRATIGRAFIA": "O estudo das camadas de solo e sua cronologia de deposição.",
        "PINTURA RUPESTRE": "Arte feita em paredes de cavernas ou abrigos rochosos (geralmente vermelho).",
        "DATAÇAO": "Técnica usada para determinar a idade de um achado ou sítio.",
        "TIPOLOGIA": "Classificação de artefatos por forma, estilo e função.",
        "PROSPECCAO": "Busca e reconhecimento preliminar de sítios na paisagem.",
        "TOPOGRAFIA": "A ciência de medição e representação detalhada do relevo, contornos e acidentes naturais e artificiais de uma porção de terra.",
        "SEPULTAMENTO": "O ato de enterrar um indivíduo com ou sem oferendas.",
        "RADIOCARBONO": "Método de datação que mede o decaimento do isótopo Carbono-14.",
        "LITICO": "Ferramentas de pedra.",
        "INDUSTRIA": "Conjunto de artefatos de pedra que compartilham a mesma técnica de fabricação."
    },
    "Difícil": {
        "TRADIÇAO": "Um padrão cultural que se repete por longo tempo e espaço.",
        "PERCUTOR": "Ferramenta usada para golpear outra (por exemplo, para lascar pedra).",
        "TAFONOMIA": "Estudo de como os organismos e objetos se tornam fósseis ou vestígios.",
        "ETNOARQUEOLOGIA": "Estudo de sociedades vivas para entender o registro arqueológico.",
        "ANTROPOFAGIA": "Prática de consumir carne humana, um tema de estudo em remanescentes humanos.",
        "PALEOPATOLOGIA": "Estudo de doenças e lesões em remanescentes humanos antigos.",
        "ACERVO": "O conjunto total de itens e dados coletados em uma pesquisa e guardados em um museu ou reserva técnica.",
        "CONTEXTO": "A localização precisa e a relação de um artefato com seu entorno.",
        "PALEOAMBIENTE": "O ambiente e as condições climáticas de uma época passada."
    },
    "Específicos": {
        "Clássica": {
            "EGIPTOLOGIA": "O estudo específico do Antigo Egito.",
            "PAPIRO": "Material de escrita feito de planta, comum no Nilo.",
            "HELENISTICO": "Período da história grega após as conquistas de Alexandre.",
            "TUMULO": "Estrutura de enterro, como uma mastaba ou hipogeu.",
            "HERCULANO": "Cidade romana, vizinha de Pompeia, destruída pelo Vesúvio."
        },
        "Subaquática": {
            "NAUFRAGIO": "Restos de uma embarcação que afundou.",
            "NAVIO": "Usado para navegar, principal foco desta subárea.",
            "ANCORA": "Objeto pesado usado para prender o navio ao fundo.",
            "PIROGA": "Tipo de embarcação indígena.",
            "INTERFACE": "Faixa de transição entre a água e o sedimento."
        },
        "Zooarqueologia": {
            "OSTEOLOGIA": "O estudo dos ossos (chave para identificar restos de fauna).",
            "FAUNA": "O conjunto de espécies animais de um sítio.",
            "ESQUELETO": "Estrutura óssea que ajuda a identificar o animal.",
            "DIETA": "O que os grupos consumiam, inferido pelos restos de animais e vegetais.",
            "DOMESTICACAO": "Processo de tornar espécies selvagens dependentes do ser humano."
        },
        "Geoarqueologia": {
            "SEDIΜENTO": "Material sólido que se deposita em camadas (areia, argila, etc.).",
            "SOLO": "A camada superficial da terra estudada nas escavações.",
            "GEOLOGIA": "A ciência que estuda a formação e composição da Terra.",
            "PEDOLOGIA": "O estudo da formação, natureza e classificação dos solos.",
            "MICROMORFOLOGIA": "Análise de amostras de solo em escala microscópica."
        }
    }
}

# --- 2. FUNÇÕES DE LÓGICA DO JOGO ---

def inicializar_estado_do_jogo():
    """Define o estado inicial ou reinicia o jogo."""
    if 'nivel_atual' not in st.session_state:
        st.session_state.nivel_atual = None
        st.session_state.pontuacao = 0
        st.session_state.indice_palavra = 0
        st.session_state.palavras_embaralhadas = []
        st.session_state.palavras_corretas = 0
        st.session_state.total_palavras = 0
        st.session_state.mensagem_feedback = ""

def limpar_resposta(resposta):
    """Normaliza a resposta do usuário para comparação."""
    # Remove espaços, converte para maiúsculas e remove acentos/caracteres especiais (simples)
    return resposta.strip().upper().replace(" ", "").replace("Ç", "C").replace("ÃO", "AO").replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Â", "A").replace("Ú", "U")


def carregar_nivel(nome_nivel):
    """Carrega as palavras para um nível e inicia o estado."""
    st.session_state.nivel_atual = nome_nivel
    st.session_state.palavras_corretas = 0
    st.session_state.indice_palavra = 0
    st.session_state.mensagem_feedback = ""
    
    # Lógica para lidar com subáreas
    if nome_nivel in DADOS_ARQUEOLOGIA:
        palavras_dicas = DADOS_ARQUEOLOGIA[nome_nivel]
    else: # Se for uma subárea
        subarea_data = DADOS_ARQUEOLOGIA["Específicos"]
        if nome_nivel in subarea_data:
            palavras_dicas = subarea_data[nome_nivel]
        else:
            st.error("Nível não encontrado!")
            return

    st.session_state.total_palavras = len(palavras_dicas)
    
    # Cria uma lista de (palavra, dica) e embaralha
    palavras_lista = list(palavras_dicas.items())
    random.shuffle(palavras_lista)
    st.session_state.palavras_embaralhadas = palavras_lista
    st.session_state.pontuacao_nivel = 0
    st.session_state.fase_jogo = "jogando"

def verificar_resposta(resposta_usuario):
    """Verifica a resposta e atualiza o estado do jogo."""
    if st.session_state.fase_jogo != "jogando":
        return

    # Pega a palavra e dica atual
    palavra_correta, dica = st.session_state.palavras_embaralhadas[st.session_state.indice_palavra]
    
    if limpar_resposta(resposta_usuario) == limpar_resposta(palavra_correta):
        st.session_state.mensagem_feedback = f"✅ **Correto!** A palavra é: *{palavra_correta}*."
        st.session_state.palavras_corretas += 1
        st.session_state.pontuacao += 1 # Pontuação total
        st.session_state.pontuacao_nivel += 1 # Pontuação do nível
    else:
        st.session_state.mensagem_feedback = f"❌ **Errado.** A palavra correta era: *{palavra_correta}*."

    # Avança para a próxima palavra
    st.session_state.indice_palavra += 1
    
    if st.session_state.indice_palavra >= st.session_state.total_palavras:
        st.session_state.fase_jogo = "finalizado"

# --- 3. CONFIGURAÇÃO DE DESIGN (CSS TEMÁTICO REFINADO) ---

def aplicar_tema(nivel):
    """Aplica o CSS com alto contraste, cores temáticas e decoração para cada subárea."""
    
    FUNDO_PADRAO = "#F5F5DC"  # Bege claro (papel de campo)
    TEXTO_PADRAO = "#4B3832" # Marrom escuro
    
    # Mapeamento de estilos temáticos
    temas = {
        # Clássica: Papiro e Hieróglifos.
        "Clássica": {
            'estilo_fundo': 'background-color: #F8F4E3;', 
            'cor_texto': '#8B4513', # Marrom Sépia
            'sombra_texto': 'none',
            'emoji': "🏺🏛️"
        },
        # Subaquática: Oceano Profundo. Alto contraste com sombra branca.
        "Subaquática": {
            'estilo_fundo': 'background: linear-gradient(to bottom, #001f3f, #003366);', 
            'cor_texto': '#ADD8E6', # Azul Claro
            'sombra_texto': '1px 1px 2px #000000', # Sombra escura para contraste máximo
            'emoji': "🌊⚓"
        },
        # Zooarqueologia: Ossos e Natureza.
        "Zooarqueologia": {
            'estilo_fundo': 'background-color: #F0F0F0;', 
            'cor_texto': '#36454F', # Cinza Ardósia
            'sombra_texto': 'none',
            'emoji': "🦴🌿"
        },
        # Geoarqueologia: Estratos de Solo e Rochas.
        "Geoarqueologia": {
            'estilo_fundo': 'background: linear-gradient(to bottom, #A0522D, #696969);', 
            'cor_texto': '#FFDAB9', # Pêssego Claro
            'sombra_texto': '1px 1px 2px #000000', # Sombra escura
            'emoji': "⛰️🪨"
        }
    }

    # Seleciona o tema ou usa o padrão
    tema_config = temas.get(nivel, {
        'estilo_fundo': f'background-color: {FUNDO_PADRAO};',
        'cor_texto': TEXTO_PADRAO,
        'sombra_texto': 'none',
        'emoji': "🔎"
    })
    
    estilo_aplicar = tema_config['estilo_fundo'] + f'color: {tema_config["cor_texto"]};'
    cor_primaria = tema_config['cor_texto']
    sombra_texto = tema_config['sombra_texto']
    
    # 2. INJEÇÃO DE CSS
    
    st.markdown(
        f'<style>.stApp {{ {estilo_aplicar} }}</style>', 
        unsafe_allow_html=True
    )
    
    # Adiciona decoração ao título (se estiver no jogo)
    if st.session_state.nivel_atual and st.session_state.fase_jogo != "inicio":
        emoji = tema_config['emoji']
        st.sidebar.markdown(f"### {emoji} **Nível: {st.session_state.nivel_atual}**")
        
    # 3. CSS PARA GARANTIR LEGIBILIDADE DOS COMPONENTES
    st.markdown(f"""
    <style>
    /* 1. Cores de Texto e Títulos (Aplicado à Div Principal) */
    .stApp, .stButton, .stProgress, .stRadio, .stForm, .stSidebar {{
        color: {cor_primaria} !important;
        text-shadow: {sombra_texto};
    }}
    
    /* 2. Títulos */
    h1, h2, h3 {{
        color: {cor_primaria} !important; 
        border-bottom: 2px solid #D2B48C;
        padding-bottom: 5px;
        text-shadow: {sombra_texto};
    }}
    
    /* 3. Área de Dica (Mantida clara para alto contraste) */
    .stMarkdown p {{
        background-color: rgba(255, 255, 240, 0.95) !important; /* Quase branco sólido */
        color: #4B3832 !important; /* Texto escuro dentro da caixa de dica */
        border: 1px solid {cor_primaria};
        text-shadow: none;
    }}
    
    /* 4. Botões (mantidos verdes para destaque) */
    .stButton>button {{
        background-color: #6B8E23; 
        color: white;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.4);
        text-shadow: none;
    }}
    
    /* 5. Radio Buttons (Garante que o texto da opção seja legível) */
    .stRadio div[data-baseweb="radio"] label span {{
        color: {cor_primaria} !important;
        text-shadow: {sombra_texto};
    }}
    
    </style>
    """, unsafe_allow_html=True)


def mostrar_tela_inicial():
    """Mostra a tela de seleção de nível."""
    st.title("🗺️ Mistério Arqueológico")
    st.header("Selecione o seu Nível de Descoberta")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("Nível 1: FÁCIL (Fundamentos)", on_click=carregar_nivel, args=("Fácil",), use_container_width=True)
    with col2:
        st.button("Nível 2: MÉDIO (Técnicas de Campo)", on_click=carregar_nivel, args=("Médio",), use_container_width=True)
    with col3:
        st.button("Nível 3: DIFÍCIL (Teoria Avançada)", on_click=carregar_nivel, args=("Difícil",), use_container_width=True)

    st.subheader("Nível 4: ESPECÍFICOS (Subáreas)")
    col_sub1, col_sub2, col_sub3, col_sub4 = st.columns(4)
    
    with col_sub1:
        st.button("Clássica", on_click=carregar_nivel, args=("Clássica",), help="Egiptologia, Roma, Grécia.", use_container_width=True)
    with col_sub2:
        st.button("Subaquática", on_click=carregar_nivel, args=("Subaquática",), help="Naufrágios, Marítima.", use_container_width=True)
    with col_sub3:
        st.button("Zooarqueologia", on_click=carregar_nivel, args=("Zooarqueologia",), help="Ossos, Dieta, Fauna.", use_container_width=True)
    with col_sub4:
        st.button("Geoarqueologia", on_click=carregar_nivel, args=("Geoarqueologia",), help="Solos, Sedimentos, Geologia.", use_container_width=True)


def mostrar_tela_jogo():
    """Mostra a interface do quiz interativo."""
    
    if st.session_state.fase_jogo == "finalizado":
        st.success(f"🥳 Nível '{st.session_state.nivel_atual}' COMPLETO!")
        st.balloons()
        st.write(f"Você acertou **{st.session_state.palavras_corretas}** de **{st.session_state.total_palavras}** palavras neste nível.")
        st.button("Voltar para Seleção de Nível", on_click=inicializar_estado_do_jogo)
        return

    # Cabeçalho do Jogo
    st.header(f"🗃️ Nível: {st.session_state.nivel_atual}")
    st.progress(st.session_state.indice_palavra / st.session_state.total_palavras)
    st.markdown(f"**Palavra {st.session_state.indice_palavra + 1}** de {st.session_state.total_palavras} | Acertos no Nível: **{st.session_state.palavras_corretas}**")
    
    # Palavra e Dica Atual
    palavra_atual, dica_atual = st.session_state.palavras_embaralhadas[st.session_state.indice_palavra]
    
    st.subheader("🔍 Pista do Sítio:")
    st.markdown(f"<p>{dica_atual}</p>", unsafe_allow_html=True)
    
    # Campo de Resposta e Verificação
    # O campo de texto usa o mesmo 'key' e é limpo automaticamente pelo Streamlit após o botão ser clicado
    
    with st.form(key=f"form_palavra_{st.session_state.indice_palavra}"):
        resposta = st.text_input("Sua Descoberta (Palavra):", key="input_resposta")
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            # Botão de submissão do formulário. Ele chama a verificação e recarrega a página.
            submit_button = st.form_submit_button(label='Escavar (Verificar)')
            
        if submit_button:
            if resposta:
                verificar_resposta(resposta)
            else:
                st.warning("Por favor, digite uma palavra antes de escavar!")

    # Feedback da última tentativa
    if st.session_state.mensagem_feedback:
        if "Correto" in st.session_state.mensagem_feedback:
            st.success(st.session_state.mensagem_feedback)
        else:
            st.error(st.session_state.mensagem_feedback)
            
    # Botão para sair do nível
    st.button("Próxima pergunta", on_click=inicializar_estado_do_jogo)


# --- 4. FUNÇÃO PRINCIPAL DE EXECUÇÃO ---

def main():
    inicializar_estado_do_jogo()

    if st.session_state.nivel_atual is None:
        mostrar_tela_inicial()
        st.sidebar.markdown(f"**Pontuação Total Acumulada:** {st.session_state.pontuacao}")
    else:
        mostrar_tela_jogo()
        st.sidebar.markdown(f"**Pontuação Total Acumulada:** {st.session_state.pontuacao}")
        st.sidebar.markdown(f"**Progresso no Nível {st.session_state.nivel_atual}:** {st.session_state.palavras_corretas}/{st.session_state.total_palavras}")

if __name__ == "__main__":
    main()
