import streamlit as st
import random

# --- 1. ESTRUTURA DE DADOS COM DICAS SIMPLIFICADAS ---

DADOS_ARQUEOLOGIA = {
    "Fácil": {
        "VESTIGIO": "Qualquer marca ou resto de objeto antigo deixado por humanos.",
        "ESCAVAÇAO": "O trabalho de cavar o solo com cuidado para encontrar material arqueológico.",
        "CULTURA": "O jeito de viver, as crenças e os costumes de um povo do passado.",
        "RUINA": "O que sobrou de um prédio ou construção muito antiga, que caiu.",
        "HISTORIA": "O estudo da humanidade, começando após a invenção da escrita.",
        "CERAMICA": "Objetos feitos de argila (barro) queimada, como potes e vasos.",
        "CAMADA": "Cada 'fatía' de terra que se depositou com o tempo, indicando idades.",
        "SITIO": "O local exato onde os arqueólogos encontram e estudam vestígios.",
        "MUSEU": "O lugar onde os artefatos encontrados são guardados e expostos ao público.",
        "PRE HISTORIA": "O tempo da humanidade antes de inventarem a escrita.",
        "ARTEFATO": "Qualquer objeto feito ou modificado pelas mãos humanas."
    },
    "Médio": {
        "ESTRATIGRAFIA": "O estudo das camadas de solo (estratos) para entender a ordem dos eventos.",
        "PINTURA RUPESTRE": "Figuras feitas por humanos em paredes de cavernas ou rochas.",
        "DATAÇAO": "O método usado para descobrir a idade exata de um objeto ou de uma camada.",
        "TIPOLOGIA": "O sistema de classificar os artefatos agrupando-os por forma e função.",
        "PROSPECÇAO": "A busca inicial e reconhecimento de sítios arqueológicos na paisagem.",
        "TOPOGRAFIA": "A ciência de medição e representação detalhada do relevo, contornos e acidentes naturais e artificiais de uma porção de terra.",
        "SEPULTAMENTO": "O ato de enterrar um corpo ou restos mortais de forma intencional.",
        "RADIOCARBONO": "O método científico que usa o Carbono-14 para datar materiais orgânicos.",
        "LITICO": "Tudo o que é feito ou relacionado à pedra, como ferramentas de corte.",
        "INDUSTRIA": "O conjunto de ferramentas de pedra feitas com a mesma técnica."
    },
    "Difícil": {
        "TRADIÇAO": "Um conjunto de traços culturais que dura muito tempo e se espalha por uma grande área.",
        "PERCUTOR": "Uma pedra ou ferramenta usada para bater em outra e lascá-la (fazer uma ferramenta nova).",
        "TAFONOMIA": "O estudo de como os restos (ossos, plantas) se transformam e se enterram até virarem vestígios.",
        "ETNOARQUEOLOGIA": "O estudo de povos atuais (vivos) para ajudar a entender o comportamento de povos antigos.",
        "ANTROPOFAGIA": "O costume de consumir carne humana, estudado através de marcas em ossos antigos.",
        "PALEOPATOLOGIA": "O estudo de doenças, feridas e lesões encontradas em esqueletos e múmias antigas.",
        "ACERVO": "Todo o conjunto de objetos, dados e documentos guardados em um museu ou instituição.",
        "CONTEXTO": "A posição exata, a relação e o significado de um artefato dentro de seu local de achado.",
        "PALEOAMBIENTE": "O clima, a vegetação e as condições do ambiente de uma época muito antiga."
    },
    "Específicos": {
        "Clássica": {
            "EGIPTOLOGIA": "O estudo especializado na civilização do Antigo Egito.",
            "PAPIRO": "Material feito de uma planta, muito usado como papel no Egito e Roma.",
            "HELENISTICO": "O período da cultura grega que se espalhou após as conquistas de Alexandre, o Grande.",
            "TUMULO": "Uma estrutura de pedra ou terra feita para o enterro de uma pessoa ou grupo.",
            "HERCULANO": "Cidade romana, perto de Pompeia, que foi soterrada pela erupção do Vesúvio."
        },
        "Subaquática": {
            "NAUFRAGIO": "Os restos de uma embarcação que afundou no mar ou em um rio.",
            "NAVIO": "A embarcação principal de interesse nesta subárea da arqueologia.",
            "ANCORA": "Objeto pesado que prende o barco ao fundo, muitas vezes o primeiro achado de um naufrágio.",
            "PIROGA": "Tipo de embarcação indígena.",
            "INTERFACE": "A faixa de transição onde a água encontra o solo."
        },
        "Zooarqueologia": {
            "OSTEOLOGIA": "O estudo dos ossos; vital para identificar os restos de animais.",
            "FAUNA": "O conjunto de espécies de animais que viviam em determinado sítio.",
            "ESQUELETO": "A estrutura óssea do animal, usada para saber a espécie.",
            "DIETA": "O que os humanos comiam, baseado nos restos de animais encontrados.",
            "DOMESTICACAO": "O processo de transformar animais selvagens em dependentes dos humanos."
        },
        "Geoarqueologia": {
            "SEDIΜENTO": "O material (areia, argila) que se acumula em camadas no chão.",
            "SOLO": "A camada superficial da Terra que é escavada e estudada.",
            "GEOLOGIA": "A ciência que estuda a formação e a composição das rochas e da Terra.",
            "PEDOLOGIA": "O estudo específico de como o solo se forma, suas características e classificação.",
            "MICROMORFOLOGIA": "Análise de pequenas amostras de solo, observadas em escala microscópica."
        }
    }
}

# --- 2. FUNÇÕES DE LÓGICA E ESTADO DO JOGO ---

def inicializar_estado_do_jogo():
    """Define o estado inicial ou reinicia o jogo."""
    st.session_state.nivel_atual = None
    st.session_state.indice_palavra = 0
    st.session_state.palavras_embaralhadas = []
    st.session_state.palavras_corretas = 0
    st.session_state.total_palavras = 0
    st.session_state.mensagem_feedback = ""
    st.session_state.fase_jogo = "inicio"
    
    # Manter a pontuação total (só zera quando o app é reiniciado)
    if 'pontuacao_total' not in st.session_state:
        st.session_state.pontuacao_total = 0
        
    st.session_state.resposta_verificada = False
    st.session_state.radio_selection = None

def get_palavras_do_contexto(nome_nivel):
    """
    Retorna a lista de todas as palavras (chaves) de um nível ou subárea.
    """
    if nome_nivel in DADOS_ARQUEOLOGIA:
        return list(DADOS_ARQUEOLOGIA[nome_nivel].keys())
    elif nome_nivel in DADOS_ARQUEOLOGIA["Específicos"]:
        return list(DADOS_ARQUEOLOGIA["Específicos"][nome_nivel].keys())
    return []

def extrair_todas_as_palavras(dados):
    """Extrai todas as palavras-chave de todos os níveis."""
    todas_palavras = []
    for nivel, conteudo in dados.items():
        if nivel == "Específicos":
            for subarea in conteudo.keys():
                todas_palavras.extend(get_palavras_do_contexto(subarea))
        else:
            todas_palavras.extend(get_palavras_do_contexto(nivel))
    return todas_palavras

TODAS_AS_PALAVRAS = extrair_todas_as_palavras(DADOS_ARQUEOLOGIA)


def gerar_alternativas(palavra_correta, nome_nivel):
    """
    Gera três alternativas contextuais (uma correta e duas do mesmo contexto), 
    priorizando o contexto restrito do nível/subárea.
    """
    palavras_contexto = get_palavras_do_contexto(nome_nivel)
    
    # 1. Tenta tirar palavras do contexto imediato (mesmo nível/subárea)
    distratores_potenciais = [p for p in palavras_contexto if p != palavra_correta]
    alternativas_falsas = []
    
    if len(distratores_potenciais) >= 2:
        # Se houver palavras suficientes no contexto, usa 2 delas
        alternativas_falsas = random.sample(distratores_potenciais, 2)
    else:
        # Se houver 0 ou 1, usa o que tem e busca o restante em palavras globais relevantes
        alternativas_falsas = distratores_potenciais
        num_faltante = 2 - len(alternativas_falsas)
        
        if num_faltante > 0:
            outras_palavras_globais = [
                p for p in TODAS_AS_PALAVRAS 
                if p != palavra_correta and p not in alternativas_falsas
            ]
            
            if len(outras_palavras_globais) >= num_faltante:
                alternativas_falsas.extend(random.sample(outras_palavras_globais, num_faltante))
            else:
                # Fallback extremo para garantir 3 opções (pode ter repetição, mas mantém a estabilidade)
                alternativas_falsas.extend(random.sample(TODAS_AS_PALAVRAS, num_faltante))

    # 3. Monta a lista final e embaralha a ordem
    alternativas = [palavra_correta] + alternativas_falsas
    random.shuffle(alternativas)
    return alternativas


def carregar_nivel(nome_nivel):
    """Carrega as palavras para um nível e inicia o estado."""
    inicializar_estado_do_jogo() # Reinicia antes de carregar um novo nível
    
    st.session_state.nivel_atual = nome_nivel
    st.session_state.pontuacao_nivel = 0
    
    if nome_nivel in DADOS_ARQUEOLOGIA:
        palavras_dicas = DADOS_ARQUEOLOGIA[nome_nivel]
    elif nome_nivel in DADOS_ARQUEOLOGIA["Específicos"]:
        palavras_dicas = DADOS_ARQUEOLOGIA["Específicos"][nome_nivel]
    else:
        st.error("Nível não encontrado!")
        return

    st.session_state.total_palavras = len(palavras_dicas)
    palavras_lista = list(palavras_dicas.items())
    random.shuffle(palavras_lista)
    st.session_state.palavras_embaralhadas = palavras_lista
    st.session_state.fase_jogo = "jogando"

def avancar_pergunta():
    """Limpa o feedback, avança o índice e verifica se o nível terminou."""
    st.session_state.resposta_verificada = False
    st.session_state.mensagem_feedback = ""
    st.session_state.radio_selection = None # Limpa a seleção do rádio
    
    # Avança para a próxima palavra
    st.session_state.indice_palavra += 1
    
    # Verifica se o nível terminou após o avanço
    if st.session_state.indice_palavra >= st.session_state.total_palavras:
        st.session_state.fase_jogo = "finalizado"

def submeter_resposta(palavra_correta):
    """
    Função de callback para o botão 'Verificar'. 
    Usa o valor da sessão de estado do rádio e chama a verificação.
    """
    resposta_selecionada = st.session_state.get("radio_selection")
    
    if not resposta_selecionada:
        st.session_state.mensagem_feedback = "⚠️ Por favor, selecione uma alternativa antes de verificar!"
        st.session_state.resposta_verificada = False # Mantém o botão verificar visível
        return

    # Se a resposta foi selecionada, faça a verificação
    st.session_state.resposta_verificada = True # Muda o estado para verificado
    
    if resposta_selecionada == palavra_correta:
        st.session_state.mensagem_feedback = f"✅ **Resposta Certa!** A palavra é: *{palavra_correta}*."
        st.session_state.palavras_corretas += 1
        st.session_state.pontuacao_total += 1
    else:
        st.session_state.mensagem_feedback = f"❌ **Resposta Errada.** A correta era: *{palavra_correta}*."


# --- 3. CONFIGURAÇÃO DE DESIGN (CSS TEMÁTICO REFINADO) ---

def aplicar_tema(nivel):
    """Aplica o CSS com alto contraste, cores temáticas e decoração para cada subárea."""
    
    # 1. TEMAS E CORES PRINCIPAIS (Alto Contraste Garantido)
    
    # Cor de fundo padrão (Níveis Fácil/Médio/Difícil)
    FUNDO_PADRAO = "#F5F5DC"  # Bege claro (papel de campo)
    TEXTO_PADRAO = "#4B3832" # Marrom escuro
    
    # Mapeamento de estilos temáticos
    temas = {
        # Clássica: Papiro e Hieróglifos.
        "Clássica": {
            'estilo_fundo': 'background-color: #F8F4E3;', # Papiro claro
            'cor_texto': '#8B4513', # Marrom Sépia
            'emoji': "🏺🏛️"
        },
        # Subaquática: Oceano Profundo e Tesouros.
        "Subaquática": {
            'estilo_fundo': 'background: linear-gradient(to bottom, #001f3f, #003366);', # Gradiente Azul Marinho
            'cor_texto': '#ADD8E6', # Azul Claro (Alto Contraste)
            'emoji': "🌊⚓"
        },
        # Zooarqueologia: Ossos e Natureza.
        "Zooarqueologia": {
            'estilo_fundo': 'background-color: #F0F0F0;', # Osso/Marfim
            'cor_texto': '#36454F', # Cinza Ardósia (Alto Contraste)
            'emoji': "🦴🌿"
        },
        # Geoarqueologia: Estratos de Solo e Rochas.
        "Geoarqueologia": {
            'estilo_fundo': 'background: linear-gradient(to bottom, #A0522D, #696969);', # Marrom Terra a Cinza Rocha
            'cor_texto': '#FFDAB9', # Pêssego Claro (Alto Contraste)
            'emoji': "⛰️🪨"
        }
    }

    # Seleciona o tema ou usa o padrão
    tema_config = temas.get(nivel, {
        'estilo_fundo': f'background-color: {FUNDO_PADRAO};',
        'cor_texto': TEXTO_PADRAO,
        'emoji': "🔎"
    })
    
    estilo_aplicar = tema_config['estilo_fundo'] + f'color: {tema_config["cor_texto"]};'
    cor_primaria = tema_config['cor_texto']

    # Injeta o estilo de fundo no Streamlit App
    st.markdown(
        f'<style>.stApp {{ {estilo_aplicar} }}</style>', 
        unsafe_allow_html=True
    )

    # 2. APLICAÇÃO DE DECORAÇÃO NO TÍTULO
    
    # Adiciona o emoji temático ao título do nível
    if st.session_state.nivel_atual:
        emoji = tema_config['emoji']
        st.sidebar.markdown(f"### {emoji} **Nível Atual: {st.session_state.nivel_atual}**")
    
    # 3. CSS COMUM (Garantindo Consistência)
    st.markdown(f"""
    <style>
    /* Estilos para Títulos (Herda cor do tema) */
    h1, h2, h3 {{
        color: {cor_primaria} !important; 
        border-bottom: 2px solid #D2B48C;
        padding-bottom: 5px;
    }}
    /* Botões */
    .stButton>button {{
        background-color: #6B8E23; 
        color: white;
        border: none;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.4);
        font-weight: bold;
    }}
    /* Área de Dica (Manter sempre claro para máxima legibilidade) */
    .stMarkdown p {{
        font-size: 1.2em;
        padding: 15px;
        border: 1px solid #D2B48C;
        background-color: rgba(255, 255, 240, 0.9); /* Fundo quase branco semi-transparente */
        border-radius: 8px;
        color: #4B3832; /* Texto escuro para alto contraste na caixa de dica */
        text-shadow: none;
    }}
    /* Cores das Alternativas de Rádio (Garante que o texto do rádio seja legível contra o fundo) */
    .stRadio label > div:first-child {{
        color: {cor_primaria};
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # --- 4. EXIBIÇÃO DA INTERFACE ---

def mostrar_tela_inicial():
    """Mostra a tela de seleção de nível."""
    st.title("🗺️ Arqueologia em Camadas: O Quiz")
    st.header("Selecione o seu Nível de Descoberta")
    
    # Níveis Regulares
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Nível 1: FÁCIL (Fundamentos)", on_click=carregar_nivel, args=("Fácil",), use_container_width=True)
    with col2:
        st.button("Nível 2: MÉDIO (Técnicas de Campo)", on_click=carregar_nivel, args=("Médio",), use_container_width=True)
    with col3:
        st.button("Nível 3: DIFÍCIL (Teoria Avançada)", on_click=carregar_nivel, args=("Difícil",), use_container_width=True)

    # Níveis Específicos
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
    """Mostra a interface do quiz de múltipla escolha."""
    
    # Lida com o final do nível
    if st.session_state.fase_jogo == "finalizado":
        st.success(f"🥳 Nível '{st.session_state.nivel_atual}' COMPLETO!")
        st.balloons()
        st.write(f"Você acertou **{st.session_state.palavras_corretas}** de **{st.session_state.total_palavras}** palavras neste nível.")
        st.button("Voltar para Seleção de Nível", on_click=inicializar_estado_do_jogo)
        return

    # Exibe o jogo em andamento
    
    # Palavra e Dica Atual
    indice = st.session_state.indice_palavra
    palavra_correta, dica_atual = st.session_state.palavras_embaralhadas[indice]
    
    # Gera as alternativas para a palavra atual
    alternativas = gerar_alternativas(palavra_correta, st.session_state.nivel_atual)
    
    st.header(f"🗃️ Nível: {st.session_state.nivel_atual}")
    st.markdown(f"**Palavra {indice + 1}** de {st.session_state.total_palavras}")
    st.progress(indice / st.session_state.total_palavras)

    # Dica (Pista)
    st.subheader("🔍 Pista do Sítio:")
    st.markdown(f"<p>{dica_atual}</p>", unsafe_allow_html=True)
    
    st.subheader("Escolha a palavra correta:")

    # Formulário para a Múltipla Escolha
    with st.form(key=f"form_quiz_{indice}"):
        
        # O st.radio armazena a seleção em st.session_state.radio_selection
        st.radio(
            "Alternativas:",
            alternativas,
            key="radio_selection", # CHAVE FIXA para o callback ler o valor
            disabled=st.session_state.resposta_verificada,
            index=None
        )
        
        # --- Lógica do Botão Dinâmico ---
        col_btn1, col_btn2 = st.columns([1, 4])
        
        with col_btn1:
            if not st.session_state.resposta_verificada:
                # Botão 'Verificar' - Usa o callback para submeter a resposta
                st.form_submit_button(
                    label='Escavar e Verificar', 
                    on_click=submeter_resposta, 
                    args=(palavra_correta,)
                )
            else:
                # Botão 'Próxima Pergunta' - Visível após responder
                st.form_submit_button(
                    label='Próxima Pergunta >>', 
                    on_click=avancar_pergunta
                )
                
    # Feedback da última tentativa (Exibido após verificar)
    if st.session_state.mensagem_feedback:
        if "Certa" in st.session_state.mensagem_feedback:
            st.success(st.session_state.mensagem_feedback)
        elif "Errada" in st.session_state.mensagem_feedback:
            st.error(st.session_state.mensagem_feedback)
        else:
             st.warning(st.session_state.mensagem_feedback) 
            
    st.button("Mudar Nível", on_click=inicializar_estado_do_jogo)


# --- 5. FUNÇÃO PRINCIPAL DE EXECUÇÃO ---

def main():
    # Inicializa o estado se for a primeira vez
    if 'fase_jogo' not in st.session_state:
        inicializar_estado_do_jogo()
    
    # Aplica o tema visual dependendo do nível atual
    aplicar_tema(st.session_state.nivel_atual)

    # Gerencia a tela a ser exibida
    if st.session_state.nivel_atual is None:
        mostrar_tela_inicial()
    else:
        mostrar_tela_jogo()
        
    st.sidebar.header("Status")
    st.sidebar.markdown(f"**Total de Acertos Acumulados:** {st.session_state.pontuacao_total}")
    if st.session_state.nivel_atual and st.session_state.fase_jogo != "inicio":
         st.sidebar.markdown(f"**Progresso no Nível {st.session_state.nivel_atual}:** {st.session_state.palavras_corretas}/{st.session_state.total_palavras}")

if __name__ == "__main__":
    main()
