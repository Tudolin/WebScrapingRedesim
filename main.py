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

def encontrar_status_por_texto(soup, texto_licenca):
    """
    Encontra o status de uma licença dado o texto da licença.

    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup da página HTML.
        texto_licenca (str): Texto da licença a ser encontrada.

    Returns:
        str: Status da licença ou None se não encontrado.
    """
    # Encontra o elemento que contém o texto da licença
    licenca_element = soup.find(string=texto_licenca)
    if not licenca_element:
        return None

    # Assume que o status está em um elemento próximo. Ajuste conforme a estrutura real.
    # Por exemplo, se o status estiver em um <span> logo após o texto da licença:
    parent = licenca_element.find_parent()
    if not parent:
        return None

    # Tenta encontrar um elemento <span> que contenha o status
    status_element = parent.find_next_sibling("span")
    if status_element:
        return status_element.get_text(strip=True)

    # Alternativamente, se o status estiver dentro do mesmo elemento pai
    status_element = parent.find("span")
    if status_element:
        return status_element.get_text(strip=True)

    return None
    
def consulta_redesim(n_protocolo):
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
        url = f"https://redesim.curitiba.pr.gov.br/licenciamento/{n_protocolo}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Verifica se a resposta contém informações válidas
        if not soup or 'Nenhuma informação encontrada' in response.text:
            raise ValueError(f"No valid data found for protocol {n_protocolo}")

        # Informações Adicionais - Secretaria Municipal do Meio Ambiente
        resultados["Secretaria Municipal do Meio Ambiente"]["Informações Adicionais"] = encontrar_elemento_com_multiplos_select(
            soup, ['#frmOrgao\\:j_idt75', '#frmOrgao\\:j_idt74', '#frmOrgao\\:j_idt76']
        )

        # Secretaria Municipal do Meio Ambiente - Documentos
        resultados["Secretaria Municipal do Meio Ambiente"]["Documentos"]["Licença Ambiental Prévia"] = encontrar_status_por_texto(
            soup, "Licença Ambiental Prévia"
        )
        
        resultados["Secretaria Municipal do Meio Ambiente"]["Documentos"]["Licença Ambiental de Instalação"] = encontrar_status_por_texto(
            soup, "Licença Ambiental de Instalação"
        )
        
        resultados["Secretaria Municipal do Meio Ambiente"]["Documentos"]["Licença Ambiental de Operação"] = encontrar_status_por_texto(
            soup, "Licença Ambiental de Operação"
        )

        # Vigilância Sanitária - Informações Adicionais
        resultados["Vigilância Sanitária"]["Informações Adicionais"] = encontrar_elemento_com_multiplos_select(
            soup, ['#j_idt163\\:j_idt168', '#j_idt163\\:j_idt169', '#j_idt163\\:j_idt190']
        )

        # Vigilância Sanitária - Documentos
        resultados["Vigilância Sanitária"]["Documentos"]["Análise de Projeto Arquitetônico"] = encontrar_status_por_texto(
            soup, "Análise de Projeto Arquitetônico"
        )
        
        resultados["Vigilância Sanitária"]["Documentos"]["Declaração de Dispensa de Licenciamento Sanitário"] = encontrar_status_por_texto(
            soup, "Declaração de Dispensa de Licenciamento Sanitário"
        )
        
        resultados["Vigilância Sanitária"]["Documentos"]["Licença Sanitária Simplificada"] = encontrar_status_por_texto(
            soup, "Licença Sanitária Simplificada"
        )

        # Secretaria Municipal de Finanças - Informações Adicionais
        resultados["Secretaria Municipal de Finanças"]["Informações Adicionais"] = encontrar_elemento_com_multiplos_select(
            soup, ['#frmOrgao\\:j_idt257\\:j_idt258', '#frmOrgao\\:j_idt257\\:j_idt259', '#frmOrgao\\:j_idt257\\:j_idt260']
        )

        # Secretaria Municipal de Finanças - Documentos
        resultados["Secretaria Municipal de Finanças"]["Documentos"]["Inscrição Municipal"] = encontrar_status_por_texto(
            soup, "Inscrição Municipal"
        )
        
        resultados["Secretaria Municipal de Finanças"]["Documentos"]["Alvará de Licença de Localização"] = encontrar_status_por_texto(
            soup, "Alvará de Licença de Localização"
        )

        # Verifica se ao menos uma licença ambiental foi encontrada
        if not resultados["Secretaria Municipal do Meio Ambiente"]["Documentos"]["Licença Ambiental Prévia"] and \
           not resultados["Secretaria Municipal do Meio Ambiente"]["Documentos"]["Licença Ambiental de Instalação"] and \
           not resultados["Secretaria Municipal do Meio Ambiente"]["Documentos"]["Licença Ambiental de Operação"]:
            raise ValueError(f"Incomplete data for protocol {n_protocolo}")
        
    except Exception as e:
        print(f"Erro ao consultar protocolo {n_protocolo}: {e}")
        return None
    
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
