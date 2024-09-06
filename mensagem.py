import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviar_email(para, assunto, mensagem):
    """
    Envia um e-mail utilizando o serviço SMTP, neste exemplo o Mailjet.

    Args:
        para (str): Endereço de e-mail do destinatário.
        assunto (str): Assunto do e-mail.
        mensagem (str): Corpo do e-mail no formato HTML.

    Returns:
        None: A função imprime uma mensagem de sucesso ou falha na operação.
    """
    de = 'seuemail@email.com'
    api_key = 'chave-de-api'
    secret_key = 'secret-key'

    # Criação da estrutura do e-mail
    msg = MIMEMultipart()
    msg['From'] = de
    msg['To'] = para
    msg['Subject'] = assunto

    # Adiciona a mensagem ao corpo do e-mail no formato HTML
    msg.attach(MIMEText(mensagem, 'html'))

    try:
        # Configuração do servidor SMTP
        server = smtplib.SMTP('in-v3.mailjet.com', 587)  # Utilizando o serviço Mailjet
        server.starttls()  # Inicia a conexão segura
        server.login(api_key, secret_key)  # Faz o login no servidor SMTP com a API key
        texto = msg.as_string()
        server.sendmail(de, para, texto)  # Envia o e-mail
        server.quit()  # Fecha a conexão
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Falha ao enviar email: {e}")


def formatar_mensagem_alterada(status_anteriores, novos_status):
    """
    Formata a mensagem HTML que será enviada por e-mail, contendo as mudanças de status de um protocolo.

    Args:
        status_anteriores (dict): Dicionário com os status anteriores dos documentos.
        novos_status (dict): Dicionário com os novos status dos documentos.

    Returns:
        str: String HTML formatada contendo as informações das alterações nos status.
    """
    mensagem = """
    <html>
    <body>
    <p>*Esta mensagem é gerada automaticamente, favor não responder*</p><br><br>
    <h2>Atualização no status do protocolo</h2>
    <p>Os seguintes status foram alterados:</p>
    <table border="1" style="width:100%; border-collapse: collapse;">
        <tr>
            <th>Departamento</th>
            <th>Seção</th>
            <th>Documento</th>
            <th>Status Anterior</th>
            <th>Novo Status</th>
        </tr>
    """
    # Itera sobre os status anteriores para comparar com os novos status
    for departamento, detalhes in status_anteriores.items():
        for secao, conteudo in detalhes.items():
            if isinstance(conteudo, dict):
                for documento, status in conteudo.items():
                    novo_status = novos_status.get(departamento, {}).get(secao, {}).get(documento)

                    # Verifica se há mudanças nos status
                    if novo_status is not None and status != novo_status:
                        cor = "red" if "Em Exigência" in novo_status or "None" in novo_status else "green" if "Emitido" in novo_status else "blue"
                        mensagem += f"""
                        <tr>
                            <td>{departamento}</td>
                            <td>{secao}</td>
                            <td>{documento}</td>
                            <td style="text-align:center;">{status}</td>
                            <td style="text-align:center; color: {cor};">{novo_status}</td>
                        </tr>
                        """
            else:
                print(f"'{secao}' em '{departamento}' não é um dicionário. Conteúdo: {conteudo}")

    mensagem += """
    </table>
    </body>
    </html>
    """
    return mensagem


def enviar_notificacao(time, n_protocolo, dados_anteriores, novos_dados):
    """
    Envia uma notificação por e-mail quando houver alterações no status de um protocolo.

    Args:
        time (str): Nome do time ou entidade responsável pelo protocolo.
        n_protocolo (str): Número do protocolo.
        dados_anteriores (dict): Status anteriores do protocolo.
        novos_dados (dict): Novos status atualizados do protocolo.

    Returns:
        None: A função envia um e-mail e imprime informações sobre o envio.
    """
    assunto = f"Atualização no status do protocolo {n_protocolo}"
    mensagem = f"""
    <p>O status do protocolo <a href="https://redesim.curitiba.pr.gov.br/licenciamento/{n_protocolo}">
    https://redesim.curitiba.pr.gov.br/licenciamento/{n_protocolo}</a> do {time} foi alterado.</p>
    """
    mensagem += formatar_mensagem_alterada(dados_anteriores, novos_dados)

    # Define o destinatário do e-mail
    email_destinatario = 'emaildestinatario@gmail.com'
    print(f"Enviando e-mail para {email_destinatario} com assunto '{assunto}' e mensagem:\n{mensagem}")

    # Envia o e-mail
    enviar_email(email_destinatario, assunto, mensagem)
