import streamlit as st
import random
import pandas as pd
import os # Importação necessária para lidar com o arquivo

# --- 0. CONFIGURAÇÃO DE ARQUIVO DO RANKING ---
RANKING_FILE = 'ranking_arqueologia.csv'

def carregar_ranking():
    """Carrega o ranking do CSV ou cria um DataFrame vazio se o arquivo não existir."""
    if os.path.exists(RANKING_FILE):
        df = pd.read_csv(RANKING_FILE)
        # Garante que a coluna 'Pontuação' seja numérica e ordena
        df['Pontuação'] = pd.to_numeric(df['Pontuação'], errors='coerce')
        return df.sort_values(by='Pontuação', ascending=False).reset_index(drop=True)
    else:
        return pd.DataFrame(columns=['Nome', 'Pontuação'])

def salvar_ranking(nome, pontuacao):
    """Adiciona a nova pontuação ao ranking e salva no CSV."""
    df = carregar_ranking()
    novo_registro = pd.DataFrame([{'Nome': nome, 'Pontuação': pontuacao}])
    
    # Concatena o novo registro, ordena e pega o top 10 (opcional)
    df_atualizado = pd.concat([df, novo_registro], ignore_index=True)
    df_atualizado = df_atualizado.sort_values(by='Pontuação', ascending=False)
    
    # Limita ao Top 10 para não sobrecarregar
    df_atualizado = df_atualizado.head(10) 
    
    df_atualizado.to_csv(RANKING_FILE, index=False)
    return df_atualizado.reset_index(drop=True)

# --- 1. ESTRUTURA DE DADOS COM DICAS SIMPLIFICADAS ---
DADOS_ARQUEOLOGIA = {
    "Fácil": {
        "VESTIGIO": "Qualquer marca ou remanescente de algo antigo deixado por humanos.",
        "ESCAVACAO": "O trabalho de cavar o solo com cuidado para encontrar coisas antigas.",
        "CULTURA": "O jeito de viver, as crenças e os costumes de um povo.",
        "RUINA": "O que resistiu de um prédio ou construção muito antiga, que caiu.",
        "HISTORIA": "O estudo do passado humano, começando após a invenção da escrita.",
        "CERAMICA": "Objetos feitos de argila (barro) queimada, como potes e vasos.",
        "CAMADA": "Cada 'fatia' de terra que se depositou com o tempo, indicando idades.",
        "SITIO": "O local exato onde os arqueólogos encontram e estudam vestígios.",
        "MUSEU": "O lugar onde os artefatos encontrados são guardados e expostos ao público.",
        "PRE HISTORIA": "O tempo da humanidade antes de inventarem a escrita.",
        "ARTEFATO": "Qualquer objeto feito ou modificado pelas mãos humanas."
    },
    "Médio": {
        "ESTRATIGRAFIA": "O estudo das camadas de solo (estratos) para entender a ordem dos eventos.",
        "PINTURA RUPESTRE": "Desenhos e pinturas feitas por humanos em paredes de cavernas ou rochas.",
        "DATAÇAO": "A técnica usada para descobrir a idade exata de um objeto ou de uma camada.",
        "TIPOLOGIA": "O sistema de classificar os artefatos agrupando-os por forma e função.",
        "PROSPECCAO": "A busca inicial e reconhecimento de sítios arqueológicos na paisagem.",
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
        "ANTROPOFAGIA": "O costume de comer carne humana, estudado através de marcas em ossos antigos.",
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
            "NAUFRAGIO": "Os vestígios de uma embarcação que afundou no mar ou em um rio.",
            "NAVIO": "A embarcação principal de interesse nesta subárea da arqueologia.",
            "ANCORA": "Objeto pesado que prende o barco ao fundo, muitas vezes o primeiro achado de um naufrágio.",
            "MARITIMA": "Tudo que se relaciona com o mar, navegação e vida costeira antiga.",
            "INTERFACE": "A faixa de transição entre a água e ambiente terreste."
        },
        "Zooarqueologia": {
            "OSTEOLOGIA": "O estudo dos ossos; vital para identificar os restos de animais.",
            "FAUNA": "O conjunto de espécies de animais que viviam em um sítio.",
            "ESQUELETO": "A estrutura óssea do animal, usada para saber a espécie e o que foi consumido.",
            "DIETA": "O estudo do que os humanos comiam, baseado nos restos de animais encontrados.",
            "DOMESTICACAO": "O processo de transformar animais selvagens em dependentes dos humanos (criação)."
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
    
    # Salva a pontuação se estiver voltando do jogo para o menu (e se houve acertos)
    if 'fase_jogo' in st.session_state and st.session_state.fase_jogo == "jogando":
        if st.session_state.pontuacao_total > 0 and st.session_state.get('nome_jogador'):
             st.session_state.ranking_atualizado = salvar_ranking(
                 st.session_state.nome_jogador, 
                 st.session_state.pontuacao_total
             )
        
    st.session_state.nivel_atual = None
    st.session_state.indice_palavra = 0
    st.session_state.palavras_embaralhadas = []
    st.session_state.palavras_corretas = 0
    st.session_state.total_palavras = 0
    st.session_state.mensagem_feedback = ""
    st.session_state.fase_jogo = "inicio"
    
    # Zera a pontuação total APENAS quando volta para o menu principal
    st.session_state.pontuacao_total = 0
        
    st.session_state.resposta_verificada = False
    st.session_state.radio_selection = None
    
    # Inicializa ou carrega o ranking
    if 'ranking_atualizado' not in st.session_state:
        st.session_state.ranking_atualizado = carregar_ranking()

# Funções auxiliares de palavras e alternativas (mantidas)
def get_palavras_do_contexto(nome_nivel):
    """Retorna a lista de todas as palavras (chaves) de um nível ou subárea."""
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
    """Gera três alternativas contextuais (uma correta e duas do mesmo contexto)."""
    
    palavras_contexto = get_palavras_do_contexto(nome_nivel)
    distratores_potenciais = [p for p in palavras_contexto if p != palavra_correta]
    alternativas_falsas = []
    
    if len(distratores_potenciais) >= 2:
        alternativas_falsas = random.sample(distratores_potenciais, 2)
    else:
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
                alternativas_falsas.extend(random.sample(TODAS_AS_PALAVRAS, num_faltante))

    alternativas = [palavra_correta] + alternativas_falsas
    random.shuffle(alternativas)
    return alternativas


def carregar_nivel(nome_nivel):
    """Carrega as palavras para um nível, ZERA o estado do quiz atual e mantém a pontuação total."""
    
    # 1. ZERA O ESTADO DO QUIZ ATUAL (Variáveis que controlam a pergunta)
    st.session_state.nivel_atual = nome_nivel
    st.session_state.indice_palavra = 0 # Zera o índice
    st.session_state.palavras_corretas = 0 # Zera acertos do nível atual (se precisar usar)
    st.session_state.mensagem_feedback = ""
    st.session_state.resposta_verificada = False
    st.session_state.radio_selection = None
    
    # 2. CARREGA AS PALAVRAS DO NOVO NÍVEL
    if nome_nivel in DADOS_ARQUEOLOGIA:
        palavras_dicas = DADOS_ARQUEOLOGIA[nome_nivel]
    elif nome_nivel in DADOS_ARQUEOLOGIA["Específicos"]:
        palavras_dicas = DADOS_ARQUEOLOGIA["Específicos"][nome_nivel]
    else:
        st.error("Nível não encontrado!")
        return

    # 3. ATUALIZA O TOTAL E EMBARALHA
    # A lista de palavras DEVE ser substituída pelas novas do nível, não estendida.
    st.session_state.total_palavras_do_nivel = len(palavras_dicas) # Novo total para a barra de progresso
    palavras_lista = list(palavras_dicas.items())
    random.shuffle(palavras_lista)
    st.session_state.palavras_embaralhadas = palavras_lista # Substitui a lista
    
    st.session_state.fase_jogo = "jogando"

def avancar_pergunta():
    """Limpa o feedback, avança o índice e verifica se o nível terminou."""
    st.session_state.resposta_verificada = False
    st.session_state.mensagem_feedback = ""
    st.session_state.radio_selection = None 
    
    # Avança para a próxima palavra
    st.session_state.indice_palavra += 1
    
    # Nota: A lógica de 'finalizado' agora é tratada implicitamente ao voltar para a tela inicial
    # Se todos os níveis fossem sequenciais, a lógica estaria aqui.
    # Como os níveis são escolhidos, o jogo só termina quando o usuário clica em "Mudar Nível".

def submeter_resposta(palavra_correta):
    """
    Função de callback para o botão 'Verificar'. 
    Usa o valor da sessão de estado do rádio e chama a verificação.
    """
    resposta_selecionada = st.session_state.get("radio_selection")
    
    if not resposta_selecionada:
        st.session_state.mensagem_feedback = "⚠️ Por favor, selecione uma alternativa antes de verificar!"
        st.session_state.resposta_verificada = False
        return

    st.session_state.resposta_verificada = True
    
    if resposta_selecionada == palavra_correta:
        st.session_state.mensagem_feedback = f"✅ **Resposta Certa!** A palavra é: *{palavra_correta}*."
        st.session_state.palavras_corretas += 1
        st.session_state.pontuacao_total += 1 # Pontuação acumulada
    else:
        st.session_state.mensagem_feedback = f"❌ **Resposta Errada.** A correta era: *{palavra_correta}*."


# --- 3. CONFIGURAÇÃO DE DESIGN (CSS TEMÁTICO REFINADO) ---

def aplicar_tema(nivel):
    """Aplica o CSS com alto contraste, cores temáticas e decoração para cada subárea."""
    
    FUNDO_PADRAO = "#F5F5DC"
    TEXTO_PADRAO = "#4B3832"
    
    # Mapeamento de estilos temáticos
    temas = {
        "Clássica": {
            'estilo_fundo': 'background-color: #F8F4E3;', 
            'cor_texto': '#8B4513',
            'sombra_texto': 'none',
            'emoji': "🏺🏛️"
        },
        "Subaquática": {
            'estilo_fundo': 'background: linear-gradient(to bottom, #001f3f, #003366);', 
            'cor_texto': '#FFFFFF', # Branco Puro
            'sombra_texto': '1px 1px 2px #000000',
            'emoji': "🌊⚓"
        },
        "Zooarqueologia": {
            'estilo_fundo': 'background-color: #F0F0F0;', 
            'cor_texto': '#36454F',
            'sombra_texto': 'none',
            'emoji': "🦴🌿"
        },
        "Geoarqueologia": {
            'estilo_fundo': 'background: linear-gradient(to bottom, #A0522D, #696969);', 
            'cor_texto': '#FFFFFF', # Branco Puro
            'sombra_texto': '1px 1px 2px #000000',
            'emoji': "⛰️🪨"
        }
    }

    tema_config = temas.get(nivel, {
        'estilo_fundo': f'background-color: {FUNDO_PADRAO};',
        'cor_texto': TEXTO_PADRAO,
        'sombra_texto': 'none',
        'emoji': "🔎"
    })
    
    estilo_aplicar = tema_config['estilo_fundo'] + f'color: {tema_config["cor_texto"]};'
    cor_primaria = tema_config['cor_texto']
    sombra_texto = tema_config['sombra_texto']
    
    st.markdown(f'<style>.stApp {{ {estilo_aplicar} }}</style>', unsafe_allow_html=True)
    
    # Adiciona decoração ao título (se estiver no jogo)
    if st.session_state.nivel_atual and st.session_state.fase_jogo != "inicio":
        emoji = tema_config['emoji']
        st.sidebar.markdown(f"### {emoji} **Nível: {st.session_state.nivel_atual}**")
        
    # CSS PARA GARANTIR LEGIBILIDADE DOS COMPONENTES
    st.markdown(f"""
    <style>
    /* 1. Cores de Texto e Títulos */
    .stApp, .stButton, .stProgress, .stRadio, .stForm, .stSidebar, .stAlert {{
        color: {cor_primaria} !important;
        text-shadow: {sombra_texto};
    }}
    h1, h2, h3 {{
        color: {cor_primaria} !important; 
        border-bottom: 2px solid #D2B48C;
        padding-bottom: 5px;
        text-shadow: {sombra_texto};
    }}
    /* 2. Área de Dica (Mantida clara) */
    .stMarkdown p {{
        background-color: rgba(255, 255, 240, 0.95) !important;
        color: #4B3832 !important;
        border: 1px solid {cor_primaria};
        text-shadow: none;
    }}
    /* 3. Botões (Contraste reforçado) */
    .stButton>button {{
        background-color: #38761D;
        color: white;
        border: 2px solid #548235;
        box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.6);
        font-weight: bold;
        text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.4);
    }}
    /* 4. Radio Buttons (Contraste reforçado nas alternativas) */
      /* Cores das Alternativas de Rádio - Forçar cor do texto das opções */
    .stRadio > div > div > div > label > div {{
        color: {cor_primaria} !important;
        text-shadow: {sombra_texto};
    }}
    /* Alternativa mais específica para o texto das opções do radio */
    .stRadio label > div:last-child > div {{
        color: {cor_primaria} !important;
        text-shadow: {sombra_texto};
        font-weight: 500;
    </style>
    """, unsafe_allow_html=True)


# --- 4. EXIBIÇÃO DA INTERFACE ---

def mostrar_tela_inicial():
    """Mostra a tela de seleção de nível e o ranking."""
    
    st.title("🗺️ Mistério Arqueológico: O Quiz")
    
    # --- NOVIDADE: CAMPO DE NOME DO JOGADOR ---
    st.header("1. Identificação do Arqueólogo")
    
    # Campo de texto para o nome
    st.text_input(
        "Insira seu nome/apelido de campo:", 
        key="nome_jogador", 
        placeholder="Ex: Indiana Jones"
    )

    # Verifica se o nome foi inserido antes de mostrar os níveis
    if st.session_state.get('nome_jogador') and st.session_state.nome_jogador.strip() != "":
        st.success(f"Arqueólogo(a) **{st.session_state.nome_jogador}**, sua escavação pode começar!")

        st.header("2. Selecione o seu Nível de Descoberta")
        
        # Níveis Regulares
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Nível 1: FÁCIL", on_click=carregar_nivel, args=("Fácil",), use_container_width=True)
        with col2:
            st.button("Nível 2: MÉDIO", on_click=carregar_nivel, args=("Médio",), use_container_width=True)
        with col3:
            st.button("Nível 3: DIFÍCIL", on_click=carregar_nivel, args=("Difícil",), use_container_width=True)

        # Níveis Específicos
        st.subheader("Nível 4: ESPECÍFICOS (Subáreas)")
        col_sub1, col_sub2, col_sub3, col_sub4 = st.columns(4)
        with col_sub1:
            st.button("Clássica", on_click=carregar_nivel, args=("Clássica",), use_container_width=True)
        with col_sub2:
            st.button("Subaquática", on_click=carregar_nivel, args=("Subaquática",), use_container_width=True)
        with col_sub3:
            st.button("Zooarqueologia", on_click=carregar_nivel, args=("Zooarqueologia",), use_container_width=True)
        with col_sub4:
            st.button("Geoarqueologia", on_click=carregar_nivel, args=("Geoarqueologia",), use_container_width=True)

    else:
        st.info("Por favor, insira seu nome para iniciar o jogo.")

    # --- NOVIDADE: EXIBIÇÃO DO RANKING ---
    st.markdown("---")
    st.header("🏆 Ranking dos Melhores Arqueólogos")
    df_ranking = carregar_ranking()
    
    if not df_ranking.empty:
        # Renomeia as colunas para exibição amigável
        df_display = df_ranking.rename(columns={'Nome': 'Nome', 'Pontuação': 'Acertos'})
        # Adiciona a coluna de Posição
        df_display.index = df_display.index + 1
        df_display.index.name = 'Posição'
        st.table(df_display)
    else:
        st.info("Nenhum registro de pontuação ainda. Seja o primeiro a jogar!")


def mostrar_tela_jogo():
    """Mostra a interface do quiz de múltipla escolha."""
    
    indice = st.session_state.indice_palavra
    
    # Verifica se há perguntas para exibir
    if indice >= st.session_state.total_palavras_do_nivel:
        # 1. TRATAMENTO DE FIM DE NÍVEL
        
        # Salva a pontuação (se for o último nível jogado)
        if st.session_state.pontuacao_total > 0 and st.session_state.get('nome_jogador'):
             st.session_state.ranking_atualizado = salvar_ranking(
                 st.session_state.nome_jogador, 
                 st.session_state.pontuacao_total
             )
        
        # Exibe a mensagem de finalização
        st.success(f"🥳 Fim da Escavação, **{st.session_state.nome_jogador}**!")
        st.balloons()
        st.markdown(f"Você completou a escavação com **{st.session_state.palavras_corretas}** acertos neste nível e **{st.session_state.pontuacao_total}** acertos totais.")
        st.markdown("Clique abaixo para ver o **Ranking** e escolher um novo nível.")
        
        # O botão reinicia o estado de jogo para "inicio" e salva a pontuação
        st.button("Voltar para Seleção de Nível", on_click=inicializar_estado_do_jogo)
        
        # É ESSENCIAL RETORNAR AQUI para parar a execução da função
        return 
    


# Na exibição da pergunta em andamento (abaixo):
# ...
# Progresso
st.markdown(f"**Pergunta {indice + 1}** de {st.session_state.total_palavras_do_nivel} no **Nível Atual**.")
st.progress(indice / st.session_state.total_palavras_do_nivel)



        st.success(f"🥳 Fim da Escavação, **{st.session_state.nome_jogador}**!")
        st.balloons()
        st.markdown(f"Você completou a escavação com **{st.session_state.palavras_corretas}** acertos!")
        st.markdown("Clique abaixo para salvar e ver o **Ranking**.")
        st.button("Voltar para Seleção de Nível", on_click=inicializar_estado_do_jogo)
        return

    # 2. EXIBIÇÃO DA PERGUNTA ATUAL
    
    palavra_correta, dica_atual = st.session_state.palavras_embaralhadas[indice]
    alternativas = gerar_alternativas(palavra_correta, st.session_state.nivel_atual)
    
    st.header(f"🗃️ Escavação em Andamento...")
    st.markdown(f"**Pergunta {indice + 1}** de {st.session_state.total_palavras} no total.")
    st.progress(indice / st.session_state.total_palavras)

    # Dica (Pista)
    st.subheader("🔍 Pista do Sítio:")
    st.markdown(f"<p>{dica_atual}</p>", unsafe_allow_html=True)
    
    st.subheader("Escolha a palavra correta:")

    # Formulário para a Múltipla Escolha
    with st.form(key=f"form_quiz_{indice}"):
        
        st.radio(
            "Alternativas:",
            alternativas,
            key="radio_selection",
            disabled=st.session_state.resposta_verificada,
            index=None
        )
        
        # Lógica do Botão Dinâmico
        col_btn1, col_btn2 = st.columns([1, 4])
        
        with col_btn1:
            if not st.session_state.resposta_verificada:
                st.form_submit_button(
                    label='Escavar e Verificar', 
                    on_click=submeter_resposta, 
                    args=(palavra_correta,)
                )
            else:
                st.form_submit_button(
                    label='Próxima Pergunta >>', 
                    on_click=avancar_pergunta
                )
                
    # Feedback da última tentativa
    if st.session_state.mensagem_feedback:
        if "Certa" in st.session_state.mensagem_feedback:
            st.success(st.session_state.mensagem_feedback)
        elif "Errada" in st.session_state.mensagem_feedback:
            st.error(st.session_state.mensagem_feedback)
        else:
             st.warning(st.session_state.mensagem_feedback) 
            
    st.button("Finalizar Escavação e Salvar Pontuação", on_click=inicializar_estado_do_jogo)


# --- 5. FUNÇÃO PRINCIPAL DE EXECUÇÃO ---

def main():
    if 'fase_jogo' not in st.session_state:
        inicializar_estado_do_jogo()
    
    aplicar_tema(st.session_state.nivel_atual)

    if st.session_state.fase_jogo == "inicio" or st.session_state.fase_jogo == "finalizado":
        mostrar_tela_inicial()
    else:
        mostrar_tela_jogo()
        
    st.sidebar.header("Status")
    st.sidebar.markdown(f"**Arqueólogo(a):** {st.session_state.get('nome_jogador', 'Visitante')}")
    st.sidebar.markdown(f"**Acertos Acumulados:** {st.session_state.pontuacao_total}")
    
    if st.session_state.fase_jogo == "jogando" and st.session_state.total_palavras > 0:
         progresso_atual = st.session_state.palavras_corretas + (st.session_state.indice_palavra - st.session_state.palavras_corretas)
         st.sidebar.markdown(f"**Progresso Total:** {st.session_state.indice_palavra} / {st.session_state.total_palavras}")
        
if __name__ == "__main__":
    main()
