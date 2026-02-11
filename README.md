# Clubbi E-commerce API

Uma API B2B de carrinho de compras construída com **FastAPI**, **SQLAlchemy 2.0** e **Pydantic v2**, projetada para gerenciar catálogos de produtos, ofertas personalizadas por cliente e fluxos de checkout simplificados.

---

## 📋 Visão Geral

**Clubbi** é uma plataforma de e-commerce voltada para supermercados e varejistas no Rio de Janeiro. A API permite:

- ✅ Criar e gerenciar carrinhos de compras por cliente
- ✅ Adicionar/remover itens de carrinho com ofertas personalizadas
- ✅ Validar expiração de ofertas e pertencimento de cliente
- ✅ Executar checkout em fluxo linear (OPEN → CHECKOUT → PAID)
- ✅ Registrar pagamentos e gerar histórico de pedidos

---

## 🏗️ Arquitetura

```
├── app/
│   ├── main.py                    # Configuração FastAPI e lifespan
│   ├── exceptions.py              # Exceções de negócio centralizadas
│   ├── db/
│   │   ├── connection.py          # Engine e Session factory
│   │   ├── base.py                # DeclarativeBase do SQLAlchemy
│   │   └── seed_database.py       # Popular DB com dados de exemplo
│   ├── models/                    # Modelos ORM SQLAlchemy
│   │   ├── product.py             # Produto
│   │   ├── client.py              # Cliente (CNPJ, endereço)
│   │   ├── offer.py               # Oferta (preço por cliente + validade)
│   │   ├── cart.py                # Carrinho com estados (OPEN/CHECKOUT/PAID)
│   │   ├── cart_item.py           # Item no carrinho + snapshot de preço
│   │   └── payment.py             # Registro de pagamento
│   ├── schemas/                   # Validação Pydantic (entrada/saída)
│   ├── routers/                   # Endpoints por domínio
│   │   ├── cart_router.py         # CRUD de carrinho
│   │   ├── catalog_router.py      # Consulta de ofertas/produtos
│   │   └── checkout_router.py     # Iniciar checkout e processar pagamento
│   ├── services/                  # Regras de negócio
│   │   ├── cart_service/CartService.py
│   │   └── checkout_service/CheckoutService.py
│   └── dependencies/              # Injeção de dependência (FastAPI)
│
├── docs/
│   └── technical-decisions.md     # Documentação de decisões técnicas
│
├── pyproject.toml                 # Gerenciamento de dependências (Poetry)
├── requirements.txt               # Alternativa (pip)
└── README.md                      # Este arquivo
```

---

## 🔄 Fluxos Principais

### 1. **Criar Carrinho**
```
POST /api/v1/cart/create-cart/{client_id}
↓
CartService.create_cart()
  ├─ Valida se cliente já tem carrinho aberto/em checkout
  ├─ Cria novo Cart com status=OPEN
  └─ Retorna CartSchema
```

### 2. **Adicionar Oferta ao Carrinho**
```
POST /api/v1/cart/{cart_id}/items
├─ Body: { "offer_id": 5, "quantity": 10 }
↓
CartService.add_offer_to_cart()
  ├─ Valida cart (deve estar OPEN)
  ├─ Valida offer (existe, pertence ao cliente, não expirou)
  ├─ Se item já existe no carrinho: incrementa quantidade
  ├─ Se novo: cria CartItem com unit_price_snapshot
  └─ Retorna CartSchema atualizado
```

### 3. **Remover Item do Carrinho**
```
DELETE /api/v1/cart/{cart_id}/items/{cart_item_id}
↓
CartService.remove_offer_from_cart()
  ├─ Valida pertencimento do item ao carrinho
  ├─ Deleta CartItem
  └─ Retorna 204 No Content
```

### 4. **Iniciar Checkout**
```
POST /api/v1/checkout/{cart_id}
↓
CheckoutService.start_checkout()
  ├─ Valida cart (status=OPEN, não vazio)
  ├─ Altera status para CHECKOUT
  └─ Retorna CartSchema
```

### 5. **Finalizar Pagamento**
```
POST /api/v1/checkout/payment/{cart_id}
↓
CheckoutService.finalize_payment()
  ├─ Valida cart (status=CHECKOUT)
  ├─ Calcula total: Σ(quantity × unit_price_snapshot)
  ├─ Cria Payment com status=PAID
  ├─ Altera cart.status para PAID
  └─ Retorna { cart: CartSchema, payment: PaymentSchema }
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|---|---|---|
| **FastAPI** | ≥0.128.6 | Framework HTTP assíncrono, documentação automática |
| **SQLAlchemy** | ≥2.0.46 | ORM com tipagem moderna (`Mapped`, `mapped_column`) |
| **Pydantic** | v2 | Validação de entrada/saída com `from_attributes` |
| **Uvicorn** | ≥0.40.0 | Servidor ASGI |
| **python-dotenv** | ≥1.2.1 | Variáveis de ambiente (`.env`) |
| **Poetry** | — | Gerenciamento de dependências |

---

## 🚀 Como Rodar Localmente

### 1. **Pré-requisitos**
- Python ≥ 3.11
- Poetry (recomendado) ou pip
- SQLite (padrão) ou PostgreSQL/MySQL

### 2. **Clonar e Instalar Dependências**

```bash
# Clone o repositório (ou descompacte)
cd clubbi-case

# Instale com Poetry
poetry install

# Ou com pip
pip install -r requirements.txt
```

### 3. **Configurar Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto:

```env
# SQLite (desenvolvimento)
DATA_BASE_URL=sqlite:///./dev.db

# PostgreSQL (opcional)
# DATA_BASE_URL=postgresql://usuario:senha@localhost:5432/clubbi
```

### 4. **Popular Banco com Dados de Exemplo**

```bash
poetry run python -m app.db.seed_database
# ou
python -m app.db.seed_database
```

Isso cria:
- 25 produtos (arroz, feijão, bebidas, higiene, etc.)
- 10 clientes (supermercados do RJ)
- ~150 ofertas personalizadas por cliente

### 5. **Rodar a Aplicação**

```bash
poetry run uvicorn app.main:app --reload

# ou direto
uvicorn app.main:app --reload
```

A API estará disponível em:
- **API**: http://localhost:8000
- **Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📊 Exemplos de Requisições

### Criar um carrinho
```bash
curl -X POST "http://localhost:8000/api/v1/cart/create-cart/1" \
  -H "Content-Type: application/json"
```

**Resposta:**
```json
{
  "id": 1,
  "client_id": 1,
  "status": "open",
  "created_at": "2026-02-11T10:00:00Z",
  "items": []
}
```

### Adicionar oferta ao carrinho
```bash
curl -X POST "http://localhost:8000/api/v1/cart/1/items" \
  -H "Content-Type: application/json" \
  -d '{"offer_id": 5, "quantity": 10}'
```

### Iniciar checkout
```bash
curl -X POST "http://localhost:8000/api/v1/checkout/1"
```

### Finalizar pagamento
```bash
curl -X POST "http://localhost:8000/api/v1/checkout/payment/1"
```

---

## 🔐 Tratamento de Erros

Todas as exceções de negócio retornam `JSONResponse` com status HTTP e mensagem clara:

```json
{
  "error": "CartNotFoundError",
  "detail": "Cart with id 999 not found."
}
```

**Exceções principais:**
- `CartAlreadyExistsError` (400) — Cliente já tem carrinho aberto
- `CartNotFoundError` (404) — Carrinho não encontrado
- `CartIsEmptyError` (400) — Carrinho vazio para checkout
- `OfferNotFoundError` (404) — Oferta não existe
- `ExpiredOfferError` (400) — Oferta expirou
- `OfferDoesNotBelongToClientError` (403) — Oferta não pertence ao cliente

---

## 💾 Modelo de Dados

### Clientes (`customers`)
```
id (PK), name, cnpj (UNIQUE), address
```

### Produtos (`products`)
```
id (PK), ean (UNIQUE), name, items_per_box
```

### Ofertas (`offers`)
```
id (PK), client_id (FK), product_id (FK), unit_price (Decimal), valid_until (Date)
```

### Carrinhos (`carts`)
```
id (PK), client_id (FK), status (Enum: open|checkout|paid), created_at
```

### Itens de Carrinho (`cart_items`)
```
id (PK), cart_id (FK), offer_id (FK), quantity, unit_price_snapshot (Decimal)
```

### Pagamentos (`payments`)
```
id (PK), cart_id (FK), status (Enum: paid), amount (Decimal), created_at
```

---

## 🔍 Decisões Técnicas Importantes

Para detalhes sobre arquitetura, padrões e recomendações, consulte **[docs/technical-decisions.md](docs/technical-decisions.md)**.

Resumo:
- ✅ Uso de `Decimal` para precisão monetária
- ✅ Snapshot de preço em `CartItem` para histórico
- ✅ Estados de carrinho explícitos (OPEN/CHECKOUT/PAID)
- ✅ Exceções centralizadas com mapeamento HTTP automático
- ⚠️ Falta de locks para concorrência (considerar `SELECT ... FOR UPDATE`)

---

## 📝 Estrutura de Projeto com Poetry

```toml
[project]
name = "clubbi-case"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi (>=0.128.6,<0.129.0)",
    "sqlalchemy (>=2.0.46,<3.0.0)",
    "uvicorn (>=0.40.0,<0.41.0)",
    "python-dotenv (>=1.2.1,<2.0.0)"
]
```

---

## 🧪 Testes (Futuro)

Sugestão de estrutura para testes:
```
tests/
├── conftest.py              # Fixtures (DB em memória, sessão, etc)
├── unit/
│   ├── test_cart_service.py
│   └── test_checkout_service.py
└── integration/
    └── test_api_endpoints.py
```

Comando sugerido:
```bash
poetry add --group dev pytest pytest-asyncio httpx
poetry run pytest tests/ -v
```

---

## 📚 Documentação Adicional

- **Swagger (Interativo)**: http://localhost:8000/docs
- **ReDoc (Estático)**: http://localhost:8000/redoc
- **Decisões Técnicas**: [docs/technical-decisions.md](docs/technical-decisions.md)

---

## 👨‍💻 Autor

**Joao Ribeiro** — joao.ribeiro@e-deploy.com.br

---

## 📄 Licença

Este projeto é fornecido como está, sem licença específica.

---

**Última atualização:** 11 de fevereiro de 2026
