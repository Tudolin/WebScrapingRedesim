import firebase_admin
import requests
from bs4 import BeautifulSoup
from firebase_admin import credentials, firestore

# Inicialização da credencial Firebase
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

# Conexão com o Firestore
db = firestore.client()

def connection_fb(collection_name):
    """
    Realiza a conexão com uma coleção no banco de dados Firebase Firestore.

    Args:
        collection_name (str): Nome da coleção no Firestore.

    Returns:
        firestore.CollectionReference: Referência para a coleção especificada.
    """
    return db.collection(collection_name)

def encontrar_elemento_com_multiplos_select(soup, selectors):
    """
    Encontra e retorna o texto de um elemento HTML baseado em múltiplos seletores CSS.

    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup contendo o HTML a ser analisado.
        selectors (list): Lista de seletores CSS para tentar encontrar o elemento.

    Returns:
        str: Texto do primeiro elemento encontrado que corresponda aos seletores fornecidos. 
        Retorna None se nenhum elemento for encontrado.
    """
    for selector in selectors:
        elemento = soup.select_one(selector)
        if elemento:
            return elemento.get_text(strip=True)
    return None

def consulta_redesim(n_protocolo):
    """
    Realiza a consulta no site da Redesim usando o número de protocolo fornecido e extrai informações dos status dos processos.

    Args:
        n_protocolo (str): Número de protocolo usado para consulta no site da Redesim.

    Returns:
        dict: Dicionário contendo os resultados da consulta, organizados por órgãos e documentos encontrados.
    """
    url = f"https://redesim.curitiba.pr.gov.br/licenciamento/{n_protocolo}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Estrutura inicial de resultados
    resultados = {
        "Secretaria Municipal do Meio Ambiente": {
            "Informações Adicionais": "",
            "Documentos": {
                "Licença Ambiental Prévia": None,
                "Licença Ambiental de Instalação": None,
                "Licença Ambiental de Operação": None,
            }
        },
        "Vigilância Sanitária": {
            "Informações Adicionais": "",
            "Documentos": {
                "Análise de Projeto Arquitetônico": None,
                "Declaração de Dispensa de Licenciamento Sanitário": None,
                "Licença Sanitária Simplificada": None
            }
        },
        "Secretaria Municipal de Finanças": {
            "Informações Adicionais": "",
            "Documentos": {
                "Inscrição Municipal": None,
                "Alvará de Licença de Localização": None
            }
        }
    }
    
    try:
        # Coleta de informações da Secretaria Municipal do Meio Ambiente
        resultados["Secretaria Municipal do Meio Ambiente"]["Informações Adicionais"] = encontrar_elemento_com_multiplos_select(soup, ['#frmOrgao\\:j_idt75', '#frmOrgao\\:j_idt74', '#frmOrgao\\:j_idt76'])

        # Verificação e extração de licenças ambientais
        licenca_previa = soup.find(string="Licença Ambiental Prévia")
        licenca_instalacao = soup.find(string="Licença Ambiental de Instalação")
        licenca_operacao = soup.find(string="Licença Ambiental de Operação")

        if licenca_previa:
            resultados["Secretaria Municipal do Meio Ambiente"]["Documentos"]["Licença Ambiental Prévia"] = encontrar_elemento_com_multiplos_select(soup, [
                '#frmOrgao\\:j_idt81\\:0\\:j_idt86', '#frmOrgao\\:j_idt81\\:0\\:j_idt87',
                '#frmOrgao\\:j_idt81\\:0\\:j_idt88', '#frmOrgao\\:j_idt81\\:0\\:j_idt89',
                '#frmOrgao\\:j_idt81\\:0\\:j_idt90'
            ])
        
        if licenca_instalacao:
            resultados["Secretaria Municipal do Meio Ambiente"]["Documentos"]["Licença Ambiental de Instalação"] = encontrar_elemento_com_multiplos_select(soup, [
                '#frmOrgao\\:j_idt81\\:1\\:j_idt86', '#frmOrgao\\:j_idt81\\:1\\:j_idt87',
                '#frmOrgao\\:j_idt81\\:1\\:j_idt88', '#frmOrgao\\:j_idt81\\:1\\:j_idt89',
                '#frmOrgao\\:j_idt81\\:1\\:j_idt90'
            ])
        
        if not licenca_instalacao and licenca_operacao:
            resultados["Secretaria Municipal do Meio Ambiente"]["Documentos"]["Licença Ambiental de Operação"] = encontrar_elemento_com_multiplos_select(soup, [
                '#frmOrgao\\:j_idt81\\:1\\:j_idt86', '#frmOrgao\\:j_idt81\\:1\\:j_idt87',
                '#frmOrgao\\:j_idt81\\:1\\:j_idt88', '#frmOrgao\\:j_idt81\\:1\\:j_idt89',
                '#frmOrgao\\:j_idt81\\:1\\:j_idt90'
            ])
        elif licenca_operacao:
            resultados["Secretaria Municipal do Meio Ambiente"]["Documentos"]["Licença Ambiental de Operação"] = encontrar_elemento_com_multiplos_select(soup, [
                '#frmOrgao\\:j_idt81\\:2\\:j_idt86', '#frmOrgao\\:j_idt81\\:2\\:j_idt87',
                '#frmOrgao\\:j_idt81\\:2\\:j_idt88', '#frmOrgao\\:j_idt81\\:2\\:j_idt89',
                '#frmOrgao\\:j_idt81\\:2\\:j_idt90'
            ])

        # Coleta de informações da Vigilância Sanitária
        resultados["Vigilância Sanitária"]["Informações Adicionais"] = encontrar_elemento_com_multiplos_select(soup, ['#j_idt163\\:j_idt168', '#j_idt163\\:j_idt169', '#j_idt163\\:j_idt190'])

        analise_projeto = soup.find(string="Análise de Projeto Arquitetônico")
        declaracao_dispensacao = soup.find(string="Declaração de Dispensa de Licenciamento Sanitário")
        licenca_sanit_sim = soup.find(string="Licença Sanitária Simplificada")
        
        if analise_projeto:
            resultados["Vigilância Sanitária"]["Documentos"]["Análise de Projeto Arquitetônico"] = encontrar_elemento_com_multiplos_select(soup, [
                '#j_idt163\\:j_idt175\\:0\\:j_idt180', '#j_idt163\\:j_idt175\\:0\\:j_idt194',
                '#j_idt163\\:j_idt175\\:0\\:j_idt195', '#j_idt163\\:j_idt175\\:0\\:j_idt196',
                '#j_idt163\\:j_idt175\\:0\\:j_idt197', '#j_idt163\\:j_idt175\\:0\\:j_idt198'
            ])
        
        if declaracao_dispensacao:
            resultados["Vigilância Sanitária"]["Documentos"]["Declaração de Dispensa de Licenciamento Sanitário"] = encontrar_elemento_com_multiplos_select(soup, [
                '#j_idt163\\:j_idt175\\:1\\:j_idt178', '#j_idt163\\:j_idt175\\:1\\:j_idt179',
                '#j_idt163\\:j_idt175\\:1\\:j_idt180', '#j_idt163\\:j_idt175\\:1\\:j_idt181',
                '#j_idt163\\:j_idt175\\:1\\:j_idt182'
            ])

        if licenca_sanit_sim:
            resultados["Vigilância Sanitária"]["Documentos"]["Licença Sanitária Simplificada"] = encontrar_elemento_com_multiplos_select(soup, [
                '#j_idt163\\:j_idt175\\:0\\:j_idt178', '#j_idt163\\:j_idt175\\:0\\:j_idt179',
                '#j_idt163\\:j_idt175\\:0\\:j_idt180', '#j_idt163\\:j_idt175\\:0\\:j_idt181',
                '#j_idt163\\:j_idt175\\:0\\:j_idt182'
            ])
        
        # Coleta de informações da Secretaria Municipal de Finanças
        resultados["Secretaria Municipal de Finanças"]["Informações Adicionais"] = encontrar_elemento_com_multiplos_select(soup, ['#frmOrgao\\:j_idt257\\:j_idt258', '#frmOrgao\\:j_idt257\\:j_idt259', '#frmOrgao\\:j_idt257\\:j_idt260'])

        inscricao_municipal = soup.find(string="Inscrição Municipal")
        alvara_localizacao = soup.find(string="Alvará de Licença de Localização")
        
        if inscricao_municipal:
            resultados["Secretaria Municipal de Finanças"]["Documentos"]["Inscrição Municipal"] = encontrar_elemento_com_multiplos_select(soup, [
                '#j_idt257\\:j_idt269\\:0\\:j_idt275', '#j_idt257\\:j_idt269\\:0\\:j_idt276',
                '#j_idt257\\:j_idt269\\:0\\:j_idt277', '#j_idt257\\:j_idt269\\:0\\:j_idt278'
            ])
        
        if alvara_localizacao:
            resultados["Secretaria Municipal de Finanças"]["Documentos"]["Alvará de Licença de Localização"] = encontrar_elemento_com_multiplos_select(soup, [
                '#j_idt257\\:j_idt269\\:1\\:j_idt280', '#j_idt257\\:j_idt269\\:1\\:j_idt279',
                '#j_idt257\\:j_idt269\\:1\\:j_idt278', '#j_idt257\\:j_idt269\\:1\\:j_idt277',
                '#j_idt257\\:j_idt269\\:1\\:j_idt276'
            ])
        
    except Exception as e:
        print(f"Erro ao consultar protocolo {n_protocolo}: {e}")
    
    return resultados

def process_event(event, context):
    """
    Ponto de entrada que deve ser configurada no cloud Functions.
    Processa eventos automáticos de consulta à Redesim, extrai dados e os salva no Firestore.

    Args:
        event (dict): Evento de disparo automático (não utilizado diretamente).
        context (dict): Contexto de execução do evento (não utilizado diretamente).

    Returns:
        str: Mensagem de conclusão do processo.
    """
    cadastros_collection = connection_fb('redesim_cadastros')
    resultados_collection = connection_fb('redesim_resultados')
    
    cadastros = [doc.to_dict() for doc in cadastros_collection.stream()]

    for cadastro in cadastros:
        time = cadastro['name_team']
        n_protocolo = cadastro['n_protocolo']
        nome = cadastro['nome']
        print(f"Consultando Redesim para {nome} - Protocolo: {n_protocolo}")
        novos_resultados = consulta_redesim(n_protocolo)

        doc_ref = resultados_collection.document(f"{time}_{n_protocolo}")
        doc = doc_ref.get()
        
        if doc.exists:
            dados_anteriores = doc.to_dict().get('dados')
        else:
            dados_anteriores = None
        
        doc_ref.set({
            "time": time,
            "n_protocolo": n_protocolo,
            "dados": novos_resultados,
            "dados_anteriores": dados_anteriores
        }, merge=True)

        # Verifica se houve mudança nos status e aciona o envio de mensagem
        if dados_anteriores and dados_anteriores != novos_resultados:
            from mensagem import enviar_notificacao
            print(f"Notificação para {nome} - Protocolo: {n_protocolo}")
            print(f"Dados Anteriores: {dados_anteriores}")
            print(f"Novos Dados: {novos_resultados}")
            enviar_notificacao(time, n_protocolo, dados_anteriores, novos_resultados)
    
    return 'Process completed successfully'

# Execução do processo localmente
# process_event(None, None)
