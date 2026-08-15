from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import hashlib

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="API Raízes do Nordeste",
    description="Backend para APP de pedidos, multicanalidade e autenticação",
    version="1.0.0"
)

# BANCO DE DADOS
banco_usuarios = []
banco_pedidos = []
contador_pedido_id = 1

# DADOS

class UsuarioCadastro(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cpf: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class ItemPedido(BaseModel):
    produto: str
    quantidade: int
    preco_unitario: float

class NovoPedido(BaseModel):
    id_cliente: int
    canalPedido: str  # APP/TOTEM/BALCAO
    itens: List[ItemPedido]

class PagamentoSimulacao(BaseModel):
    id_pedido: int
    metodo: str  # PIX, CREDITO, DEBITO


# ROTAS DA API 

@app.get("/")
def inicio():
    """Rota inicial de boas-vindas."""
    return {"mensagem": "Bem-vindo à API do Raízes do Nordeste!"}


@app.post("/usuarios/cadastrar", status_code=201)
def cadastrar_usuario(usuario: UsuarioCadastro):
    """
    [RF06, RNF01, RNF03] Cadastra um novo cliente com hash de senha SHA-256 (Segurança e LGPD).
    """
    # Criptografa a senha (Hash SHA-256 / RNF01 - Segurança)
    senha_hash = hashlib.sha256(usuario.senha.encode()).hexdigest()
    
    novo_usuario = {
        "id": len(banco_usuarios) + 1,
        "nome": usuario.nome,
        "email": usuario.email,
        "cpf": usuario.cpf,
        "senha_hash": senha_hash
    }
    
    banco_usuarios.append(novo_usuario)
    return {"mensagem": "Usuário cadastrado com sucesso!", "usuario_id": novo_usuario["id"]}

@app.post("/usuarios/login")
def login(dados: UsuarioLogin):
    """
    [RF06, RNF02] Realiza a autenticação e gera um Token de Acesso simulação de JWT.
    """
    # Gera o hash da senha enviada para comparar com o banco
    senha_hash = hashlib.sha256(dados.senha.encode()).hexdigest()
    
    # Busca o usuário pelo email e hash da senha
    usuario = next((u for u in banco_usuarios if u["email"] == dados.email and u["senha_hash"] == senha_hash), None)
    
    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")
    
    # Gera um token
    token_simulado = f"bearer-token-usuario-{usuario['id']}-autenticado"
    
    return {
        "mensagem": "Login realizado com sucesso!",
        "token_acesso": token_simulado,
        "tipo_token": "Bearer"
    }

@app.post("/pedidos", status_code=201)
def criar_pedido(pedido: NovoPedido):
    """
    [RF01, RF03] Cria um novo pedido registrando obrigatoriamente o canalPedido.
    """
    global contador_pedido_id
    
    # Valida se informou o canal do pedido
    if not pedido.canalPedido:
        raise HTTPException(status_code=400, detail="O campo canalPedido é obrigatório.")
    
    # Calcula o valor total
    valor_total = sum(item.quantidade * item.preco_unitario for item in pedido.itens)
    
    novo_registro = {
        "id_pedido": contador_pedido_id,
        "id_cliente": pedido.id_cliente,
        "canalPedido": pedido.canalPedido.upper(), 
        "itens": pedido.itens,
        "valor_total": valor_total,
        "status": "RECEBIDO",
        "pago": False,
        "data_criacao": datetime.now().isoformat()
    }
    
    banco_pedidos.append(novo_registro)
    contador_pedido_id += 1
    
    return {
        "mensagem": "Pedido criado com sucesso!",
        "pedido": novo_registro
    }


@app.post("/pedidos/pagamento")
def simular_pagamento(pagamento: PagamentoSimulacao):
    """
    [RF04, RF05] Simula o pagamento e atualiza o status do pedido.
    """
    # Busca o pedido
    pedido = next((p for p in banco_pedidos if p["id_pedido"] == pagamento.id_pedido), None)
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    
    # Atualiza o status do pedido após "pagamento aprovado"
    pedido["pago"] = True
    pedido["status"] = "EM_PREPARACAO"
    
    return {
        "mensagem": "Pagamento aprovado com sucesso!",
        "id_pedido": pedido["id_pedido"],
        "metodo_utilizado": pagamento.metodo,
        "novo_status": pedido["status"]
    }


@app.get("/pedidos/{id_pedido}")
def consultar_status_pedido(id_pedido: int):
    """
    [RF05] Permite acompanhar o status do pedido.
    """
    pedido = next((p for p in banco_pedidos if p["id_pedido"] == id_pedido), None)
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    
    return {
        "id_pedido": pedido["id_pedido"],
        "canalPedido": pedido["canalPedido"],
        "status": pedido["status"],
        "valor_total": pedido["valor_total"],
        "pago": pedido["pago"]
    }