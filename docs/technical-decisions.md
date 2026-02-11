**Visão Geral**

Este documento descreve as decisões técnicas implementadas no código do projeto Clubbi (API FastAPI) de acordo com requisitos do case técnico.

**Resumo Arquitetural**

- **Framework**: FastAPI para construção da API HTTP e documentação automática (`/docs`).
- **ORM**: SQLAlchemy 2.0 usando o novo API de tipagem (`Mapped`, `mapped_column`, `DeclarativeBase`).
- **Validação**: Pydantic v2 para schemas de entrada/saída (`from_attributes = True` para aceitar objetos ORM).
- **Estrutura de camadas**: routers → services → models + db, com injeção de dependência via FastAPI `Depends`.

**Decisões de Design — Banco de Dados e Models**

- **Base declarativa**: `app.db.base.Base` usa `DeclarativeBase` do SQLAlchemy 2.0, alinhado com as boas práticas do SQLAlchemy moderno.
- **Tipos monetários**: `Numeric(10, 2)` (mapeado para `Decimal`) em campos de preço/valor (`Offer.unit_price`, `CartItem.unit_price_snapshot`, `Payment.amount`) para preservar precisão financeira.
- **Enum como SQLEnum**: `CartStatus` e `PaymentStatus` são mapeados com `SQLEnum`, garantindo valores restritos no banco.
- **Relacionamentos e cascades**: `Cart.items` usa `cascade="all, delete-orphan"`, garantindo que itens de carrinho sejam removidos quando o carrinho for deletado.

**Decisões de Design — Regras de Negócio e Serviços**

- **Serviços orientados a objetos**: `CartService` e `CheckoutService` encapsulam regras de negócio e dependem de uma `Session` injetada. Isso favorece testabilidade e separação de responsabilidade.
- **Fluxo de checkout linear**: `CheckoutService` modela um fluxo estrito de estado `OPEN -> CHECKOUT -> PAID`. O método `start_checkout` valida itens e altera estado para `CHECKOUT`; `finalize_payment` exige `CHECKOUT` e cria `Payment` com `PaymentStatus.PAID`.
- **Snapshot de preço**: Ao adicionar item ao carrinho, grava-se `unit_price_snapshot` a partir da `Offer.unit_price`. Isso preserva histórico de preço para o pedido mesmo que a oferta mude depois.

**Gestão de Sessão e Transações**

- **Engine e sessionmaker**: `app.db.connection.get_engine()` cria e memoiza o `Engine` a partir de `DATA_BASE_URL` (carregado via `python-dotenv`). O `sessionmaker` é criado com `expire_on_commit=False` e `autoflush=False`.
- **Dependência de sessão**: `get_session()` é uma generator dependency que `yield` a sessão e fecha no bloco `finally` — adequada para uso com FastAPI `Depends`.
- **Padrão de commits**: Os serviços fazem adição de novos items no banco, fazendo um `flush()` manual, enquanto quem finaliza a sessão com o commit é a própria sessão após ser gerenciada pelo FastAPI.

Risco/Observação: o `sessionmaker` é instanciado chamando `get_engine()` durante import — isso é aceitável, mas significa que a criação do engine ocorre em tempo de importação do módulo `connection`.

**Validação e Schemas (Pydantic)**

- **Schemas de saída**: `CartSchema`, `CartItemSchema`, `OfferSchema` e `PaymentSchema` usam `Config.from_attributes = True` (Pydantic v2) para leitura direta de instâncias ORM.
- **Validação de entrada**: `AddOfferToCart.quantity` usa `Field(gt=0)` para garantir quantidade > 0 já na borda da API.

**Tratamento de Erros e Exceções**

- **Exceções de negócio centralizadas**: `app.exceptions.BusinessException` e subclasses (por exemplo `CartNotFoundError`, `ExpiredOfferError`) encapsulam status HTTP e mensagens de erro. O `app` registra um handler que transforma `BusinessException` em `JSONResponse` com `status_code` e `detail`.

Benefício: esse padrão facilita a separação entre regras de negócio e mapeamento HTTP, mantendo respostas consistentes.

**Design da API**

- **Routers por domínio**: `cart_router`, `catalog_router`, `checkout_router` com prefixo `/api/v1` e `tags` para documentação clara.
- **Resposta com models Pydantic**: endpoints usam `response_model` para serialização automática.

**Seed e dados de desenvolvimento**

- `app.db.seed_database.seed_data()` popula produtos, clientes e ofertas com dados de exemplo gerados programaticamente. Útil para ambiente local e testes manuais.

**Observações, Riscos e Sugestões**

- Validação de concorrência: atualmente não há locks/checagens de concorrência (p.ex. para garantir que duas requisições simultâneas não criem dois carts para o mesmo cliente). Considerar `SELECT ... FOR UPDATE` ou regras de integridade no DB.

**Como executar localmente (resumo rápido)**

- Definir variável de ambiente `DATA_BASE_URL` (ex.: `sqlite+aiosqlite:///./dev.db` ou `sqlite:///./dev.db` para uso síncrono conforme driver instalado).
- Rodar a aplicação:

```bash
uvicorn app.main:app --reload
```

- Popular dados de desenvolvimento:

```bash
python -m app.db.seed_database
```

**Conclusão**

O projeto já segue várias boas práticas: separação clara de camadas, uso do SQLAlchemy 2.0 tipado, Pydantic v2 e tratamento centralizado de exceções. Existem pequenas áreas de atenção desenho de transações, etc... que, se ajustadas, melhorarão robustez para produção.
