# Assistente Virtual Bilíngue com Edição de Código Python
# Requisitos: Python 3.8+ (recomendado para AST), SpeechRecognition, PyAudio, pyttsx3, NLTK
#
# Instalação de dependências no Ubuntu:
# 1. Python 3 (sudo apt install python3 python3-pip)
# 2. PortAudio (sudo apt install portaudio19-dev)
# 3. Bibliotecas Python:
#    pip3 install SpeechRecognition PyAudio pyttsx3 nltk
#
# 4. Baixar recursos do NLTK (necessário na primeira execução):
#    No console Python: import nltk; nltk.download('punkt'); nltk.download('stopwords')

import speech_recognition as sr
import pyttsx3
import nltk
import time
import os
import ast # Para analisar código Python

class EditorTextoCodigoVoz:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        self.current_language = 'pt-BR' # 'pt-BR' ou 'en-US'
        self.voice_ids = {'pt-BR': None, 'en-US': None}
        self._configurar_vozes()

        # Para edição de texto simples
        self.texto_editado = [] 
        self.escrevendo_continuamente = False

        # Para edição de código Python
        self.active_file = None
        self.file_content_lines = [] # Linhas do arquivo de código ativo
        self.escrevendo_corpo_funcao = False
        self.funcao_sendo_escrita_nome = None
        self.funcao_sendo_escrita_params = "" # Parâmetros como string
        self.indentacao_padrao = "    " # 4 espaços

        self.comandos_pt = {
            "SAIR": ["sair", "encerrar", "tchau"],
            "AJUDA": ["ajuda", "comandos"],
            "MUDAR_IDIOMA_EN": ["mudar idioma para inglês", "falar em inglês"],
            "MUDAR_IDIOMA_PT": ["mudar idioma para português", "falar em português"],
            # Comandos de texto
            "COMEÇAR_ESCREVER": ["começar a escrever", "iniciar escrita"],
            "PARAR_ESCREVER": ["parar de escrever", "pare de escrever"],
            "ADD_LINHA": ["adicionar linha"],
            "DEL_LINHA": ["deletar linha", "excluir linha"],
            "SUB_LINHA": ["substituir linha"],
            "SUB_TEXTO": ["substituir texto"],
            "MOSTRAR_TEXTO": ["mostrar texto", "ler texto"],
            "SALVAR_TEXTO_SIMPLES": ["salvar texto simples", "gravar texto simples"],
            "LIMPAR_TEXTO": ["limpar texto"],
            # Comandos de código
            "ABRIR_ARQUIVO": ["abrir arquivo", "carregar arquivo"],
            "SALVAR_ARQUIVO_CODIGO": ["salvar arquivo de código", "gravar arquivo de código"],
            "MOSTRAR_CODIGO": ["mostrar código", "ler código"],
            "FECHAR_ARQUIVO_CODIGO": ["fechar arquivo de código"],
            "COPIAR_FUNCAO": ["copiar função"], # "copiar função NOME daqui para ARQUIVO_DESTINO" ou "copiar função NOME do ARQUIVO_ORIGEM para ARQUIVO_DESTINO"
            "DELETAR_FUNCAO": ["deletar função", "excluir função"], # "deletar função NOME"
            "CRIAR_FUNCAO": ["criar função"], # "criar função NOME" ou "criar função NOME com parâmetros PARAMETROS"
            "TERMINAR_FUNCAO": ["terminar função", "finalizar função", "fim da função"]
        }
        self.comandos_en = {
            "SAIR": ["exit", "quit", "bye"],
            "AJUDA": ["help", "commands"],
            "MUDAR_IDIOMA_EN": ["change language to english", "speak in english"],
            "MUDAR_IDIOMA_PT": ["change language to portuguese", "speak in portuguese"],
            # Text commands
            "COMEÇAR_ESCREVER": ["start writing", "begin writing"],
            "PARAR_ESCREVER": ["stop writing"],
            "ADD_LINHA": ["add line"],
            "DEL_LINHA": ["delete line", "remove line"],
            "SUB_LINHA": ["replace line"],
            "SUB_TEXTO": ["replace text"],
            "MOSTRAR_TEXTO": ["show text", "read text"],
            "SALVAR_TEXTO_SIMPLES": ["save simple text"],
            "LIMPAR_TEXTO": ["clear text"],
            # Code commands
            "ABRIR_ARQUIVO": ["open file", "load file"],
            "SALVAR_ARQUIVO_CODIGO": ["save code file"],
            "MOSTRAR_CODIGO": ["show code", "read code"],
            "FECHAR_ARQUIVO_CODIGO": ["close code file"],
            "COPIAR_FUNCAO": ["copy function"], # "copy function NAME from here to DEST_FILE" or "copy function NAME from SOURCE_FILE to DEST_FILE"
            "DELETAR_FUNCAO": ["delete function", "remove function"], # "delete function NAME"
            "CRIAR_FUNCAO": ["create function"], # "create function NAME" or "create function NAME with parameters PARAMETERS"
            "TERMINAR_FUNCAO": ["end function", "finish function"]
        }
        
        self.saudacoes = {'pt-BR': "Olá! Sou seu assistente de edição. Diga 'ajuda' para ver os comandos.", 
                          'en-US': "Hello! I'm your editing assistant. Say 'help' for commands."}
        print("Assistente de Edição de Texto e Código iniciado.")
        self.falar(self.saudacoes[self.current_language])

    def _configurar_vozes(self):
        voices = self.tts_engine.getProperty('voices')
        # Tenta encontrar vozes específicas
        for voice in voices:
            if "brazil" in voice.name.lower() or "portuguese" in voice.name.lower():
                if not self.voice_ids['pt-BR']: self.voice_ids['pt-BR'] = voice.id
            if voice.languages and ('en_US' in voice.languages or 'en-US' in voice.languages):
                 if not self.voice_ids['en-US']: self.voice_ids['en-US'] = voice.id
        
        # Fallback para vozes mais genéricas se as específicas não forem encontradas
        if not self.voice_ids['pt-BR']:
            for voice in voices:
                if "portuguese" in voice.name.lower():
                    self.voice_ids['pt-BR'] = voice.id
                    break
        if not self.voice_ids['en-US']:
            for voice in voices:
                if "english" in voice.name.lower() and ('US' in voice.id or 'America' in voice.name): # Prioriza US
                     self.voice_ids['en-US'] = voice.id
                     break
        if not self.voice_ids['en-US']: # Qualquer inglês se US não for encontrado
            for voice in voices:
                if "english" in voice.name.lower():
                     self.voice_ids['en-US'] = voice.id
                     break
        
        # Define a taxa de fala
        self.tts_engine.setProperty('rate', 180)
        # Define a voz inicial
        if self.voice_ids[self.current_language]:
            self.tts_engine.setProperty('voice', self.voice_ids[self.current_language])
        else:
            print(f"Aviso: Voz para {self.current_language} não encontrada. Usando voz padrão.")

    def falar(self, texto, lang=None):
        """Converte texto em fala no idioma especificado ou no atual."""
        target_lang = lang if lang else self.current_language
        print(f"Assistente ({target_lang}): {texto}")
        
        current_voice = self.tts_engine.getProperty('voice')
        target_voice_id = self.voice_ids.get(target_lang)

        if target_voice_id and target_voice_id != current_voice:
            try:
                self.tts_engine.setProperty('voice', target_voice_id)
            except Exception as e:
                print(f"Erro ao definir voz para {target_lang}: {e}. Usando voz atual.")
        elif not target_voice_id:
             print(f"Aviso: Voz para {target_lang} não configurada. Usando voz atual.")

        self.tts_engine.say(texto)
        self.tts_engine.runAndWait()

    def ouvir(self):
        """Captura áudio e converte para texto no idioma atual."""
        with self.microphone as source:
            # self.falar("Ouvindo...", self.current_language) # Pode ser verboso
            print(f"Ouvindo ({self.current_language})...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=20)
            except sr.WaitTimeoutError:
                return None

        try:
            print("Reconhecendo...")
            # Tenta reconhecer no idioma atual
            comando = self.recognizer.recognize_google(audio, language=self.current_language)
            print(f"Você ({self.current_language}): {comando}")
            return comando.lower()
        except sr.RequestError:
            msg = {"pt-BR": "Não consegui me conectar ao serviço de reconhecimento.",
                   "en-US": "Could not connect to the recognition service."}
            self.falar(msg[self.current_language])
            return None
        except sr.UnknownValueError:
            # Não fala nada para não ser muito verboso em caso de não entendimento
            print("Não entendi o que você disse.")
            return None

    def _get_comandos_atuais(self):
        return self.comandos_pt if self.current_language == 'pt-BR' else self.comandos_en

    def _comando_matches(self, comando_falado, chave_comando):
        comandos_atuais = self._get_comandos_atuais()
        if chave_comando in comandos_atuais:
            for gatilho in comandos_atuais[chave_comando]:
                if comando_falado.startswith(gatilho):
                    return True, gatilho # Retorna True e o gatilho que combinou
        return False, None

    def processar_comando(self, comando):
        """Processa o comando de voz."""
        if not comando:
            return True

        comandos_atuais = self._get_comandos_atuais()
        textos_feedback = {
            'pt-BR': {
                'idioma_mudado': "Idioma alterado para {}.",
                'ingles': "Inglês",
                'portugues': "Português",
                'escrita_cont_on': "Modo de escrita contínua ativado. Diga 'parar de escrever' para finalizar.",
                'escrita_cont_off': "Modo de escrita contínua desativado.",
                'linha_adicionada': "Linha adicionada.",
                'linha_adicionada_pos': "Linha adicionada na posição {}.",
                'linha_removida': "Linha {} removida: {}",
                'linha_substituida': "Linha {} substituída.",
                'texto_substituido': "Texto '{}' substituído por '{}'.",
                'texto_nao_encontrado': "Texto '{}' não encontrado.",
                'texto_salvo': "Texto salvo em {}.",
                'texto_limpo': "Texto limpo.",
                'arquivo_aberto': "Arquivo {} aberto.",
                'erro_abrir_arquivo': "Erro ao abrir arquivo {}: {}",
                'nenhum_arquivo_aberto': "Nenhum arquivo de código aberto.",
                'arquivo_salvo': "Arquivo {} salvo.",
                'erro_salvar_arquivo': "Erro ao salvar arquivo {}: {}",
                'arquivo_fechado': "Arquivo {} fechado.",
                'funcao_copiada': "Função {} copiada de {} para {}.",
                'funcao_copiada_ativo': "Função {} copiada do arquivo ativo para {}.",
                'erro_copiar_funcao': "Erro ao copiar função: {}.",
                'funcao_nao_encontrada': "Função {} não encontrada em {}.",
                'funcao_deletada': "Função {} deletada de {}.",
                'erro_deletar_funcao': "Erro ao deletar função: {}.",
                'funcao_criada_inicio': "Criando função {}({}). Dite o corpo da função. Diga 'terminar função' para finalizar.",
                'corpo_funcao_finalizado': "Corpo da função {} finalizado.",
                'erro_criar_funcao': "Erro ao criar função: {}.",
                'comando_nao_reconhecido': "Comando não reconhecido.",
                'saindo': "Encerrando o assistente. Até logo!",
                'ajuda_geral': "Você pode dizer: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, ou {}.",
                'ajuda_texto': "'começar a escrever', 'adicionar linha TEXTO', 'deletar linha NUM', 'substituir linha NUM por TEXTO', 'substituir texto ANTIGO por NOVO', 'mostrar texto', 'salvar texto simples', 'limpar texto'",
                'ajuda_codigo': "'abrir arquivo NOME.py', 'salvar arquivo de código', 'mostrar código', 'fechar arquivo de código', 'copiar função NOME para ARQUIVO.py', 'deletar função NOME', 'criar função NOME'",
                'ajuda_idioma': "'mudar idioma para inglês', 'mudar idioma para português'",
                'ajuda_sair': "'sair'"
            },
            'en-US': {
                'idioma_mudado': "Language changed to {}.",
                'ingles': "English",
                'portugues': "Portuguese",
                'escrita_cont_on': "Continuous writing mode activated. Say 'stop writing' to finish.",
                'escrita_cont_off': "Continuous writing mode deactivated.",
                'linha_adicionada': "Line added.",
                'linha_adicionada_pos': "Line added at position {}.",
                'linha_removida': "Line {} removed: {}",
                'linha_substituida': "Line {} replaced.",
                'texto_substituido': "Text '{}' replaced with '{}'.",
                'texto_nao_encontrado': "Text '{}' not found.",
                'texto_salvo': "Text saved to {}.",
                'texto_limpo': "Text cleared.",
                'arquivo_aberto': "File {} opened.",
                'erro_abrir_arquivo': "Error opening file {}: {}",
                'nenhum_arquivo_aberto': "No code file is open.",
                'arquivo_salvo': "File {} saved.",
                'erro_salvar_arquivo': "Error saving file {}: {}",
                'arquivo_fechado': "File {} closed.",
                'funcao_copiada': "Function {} copied from {} to {}.",
                'funcao_copiada_ativo': "Function {} copied from active file to {}.",
                'erro_copiar_funcao': "Error copying function: {}.",
                'funcao_nao_encontrada': "Function {} not found in {}.",
                'funcao_deletada': "Function {} deleted from {}.",
                'erro_deletar_funcao': "Error deleting function: {}.",
                'funcao_criada_inicio': "Creating function {}({}). Dictate the function body. Say 'end function' to finish.",
                'corpo_funcao_finalizado': "Function body for {} finalized.",
                'erro_criar_funcao': "Error creating function: {}.",
                'comando_nao_reconhecido': "Command not recognized.",
                'saindo': "Exiting assistant. Goodbye!",
                'ajuda_geral': "You can say: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, or {}.",
                'ajuda_texto': "'start writing', 'add line TEXT', 'delete line NUM', 'replace line NUM with TEXT', 'replace text OLD with NEW', 'show text', 'save simple text', 'clear text'",
                'ajuda_codigo': "'open file NAME.py', 'save code file', 'show code', 'close code file', 'copy function NAME to FILE.py', 'delete function NAME', 'create function NAME'",
                'ajuda_idioma': "'change language to english', 'change language to portuguese'",
                'ajuda_sair': "'exit'"
            }
        }
        fb = textos_feedback[self.current_language]

        # --- Processamento de escrita de corpo de função ---
        if self.escrevendo_corpo_funcao:
            match, gatilho = self._comando_matches(comando, "TERMINAR_FUNCAO")
            if match:
                self.escrevendo_corpo_funcao = False
                if not self.file_content_lines[-1].strip().startswith(self.indentacao_padrao) and not self.file_content_lines[-1].strip(): # se a ultima linha adicionada ao corpo foi vazia
                     self.file_content_lines.append(self.indentacao_padrao + "pass") # Adiciona pass se o corpo estiver vazio
                elif not self.file_content_lines[-1].strip(): # Se a última linha é só indentação
                    self.file_content_lines[-1] = self.indentacao_padrao + "pass"

                self.falar(fb['corpo_funcao_finalizado'].format(self.funcao_sendo_escrita_nome))
                self.funcao_sendo_escrita_nome = None
                self.funcao_sendo_escrita_params = ""
                self.mostrar_codigo_atual()
            else:
                self.file_content_lines.append(self.indentacao_padrao + comando)
                print(f"Adicionado ao corpo da função: {self.indentacao_padrao + comando}")
            return True

        # --- Processamento de escrita contínua de texto simples ---
        if self.escrevendo_continuamente:
            match, _ = self._comando_matches(comando, "PARAR_ESCREVER")
            if match:
                self.escrevendo_continuamente = False
                self.falar(fb['escrita_cont_off'])
            else:
                self.texto_editado.append(comando)
                print(f"Linha adicionada (texto simples): {comando}")
            return True
        
        # --- Comandos Gerais ---
        match, _ = self._comando_matches(comando, "SAIR")
        if match:
            self.falar(fb['saindo'])
            return False

        match, _ = self._comando_matches(comando, "AJUDA")
        if match:
            self.falar(fb['ajuda_geral'].format(fb['ajuda_texto'], fb['ajuda_codigo'], fb['ajuda_idioma'], fb['ajuda_sair']))
            return True
        
        match, _ = self._comando_matches(comando, "MUDAR_IDIOMA_EN")
        if match:
            self.current_language = 'en-US'
            self._configurar_vozes() # Reconfigura para garantir a voz correta
            self.falar(fb['idioma_mudado'].format(fb['ingles']), lang='en-US')
            return True

        match, _ = self._comando_matches(comando, "MUDAR_IDIOMA_PT")
        if match:
            self.current_language = 'pt-BR'
            self._configurar_vozes()
            self.falar(fb['idioma_mudado'].format(fb['portugues']), lang='pt-BR')
            return True

        # --- Comandos de Edição de Texto Simples ---
        match, _ = self._comando_matches(comando, "COMEÇAR_ESCREVER")
        if match:
            self.escrevendo_continuamente = True
            self.falar(fb['escrita_cont_on'])
            return True

        match, gatilho = self._comando_matches(comando, "ADD_LINHA")
        if match:
            try:
                texto_para_adicionar = comando.split(gatilho, 1)[1].strip()
                # Tenta extrair "na linha X" / "at line X"
                num_linha_especifico = None
                keyword_pos = "na linha" if self.current_language == 'pt-BR' else "at line"
                
                if keyword_pos in texto_para_adicionar:
                    partes = texto_para_adicionar.split(keyword_pos)
                    texto_para_adicionar = partes[0].strip()
                    try:
                        num_linha_especifico = int(partes[1].strip()) - 1 
                        if not (0 <= num_linha_especifico <= len(self.texto_editado)):
                            self.falar("Número de linha inválido." if self.current_language == 'pt-BR' else "Invalid line number.")
                            return True
                    except ValueError:
                        self.falar("Número de linha inválido." if self.current_language == 'pt-BR' else "Invalid line number.")
                        return True
                
                if num_linha_especifico is not None:
                    self.texto_editado.insert(num_linha_especifico, texto_para_adicionar)
                    self.falar(fb['linha_adicionada_pos'].format(num_linha_especifico + 1))
                else:
                    self.texto_editado.append(texto_para_adicionar)
                    self.falar(fb['linha_adicionada'])
                self.mostrar_texto_simples_atual()
            except Exception as e:
                print(f"Erro ao adicionar linha: {e}")
                self.falar("Não entendi o texto para adicionar." if self.current_language == 'pt-BR' else "Couldn't understand the text to add.")
            return True

        match, gatilho = self._comando_matches(comando, "DEL_LINHA")
        if match:
            try:
                keyword_linha = "linha" if self.current_language == 'pt-BR' else "line"
                num_linha_str = comando.split(keyword_linha)[-1].strip()
                num_linha = int(num_linha_str) - 1
                if 0 <= num_linha < len(self.texto_editado):
                    linha_removida = self.texto_editado.pop(num_linha)
                    self.falar(fb['linha_removida'].format(num_linha + 1, linha_removida))
                    self.mostrar_texto_simples_atual()
                else:
                    self.falar("Número de linha inválido." if self.current_language == 'pt-BR' else "Invalid line number.")
            except (ValueError, IndexError):
                self.falar("Não identifiquei o número da linha." if self.current_language == 'pt-BR' else "Couldn't identify the line number.")
            return True
        
        match, gatilho = self._comando_matches(comando, "SUB_LINHA")
        if match:
            try:
                # Ex: "substituir linha 2 por NOVO TEXTO" / "replace line 2 with NEW TEXT"
                keyword_linha = "linha" if self.current_language == 'pt-BR' else "line"
                keyword_por = "por" if self.current_language == 'pt-BR' else "with"

                partes_comando = comando.split(gatilho, 1)[1].strip() # "linha 2 por NOVO TEXTO"
                num_linha_str, novo_texto_completo = partes_comando.split(f" {keyword_por} ", 1) # num_linha_str será "linha 2" ou "2"
                
                # Extrai apenas o número da string que pode conter "linha X"
                num_linha_digits = ''.join(filter(str.isdigit, num_linha_str))
                if not num_linha_digits:
                    raise ValueError("Número da linha não encontrado na string.")
                num_linha = int(num_linha_digits) - 1

                if 0 <= num_linha < len(self.texto_editado):
                    self.texto_editado[num_linha] = novo_texto_completo.strip()
                    self.falar(fb['linha_substituida'].format(num_linha + 1))
                    self.mostrar_texto_simples_atual()
                else:
                    self.falar("Número de linha inválido." if self.current_language == 'pt-BR' else "Invalid line number.")
            except Exception as e:
                print(f"Erro ao substituir linha: {e}")
                self.falar("Formato: {} NUM {} NOVO TEXTO".format(gatilho, keyword_por) if self.current_language == 'pt-BR' else "Format: {} NUM {} NEW TEXT".format(gatilho, keyword_por))
            return True

        match, gatilho = self._comando_matches(comando, "SUB_TEXTO")
        if match:
            try:
                keyword_por = "por" if self.current_language == 'pt-BR' else "with"
                partes = comando.split(gatilho, 1)[1].strip()
                texto_antigo, texto_novo = partes.split(f" {keyword_por} ", 1)
                texto_antigo = texto_antigo.strip()
                texto_novo = texto_novo.strip()
                
                modificado = False
                for i, linha in enumerate(self.texto_editado):
                    if texto_antigo in linha:
                        self.texto_editado[i] = linha.replace(texto_antigo, texto_novo)
                        modificado = True
                
                if modificado:
                    self.falar(fb['texto_substituido'].format(texto_antigo, texto_novo))
                    self.mostrar_texto_simples_atual()
                else:
                    self.falar(fb['texto_nao_encontrado'].format(texto_antigo))
            except Exception as e:
                print(f"Erro ao substituir texto: {e}")
                self.falar("Formato: {} ANTIGO {} NOVO".format(gatilho, keyword_por))

            return True

        match, _ = self._comando_matches(comando, "MOSTRAR_TEXTO")
        if match:
            self.mostrar_texto_simples_atual(falar_texto=True)
            return True

        match, gatilho = self._comando_matches(comando, "SALVAR_TEXTO_SIMPLES")
        if match:
            nome_arquivo = comando.split(gatilho, 1)[1].strip()
            if not nome_arquivo:
                nome_arquivo = "texto_editado.txt"
            if not nome_arquivo.endswith(".txt"):
                 nome_arquivo += ".txt"
            self.salvar_texto_simples_em_arquivo(nome_arquivo)
            return True
        
        match, _ = self._comando_matches(comando, "LIMPAR_TEXTO")
        if match:
            self.texto_editado = []
            self.falar(fb['texto_limpo'])
            return True

        # --- Comandos de Edição de Código ---
        match, gatilho = self._comando_matches(comando, "ABRIR_ARQUIVO")
        if match:
            try:
                nome_arquivo = comando.split(gatilho, 1)[1].strip()
                if not nome_arquivo.endswith(".py"):
                    nome_arquivo += ".py"
                self.abrir_arquivo_codigo(nome_arquivo)
            except IndexError:
                self.falar("Por favor, especifique o nome do arquivo." if self.current_language == 'pt-BR' else "Please specify the filename.")
            return True

        match, _ = self._comando_matches(comando, "SALVAR_ARQUIVO_CODIGO")
        if match:
            self.salvar_arquivo_codigo_ativo()
            return True

        match, _ = self._comando_matches(comando, "MOSTRAR_CODIGO")
        if match:
            self.mostrar_codigo_atual(falar_codigo=True)
            return True

        match, _ = self._comando_matches(comando, "FECHAR_ARQUIVO_CODIGO")
        if match:
            if self.active_file:
                self.falar(fb['arquivo_fechado'].format(self.active_file))
                self.active_file = None
                self.file_content_lines = []
            else:
                self.falar(fb['nenhum_arquivo_aberto'])
            return True

        match, gatilho = self._comando_matches(comando, "CRIAR_FUNCAO")
        if match:
            try:
                # "criar função NOME" ou "criar função NOME com parâmetros X, Y"
                # "create function NAME" or "create function NAME with parameters X, Y"
                partes = comando.split(gatilho, 1)[1].strip()
                nome_funcao = ""
                params_str = ""
                keyword_params_pt = "com parâmetros"
                keyword_params_en = "with parameters"

                if self.current_language == 'pt-BR' and keyword_params_pt in partes:
                    nome_funcao, params_str = partes.split(keyword_params_pt, 1)
                elif self.current_language == 'en-US' and keyword_params_en in partes:
                    nome_funcao, params_str = partes.split(keyword_params_en, 1)
                else:
                    nome_funcao = partes
                
                nome_funcao = nome_funcao.strip()
                params_str = params_str.strip()

                if not nome_funcao:
                    raise ValueError("Nome da função não especificado.")

                self.criar_funcao(nome_funcao, params_str)
            except Exception as e:
                print(f"Erro ao processar criar função: {e}")
                self.falar(fb['erro_criar_funcao'].format(e))
            return True

        match, gatilho = self._comando_matches(comando, "DELETAR_FUNCAO")
        if match:
            try:
                nome_funcao = comando.split(gatilho, 1)[1].strip()
                if not nome_funcao:
                    raise ValueError("Nome da função não especificado.")
                self.deletar_funcao_codigo(nome_funcao)
            except Exception as e:
                print(f"Erro ao processar deletar função: {e}")
                self.falar(fb['erro_deletar_funcao'].format(e))
            return True

        match, gatilho = self._comando_matches(comando, "COPIAR_FUNCAO")
        if match:
            # Formatos:
            # "copiar função NOMEFUNCAO para ARQUIVODESTINO.py" (do arquivo ativo)
            # "copiar função NOMEFUNCAO do ARQUIVOORIGEM.py para ARQUIVODESTINO.py"
            # "copy function FUNCNAME to DESTFILE.py"
            # "copy function FUNCNAME from SOURCEFILE.py to DESTFILE.py"
            try:
                partes_comando = comando.split(gatilho, 1)[1].strip() # "NOMEFUNCAO para ARQUIVODESTINO.py" ou "NOMEFUNCAO do ARQUIVOORIGEM.py para ARQUIVODESTINO.py"
                
                nome_funcao = ""
                arquivo_origem = self.active_file
                arquivo_destino = ""

                keyword_de_pt = "do arquivo"
                keyword_para_pt = "para"
                keyword_from_en = "from file" # ou "from"
                keyword_to_en = "to"

                if self.current_language == 'pt-BR':
                    if keyword_de_pt in partes_comando and keyword_para_pt in partes_comando:
                        # "NOMEFUNCAO do ARQUIVOORIGEM.py para ARQUIVODESTINO.py"
                        temp, arquivo_destino = partes_comando.split(f" {keyword_para_pt} ")
                        nome_funcao, arquivo_origem_temp = temp.split(f" {keyword_de_pt} ")
                        arquivo_origem = arquivo_origem_temp.strip()

                    elif keyword_para_pt in partes_comando:
                        # "NOMEFUNCAO para ARQUIVODESTINO.py" (origem é o ativo)
                        if not self.active_file:
                            self.falar(fb['nenhum_arquivo_aberto'])
                            return True
                        nome_funcao, arquivo_destino = partes_comando.split(f" {keyword_para_pt} ")
                    else:
                        raise ValueError("Formato do comando de cópia inválido.")
                else: # en-US
                    if keyword_from_en in partes_comando and keyword_to_en in partes_comando:
                        # "FUNCNAME from SOURCEFILE.py to DESTFILE.py"
                        # Need to be careful with "from file" vs "from"
                        # Assuming "from file" for clarity, or just "from"
                        # Let's try splitting by " to " first, then by " from "
                        temp, arquivo_destino = partes_comando.split(f" {keyword_to_en} ") # temp = "FUNCNAME from SOURCEFILE.py"
                        if keyword_from_en in temp:
                             nome_funcao, arquivo_origem_temp = temp.split(f" {keyword_from_en} ")
                        else: # Fallback if "from file" is not used, just "from"
                             nome_funcao, arquivo_origem_temp = temp.split(f" from ")
                        arquivo_origem = arquivo_origem_temp.strip()
                    elif keyword_to_en in partes_comando:
                        # "FUNCNAME to DESTFILE.py"
                        if not self.active_file:
                            self.falar(fb['nenhum_arquivo_aberto'])
                            return True
                        nome_funcao, arquivo_destino = partes_comando.split(f" {keyword_to_en} ")
                    else:
                        raise ValueError("Invalid copy command format.")

                nome_funcao = nome_funcao.strip()
                arquivo_destino = arquivo_destino.strip()
                if arquivo_origem: arquivo_origem = arquivo_origem.strip()

                if not nome_funcao or not arquivo_destino:
                    raise ValueError("Nome da função ou arquivo de destino não especificado.")
                if not arquivo_origem: # Se a origem não foi especificada e não há arquivo ativo
                    self.falar(fb['nenhum_arquivo_aberto'] + (" Especifique um arquivo de origem." if self.current_language == 'pt-BR' else " Specify a source file."))
                    return True

                self.copiar_funcao_codigo(nome_funcao, arquivo_origem, arquivo_destino)

            except Exception as e:
                print(f"Erro ao processar copiar função: {e}")
                self.falar(fb['erro_copiar_funcao'].format(e))
            return True
        
        # --- Se nenhum comando corresponder ---
        # self.falar(fb['comando_nao_reconhecido']) # Pode ser muito verboso
        print(f"Comando não processado: {comando}")
        return True

    # --- Métodos para Texto Simples ---
    def mostrar_texto_simples_atual(self, falar_texto=False):
        label_texto_atual = "--- Texto Atual ---" if self.current_language == 'pt-BR' else "--- Current Text ---"
        label_vazio = "(Vazio)" if self.current_language == 'pt-BR' else "(Empty)"
        label_este_e_o_texto = "Este é o texto atual:" if self.current_language == 'pt-BR' else "This is the current text:"
        label_texto_vazio = "O texto está vazio." if self.current_language == 'pt-BR' else "The text is empty."

        if not self.texto_editado:
            print(f"\n{label_texto_atual}")
            print(label_vazio)
            print("-------------------\n")
            if falar_texto:
                self.falar(label_texto_vazio)
            return

        print(f"\n{label_texto_atual}")
        for i, linha in enumerate(self.texto_editado):
            print(f"{i+1}: {linha}")
        print("-------------------\n")

        if falar_texto:
            self.falar(label_este_e_o_texto)
            for linha in self.texto_editado:
                self.falar(linha)
                time.sleep(0.2)

    def salvar_texto_simples_em_arquivo(self, nome_arquivo="texto_editado.txt"):
        fb = textos_feedback[self.current_language]
        if not self.texto_editado:
            self.falar("Não há texto para salvar." if self.current_language == 'pt-BR' else "No text to save.")
            return
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                for linha in self.texto_editado:
                    f.write(linha + "\n")
            self.falar(fb['texto_salvo'].format(nome_arquivo))
        except Exception as e:
            print(f"Erro ao salvar arquivo de texto simples: {e}")
            self.falar("Ocorreu um erro ao salvar o arquivo." if self.current_language == 'pt-BR' else "An error occurred while saving the file.")

    # --- Métodos para Código Python ---
    def _ler_arquivo_para_linhas(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().splitlines() # Mantém as linhas separadas
        except FileNotFoundError:
            self.falar(f"Arquivo {filepath} não encontrado." if self.current_language == 'pt-BR' else f"File {filepath} not found.")
            return None
        except Exception as e:
            self.falar(f"Erro ao ler {filepath}: {e}" if self.current_language == 'pt-BR' else f"Error reading {filepath}: {e}")
            return None

    def abrir_arquivo_codigo(self, filepath):
        fb = textos_feedback[self.current_language]
        content = self._ler_arquivo_para_linhas(filepath)
        if content is not None:
            self.active_file = filepath
            self.file_content_lines = content
            self.falar(fb['arquivo_aberto'].format(filepath))
            self.mostrar_codigo_atual()
        # else: Erro já falado por _ler_arquivo_para_linhas

    def salvar_arquivo_codigo_ativo(self):
        fb = textos_feedback[self.current_language]
        if not self.active_file:
            self.falar(fb['nenhum_arquivo_aberto'])
            return
        try:
            with open(self.active_file, "w", encoding="utf-8") as f:
                f.write("\n".join(self.file_content_lines)) # Junta as linhas com newline
            self.falar(fb['arquivo_salvo'].format(self.active_file))
        except Exception as e:
            print(f"Erro ao salvar arquivo de código: {e}")
            self.falar(fb['erro_salvar_arquivo'].format(self.active_file, e))

    def mostrar_codigo_atual(self, falar_codigo=False):
        label_codigo_atual = f"--- Código em {self.active_file} ---" if self.active_file else "--- Nenhum Código Aberto ---"
        label_vazio = "(Vazio)" if self.current_language == 'pt-BR' else "(Empty)"
        label_este_e_o_codigo = f"Este é o código em {self.active_file}:" if self.active_file else "Nenhum arquivo de código aberto."
        label_codigo_vazio = "O arquivo de código está vazio ou não está aberto."

        if not self.active_file or not self.file_content_lines:
            print(f"\n{label_codigo_atual}")
            print(label_vazio)
            print("-------------------\n")
            if falar_codigo:
                self.falar(label_codigo_vazio if self.current_language == 'pt-BR' else "The code file is empty or not open.")
            return

        print(f"\n{label_codigo_atual}")
        for i, linha in enumerate(self.file_content_lines):
            print(f"{i+1:03d}: {linha}") # Adiciona números de linha formatados
        print("-------------------\n")

        if falar_codigo:
            self.falar(label_este_e_o_codigo)
            # Ler código pode ser muito longo, talvez ler apenas as primeiras N linhas ou resumo?
            # Por agora, lê tudo, mas pode ser interrompido pelo usuário.
            for linha_num, linha_codigo in enumerate(self.file_content_lines):
                self.falar(f"linha {linha_num + 1}: {linha_codigo}")
                time.sleep(0.3)
                if len(self.file_content_lines) > 10 and linha_num > 8 : # Limita a fala para códigos longos
                    self.falar("... e mais linhas.")
                    break


    def _find_function_node(self, code_string, function_name):
        """Encontra o nó AST de uma função e suas linhas de início/fim."""
        try:
            tree = ast.parse(code_string)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    start_line = node.lineno
                    # end_lineno está disponível em Python 3.8+
                    # Para versões anteriores, seria mais complexo determinar o fim exato.
                    end_line = getattr(node, 'end_lineno', None)
                    if end_line is None: # Fallback simples (pode não ser perfeito)
                        # Tenta encontrar a última linha do corpo da função
                        if node.body:
                            end_line = node.body[-1].lineno 
                            # Se a última instrução do corpo for composta (ex: if, for, while, try)
                            # precisamos do end_lineno dela.
                            last_stmt_end_line = getattr(node.body[-1], 'end_lineno', node.body[-1].lineno)
                            end_line = max(end_line, last_stmt_end_line)
                        else: # Função vazia (apenas 'def ...:')
                            end_line = start_line
                        print("Aviso: end_lineno não disponível no nó AST. O fim da função pode ser impreciso.")
                    return node, start_line, end_line
        except SyntaxError as e:
            self.falar(f"Erro de sintaxe no código ao procurar função: {e}" if self.current_language == 'pt-BR' else f"Syntax error in code while searching for function: {e}")
            return None, None, None
        return None, None, None

    def copiar_funcao_codigo(self, func_name, src_filepath, dest_filepath):
        fb = textos_feedback[self.current_language]
        
        src_content_lines = self._ler_arquivo_para_linhas(src_filepath)
        if src_content_lines is None:
            return # Erro já falado

        src_code_string = "\n".join(src_content_lines)
        _, start_line, end_line = self._find_function_node(src_code_string, func_name)

        if start_line is None or end_line is None:
            self.falar(fb['funcao_nao_encontrada'].format(func_name, src_filepath))
            return

        function_code_lines = src_content_lines[start_line - 1 : end_line] # Linhas são 1-based

        try:
            # Adiciona um newline antes se o arquivo de destino não estiver vazio e não terminar com newline
            dest_content_lines = self._ler_arquivo_para_linhas(dest_filepath)
            prefix_lines = []
            if dest_content_lines and dest_content_lines[-1].strip() != "":
                prefix_lines.append("") # Adiciona uma linha em branco como separador

            with open(dest_filepath, "a", encoding="utf-8") as f_dest: # Append mode
                if prefix_lines:
                    for line in prefix_lines:
                        f_dest.write(line + "\n")
                for line in function_code_lines:
                    f_dest.write(line + "\n")
            
            if src_filepath == self.active_file:
                self.falar(fb['funcao_copiada_ativo'].format(func_name, dest_filepath))
            else:
                self.falar(fb['funcao_copiada'].format(func_name, src_filepath, dest_filepath))

        except Exception as e:
            print(f"Erro ao escrever no arquivo de destino {dest_filepath}: {e}")
            self.falar(fb['erro_copiar_funcao'].format(e))


    def deletar_funcao_codigo(self, func_name):
        fb = textos_feedback[self.current_language]
        if not self.active_file:
            self.falar(fb['nenhum_arquivo_aberto'])
            return

        current_code_string = "\n".join(self.file_content_lines)
        _, start_line, end_line = self._find_function_node(current_code_string, func_name)

        if start_line is None or end_line is None:
            self.falar(fb['funcao_nao_encontrada'].format(func_name, self.active_file))
            return

        # Remove as linhas da função
        # As linhas antes da função + as linhas depois da função
        new_content_lines = self.file_content_lines[:start_line - 1] + self.file_content_lines[end_line:]
        self.file_content_lines = new_content_lines
        
        self.falar(fb['funcao_deletada'].format(func_name, self.active_file))
        self.mostrar_codigo_atual() # Mostra o código modificado
        # Opcional: salvar automaticamente? Por enquanto, o usuário precisa salvar.


    def criar_funcao(self, func_name, params_str=""):
        fb = textos_feedback[self.current_language]
        if not self.active_file:
            # Se nenhum arquivo aberto, cria um novo "temporário" ou pede para abrir um
            # Por simplicidade, vamos pedir para abrir um
            self.falar("Por favor, abra um arquivo .py primeiro para criar a função." if self.current_language == 'pt-BR' else "Please open a .py file first to create the function in.")
            # Alternativamente, poderíamos criar um self.active_file = func_name + ".py" e começar do zero.
            return

        # Adiciona uma linha em branco antes da definição da função se o arquivo não estiver vazio
        if self.file_content_lines and self.file_content_lines[-1].strip() != "":
            self.file_content_lines.append("")

        self.file_content_lines.append(f"def {func_name}({params_str}):")
        
        self.escrevendo_corpo_funcao = True
        self.funcao_sendo_escrita_nome = func_name
        self.funcao_sendo_escrita_params = params_str
        
        self.falar(fb['funcao_criada_inicio'].format(func_name, params_str))
        self.mostrar_codigo_atual() # Mostra a definição inicial

    def iniciar(self):
        """Inicia o loop principal do assistente."""
        rodando = True
        while rodando:
            comando_falado = self.ouvir()
            if comando_falado: # Se ouviu algo
                rodando = self.processar_comando(comando_falado)
            # Se não ouviu nada (timeout), apenas continua o loop.
            # Isso é importante para não interromper os modos de escrita contínua.
            if self.escrevendo_continuamente or self.escrevendo_corpo_funcao:
                continue


if __name__ == "__main__":
    # Verifica e baixa recursos do NLTK se necessário
    try:
        nltk.data.find('tokenizers/punkt')
    except (nltk.downloader.DownloadError, LookupError):
        print("Baixando recurso 'punkt' do NLTK...")
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except (nltk.downloader.DownloadError, LookupError):
        print("Baixando recurso 'stopwords' do NLTK...")
        nltk.download('stopwords', quiet=True)

    # Bloco global para armazenar textos de feedback (evitar repetição no processar_comando)
    # Preenchido dentro de __init__ e usado em processar_comando
    textos_feedback = { 
        'pt-BR': {
            'idioma_mudado': "Idioma alterado para {}.", 'ingles': "Inglês", 'portugues': "Português",
            'escrita_cont_on': "Modo de escrita contínua ativado. Diga 'parar de escrever' para finalizar.",
            'escrita_cont_off': "Modo de escrita contínua desativado.", 'linha_adicionada': "Linha adicionada.",
            'linha_adicionada_pos': "Linha adicionada na posição {}.", 'linha_removida': "Linha {} removida: {}",
            'linha_substituida': "Linha {} substituída.", 'texto_substituido': "Texto '{}' substituído por '{}'.",
            'texto_nao_encontrado': "Texto '{}' não encontrado.", 'texto_salvo': "Texto salvo em {}.",
            'texto_limpo': "Texto limpo.", 'arquivo_aberto': "Arquivo {} aberto.",
            'erro_abrir_arquivo': "Erro ao abrir arquivo {}: {}", 'nenhum_arquivo_aberto': "Nenhum arquivo de código aberto.",
            'arquivo_salvo': "Arquivo {} salvo.", 'erro_salvar_arquivo': "Erro ao salvar arquivo {}: {}",
            'arquivo_fechado': "Arquivo {} fechado.", 'funcao_copiada': "Função {} copiada de {} para {}.",
            'funcao_copiada_ativo': "Função {} copiada do arquivo ativo para {}.",
            'erro_copiar_funcao': "Erro ao copiar função: {}.", 'funcao_nao_encontrada': "Função {} não encontrada em {}.",
            'funcao_deletada': "Função {} deletada de {}.", 'erro_deletar_funcao': "Erro ao deletar função: {}.",
            'funcao_criada_inicio': "Criando função {}({}). Dite o corpo da função. Diga 'terminar função' para finalizar.",
            'corpo_funcao_finalizado': "Corpo da função {} finalizado.", 'erro_criar_funcao': "Erro ao criar função: {}.",
            'comando_nao_reconhecido': "Comando não reconhecido.", 'saindo': "Encerrando o assistente. Até logo!",
            'ajuda_geral': "Você pode dizer: {}, {}, {}, ou {}.",
            'ajuda_texto': "'começar a escrever', 'adicionar linha TEXTO', 'deletar linha NUM', 'substituir linha NUM por TEXTO', 'substituir texto ANTIGO por NOVO', 'mostrar texto', 'salvar texto simples NOME_ARQUIVO.txt', 'limpar texto'",
            'ajuda_codigo': "'abrir arquivo NOME.py', 'salvar arquivo de código', 'mostrar código', 'fechar arquivo de código', 'copiar função NOME para ARQUIVO.py', 'deletar função NOME', 'criar função NOME'",
            'ajuda_idioma': "'mudar idioma para inglês/português'", 'ajuda_sair': "'sair'"
        },
        'en-US': { # Preencher com as traduções correspondentes
            'idioma_mudado': "Language changed to {}.", 'ingles': "English", 'portugues': "Portuguese",
            'escrita_cont_on': "Continuous writing mode activated. Say 'stop writing' to finish.",
            'escrita_cont_off': "Continuous writing mode deactivated.", 'linha_adicionada': "Line added.",
            'linha_adicionada_pos': "Line added at position {}.", 'linha_removida': "Line {} removed: {}",
            'linha_substituida': "Line {} replaced.", 'texto_substituido': "Text '{}' replaced with '{}'.",
            'texto_nao_encontrado': "Text '{}' not found.", 'texto_salvo': "Text saved to {}.",
            'texto_limpo': "Text cleared.", 'arquivo_aberto': "File {} opened.",
            'erro_abrir_arquivo': "Error opening file {}: {}", 'nenhum_arquivo_aberto': "No code file is open.",
            'arquivo_salvo': "File {} saved.", 'erro_salvar_arquivo': "Error saving file {}: {}",
            'arquivo_fechado': "File {} closed.", 'funcao_copiada': "Function {} copied from {} to {}.",
            'funcao_copiada_ativo': "Function {} copied from active file to {}.",
            'erro_copiar_funcao': "Error copying function: {}.", 'funcao_nao_encontrada': "Function {} not found in {}.",
            'funcao_deletada': "Function {} deleted from {}.", 'erro_deletar_funcao': "Error deleting function: {}.",
            'funcao_criada_inicio': "Creating function {}({}). Dictate the function body. Say 'end function' to finish.",
            'corpo_funcao_finalizado': "Function body for {} finalized.", 'erro_criar_funcao': "Error creating function: {}.",
            'comando_nao_reconhecido': "Command not recognized.", 'saindo': "Exiting assistant. Goodbye!",
            'ajuda_geral': "You can say: {}, {}, {}, or {}.",
            'ajuda_texto': "'start writing', 'add line TEXT', 'delete line NUM', 'replace line NUM with TEXT', 'replace text OLD with NEW', 'show text', 'save simple text FILENAME.txt', 'clear text'",
            'ajuda_codigo': "'open file NAME.py', 'save code file', 'show code', 'close code file', 'copy function NAME to FILE.py', 'delete function NAME', 'create function NAME'",
            'ajuda_idioma': "'change language to english/portuguese'", 'ajuda_sair': "'exit'"
        }
    }
    
    assistente = None # Inicializa como None para o bloco except
    try:
        assistente = EditorTextoCodigoVoz()
        assistente.iniciar()
    except KeyboardInterrupt:
        print("\nAssistente interrompido pelo usuário.")
        if assistente: assistente.falar(assistente.saudacoes[assistente.current_language].split('.')[0] + " encerrado." if assistente.current_language == 'pt-BR' else "Assistant closed.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado e fatal: {e}")
        if assistente: assistente.falar("Ocorreu um erro crítico e preciso ser encerrado." if assistente.current_language == 'pt-BR' else "A critical error occurred and I need to shut down.")


