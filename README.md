# Web Scraping Redesim

![Badge GCP](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Badge Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)

## Índice
* [Introdução](#introdução)
* [Instalação de Dependências](#instalação-de-dependências)
* [Estrutura do Código](#estrutura-do-código)
* [Variáveis](#variáveis)
* [Configuração do Ambiente](#configuração-do-ambiente)
* [Execução da Aplicação](#execução-da-aplicação)

## Introdução

Este projeto realiza web scraping do site [Redesim](https://redesim.curitiba.pr.gov.br/licenciamento/), extraindo informações de protocolos para monitoramento de licenças. A aplicação utiliza a API do Firebase para armazenar os resultados, e notifica automaticamente por e-mail quando há mudanças nos dados de um protocolo.

## Instalação de Dependências

> pip install -r requirements.txt

As dependências do projeto incluem:
- `firebase-admin`: Para integração com o Firebase.
- `beautifulsoup4` e `requests`: Para realizar o web scraping.
- `smtplib`: Para envio de e-mails de notificação.

## Estrutura do Código

O código está dividido da seguinte forma:

### Arquivos principais:
- **`main.py`**: 
    - Contém a lógica de conexão ao Firebase, consulta dos protocolos no site da Redesim, processamento dos dados e armazenamento dos resultados no banco de dados.
    - Orquestra o fluxo de execução de todo o processo de scraping e comparação de dados.

- **`mensagem.py`**:
    - Responsável pelo envio de notificações por e-mail, formatando a mensagem com base nas mudanças de status de cada protocolo e enviando para o destinatário definido.

### Funções importantes:

- **`connection_fb(collection_name)`** (em `main.py`): Conecta a uma coleção específica no Firebase Firestore.
  
- **`consulta_redesim(n_protocolo)`** (em `main.py`): Realiza o scraping do site da Redesim, buscando dados relacionados ao protocolo fornecido, como licenças ambientais, sanitárias e informações fiscais.
  
- **`process_event(event, context)`** (em `main.py`): Função principal que processa os dados do Firebase, executa a consulta de cada protocolo, compara os dados com versões anteriores e atualiza o banco. Caso haja mudanças, aciona o envio de notificações.
  
- **`enviar_email(para, assunto, mensagem)`** (em `mensagem.py`): Envia e-mails de notificação com base nas mudanças detectadas.

- **`formatar_mensagem_alterada(status_anteriores, novos_status)`** (em `mensagem.py`): Formata a mensagem do e-mail que será enviada, listando todas as mudanças de status dos documentos e apresentando uma tabela de comparação.

- **`enviar_notificacao(time, n_protocolo, dados_anteriores, novos_dados)`** (em `mensagem.py`): Prepara o conteúdo do e-mail e aciona o envio ao destinatário com as informações de alteração.

## Variáveis

As variáveis principais incluem:
- **Chave de API do Firebase**: Usada para autenticar e se conectar ao banco de dados Firestore.
- **Credenciais do Mailjet** (ou outro serviço SMTP): Para envio de notificações por e-mail.

Essas variáveis devem ser definidas e configuradas no ambiente antes de executar o código.

## Configuração do Ambiente

1. **Firebase**: Conecte a aplicação ao Firebase Firestore para armazenar e consultar os dados. Configure as permissões corretas no Google Cloud para acessar o Firestore.
   
2. **Mailjet ou outro serviço SMTP**: Configure suas credenciais para o envio de e-mails (API Key e Secret Key).
   
3. **Pub/Sub e Cloud Scheduler**: Configure o Pub/Sub no Google Cloud para disparar eventos automaticamente e o Cloud Scheduler para definir a periodicidade de execução do scraping.

4. **Cloud Storage**: Configure um bucket para armazenar backups ou logs, se necessário.

## Execução da Aplicação

Para rodar o código localmente:

```bash
python main.py(None, None)
