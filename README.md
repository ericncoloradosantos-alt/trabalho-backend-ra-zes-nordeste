    API Raízes do Nordeste – Backend da Lanchonete:

Este projeto apresenta a API RESTful desenvolvida para o APP de gerenciamento de pedidos da lanchonete Raízes do Nordeste. A aplicação foi criada para atender às principais necessidades do sistema, como cadastro de clientes, login de usuários, registro de pedidos por diferentes canais e simulação de pagamentos.

    Tecnologias Utilizadas:

Para o desenvolvimento da API, foram utilizadas tecnologias que facilitam a criação, execução e organização do backend:

Linguagem: Python 3.14.7
Framework: FastAPI
Servidor Web: Uvicorn
Validação de dados: Pydantic e Email-Validator
Segurança: Hash de senhas utilizando SHA-256 e autenticação por Bearer Token
Documentação: Swagger UI / OpenAPI, gerada automaticamente pelo FastAPI

    Como Executar o Projeto Localmente:
1. Pré-requisitos

Antes de iniciar o projeto, é necessário ter o Python 3.14.7 instalado no computador e configurado corretamente para ser utilizado pelo terminal.

2. Instalação das Dependências

Com o terminal aberto dentro da pasta do projeto, execute o comando abaixo para instalar as bibliotecas necessárias:

pip install fastapi uvicorn pydantic email-validator

3. Inicialização do Servidor

Depois que as dependências forem instaladas, a API pode ser iniciada em modo de desenvolvimento com o seguinte comando:

python -m uvicorn app.main:app --reload

Após a inicialização, o servidor estará disponível localmente no endereço:

http://127.0.0.1:8000

    Documentação Interativa – Swagger UI:

O FastAPI disponibiliza automaticamente uma documentação interativa da API por meio do Swagger UI. Depois de iniciar o servidor, basta acessar o endereço abaixo pelo navegador:

http://127.0.0.1:8000/docs

Por meio dessa página, é possível visualizar os endpoints disponíveis, consultar os parâmetros necessários e realizar testes diretamente na API.

    Principais Endpoints da API:

A API possui alguns endpoints principais responsáveis pelas funcionalidades do sistema:

POST /usuarios/cadastrar – Realiza o cadastro de um novo cliente e armazena sua senha utilizando hash SHA-256, contribuindo para a proteção das credenciais.
POST /usuarios/login – Verifica as credenciais do usuário e gera um token de acesso para autenticação.
POST /pedidos – Registra um novo pedido e identifica o canal utilizado pelo cliente, podendo ser TOTEM, APP ou BALCÃO.
POST /pedidos/pagamento – Realiza a simulação do pagamento, com opções como PIX e cartão, e atualiza o pedido para o status EM_PREPARAÇÃO após o processamento.
GET /pedidos/{id_pedido} – Permite consultar um pedido específico e verificar seu status atualizado.

Com essas funcionalidades, a API oferece uma estrutura básica para o gerenciamento dos pedidos da Raízes do Nordeste, permitindo integrar diferentes canais de atendimento e organizar as principais etapas do processo, desde o cadastro do cliente até o acompanhamento do pedido.