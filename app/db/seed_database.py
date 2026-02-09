# seed_database.py
import random
from datetime import datetime, timedelta

from app.db.connection import get_session, get_engine
from app.db.base import Base

from app.models.product import Product
from app.models.client import Client
from app.models.offer import Offer

def seed_data():
    """Popula o banco com dados de exemplo gerados por IA"""
    
    db_generator = get_session()
    db = next(db_generator)
    
    try:
        # Criar tabelas (se ainda não existem)
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
        
        # Limpar dados existentes (opcional)
        print("🗑️  Limpando dados antigos...")
        db.query(Offer).delete()
        db.query(Product).delete()
        db.query(Client).delete()
        db.commit()
        
        # ========== PRODUTOS (supermercado RJ) ==========
        products_data = [
            # Alimentos Básicos
            {"ean": "7891234567890", "name": "Arroz Branco Tipo 1 - 1kg", "items_per_box": 10},
            {"ean": "7891234567891", "name": "Feijão Preto - 1kg", "items_per_box": 10},
            {"ean": "7891234567892", "name": "Açúcar Refinado - 1kg", "items_per_box": 10},
            {"ean": "7891234567893", "name": "Óleo de Soja - 900ml", "items_per_box": 12},
            {"ean": "7891234567894", "name": "Café Torrado e Moído - 500g", "items_per_box": 10},
            {"ean": "7891234567895", "name": "Sal Refinado - 1kg", "items_per_box": 10},
            {"ean": "7891234567896", "name": "Farinha de Trigo - 1kg", "items_per_box": 10},
            {"ean": "7891234567897", "name": "Macarrão Espaguete - 500g", "items_per_box": 20},
            
            # Bebidas
            {"ean": "7891234567898", "name": "Refrigerante Cola 2L", "items_per_box": 6},
            {"ean": "7891234567899", "name": "Refrigerante Guaraná 2L", "items_per_box": 6},
            {"ean": "7891234567900", "name": "Suco de Laranja 1L", "items_per_box": 12},
            {"ean": "7891234567901", "name": "Água Mineral 500ml", "items_per_box": 24},
            {"ean": "7891234567902", "name": "Cerveja Lata 350ml", "items_per_box": 12},
            
            # Higiene e Limpeza
            {"ean": "7891234567903", "name": "Sabão em Pó - 1kg", "items_per_box": 8},
            {"ean": "7891234567904", "name": "Detergente Líquido 500ml", "items_per_box": 24},
            {"ean": "7891234567905", "name": "Papel Higiênico 4 rolos", "items_per_box": 16},
            {"ean": "7891234567906", "name": "Sabonete 90g", "items_per_box": 48},
            {"ean": "7891234567907", "name": "Desinfetante 2L", "items_per_box": 6},
            
            # Laticínios
            {"ean": "7891234567908", "name": "Leite Integral 1L", "items_per_box": 12},
            {"ean": "7891234567909", "name": "Iogurte Natural 170g", "items_per_box": 24},
            {"ean": "7891234567910", "name": "Manteiga 200g", "items_per_box": 12},
            
            # Snacks
            {"ean": "7891234567911", "name": "Biscoito Cream Cracker 200g", "items_per_box": 20},
            {"ean": "7891234567912", "name": "Bolacha Recheada 130g", "items_per_box": 24},
            {"ean": "7891234567913", "name": "Salgadinho 100g", "items_per_box": 30},
        ]
        
        products = []
        print("📦 Criando produtos...")
        for data in products_data:
            product = Product(**data)
            db.add(product)
            products.append(product)
        
        db.commit()
        print(f"✅ {len(products)} produtos criados!")
        
        # ========== CLIENTES (supermercados RJ) ==========
        clients_data = [
            {
                "name": "Minimercado São Jorge",
                "address": "Rua das Flores, 123 - Copacabana, Rio de Janeiro - RJ",
                "cnpj": "12.345.678/0001-91"
            },
            {
                "name": "Mercadinho Estrela",
                "address": "Av. Atlântica, 456 - Ipanema, Rio de Janeiro - RJ",
                "cnpj": "23.456.789/0001-82"
            },
            {
                "name": "Supermercado Bom Preço",
                "address": "Rua Barão de Ipanema, 789 - Botafogo, Rio de Janeiro - RJ",
                "cnpj": "34.567.890/0001-73"
            },
            {
                "name": "Mercado da Praça",
                "address": "Praça da Bandeira, 321 - Centro, Rio de Janeiro - RJ",
                "cnpj": "45.678.901/0001-64"
            },
            {
                "name": "Empório Carioca",
                "address": "Rua do Catete, 654 - Catete, Rio de Janeiro - RJ",
                "cnpj": "56.789.012/0001-55"
            },
            {
                "name": "Mercearia do Bairro",
                "address": "Rua Visconde de Pirajá, 987 - Ipanema, Rio de Janeiro - RJ",
                "cnpj": "67.890.123/0001-46"
            },
            {
                "name": "Supermercado Família",
                "address": "Av. Nossa Senhora de Copacabana, 1234 - Copacabana, RJ",
                "cnpj": "78.901.234/0001-37"
            },
            {
                "name": "Mercadinho Vila Isabel",
                "address": "Rua Teodoro da Silva, 567 - Vila Isabel, Rio de Janeiro - RJ",
                "cnpj": "89.012.345/0001-28"
            },
            {
                "name": "Mercado Tijuca",
                "address": "Rua Conde de Bonfim, 890 - Tijuca, Rio de Janeiro - RJ",
                "cnpj": "90.123.456/0001-19"
            },
            {
                "name": "Empório Zona Sul",
                "address": "Rua Voluntários da Pátria, 432 - Botafogo, Rio de Janeiro - RJ",
                "cnpj": "01.234.567/0001-00"
            },
        ]
        
        clients = []
        print("👥 Criando clientes...")
        for data in clients_data:
            client = Client(**data)
            db.add(client)
            clients.append(client)
        
        db.commit()
        print(f"✅ {len(clients)} clientes criados!")
        
        # ========== OFERTAS (preços específicos por cliente) ==========
        print("💰 Criando ofertas personalizadas...")
        offers = []
        base_prices = {
            "Arroz": 25.90,
            "Feijão": 8.50,
            "Açúcar": 4.20,
            "Óleo": 7.80,
            "Café": 15.50,
            "Sal": 2.10,
            "Farinha": 4.50,
            "Macarrão": 3.20,
            "Refrigerante Cola": 6.50,
            "Refrigerante Guaraná": 5.90,
            "Suco": 4.80,
            "Água": 1.20,
            "Cerveja": 2.80,
            "Sabão": 12.90,
            "Detergente": 2.50,
            "Papel": 15.90,
            "Sabonete": 1.80,
            "Desinfetante": 8.90,
            "Leite": 4.50,
            "Iogurte": 2.30,
            "Manteiga": 11.50,
            "Biscoito": 3.80,
            "Bolacha": 4.20,
            "Salgadinho": 5.50,
        }
        
        for client in clients:
            # Cada cliente tem ofertas para produtos aleatórios
            num_offers = random.randint(15, len(products))
            selected_products = random.sample(products, num_offers)
            
            for product in selected_products:
                # Encontrar preço base pelo nome do produto
                base_price = 5.00  # default
                for key, price in base_prices.items():
                    if key in product.name:
                        base_price = price
                        break
                
                # Variar preço ±15% por cliente (ofertas personalizadas)
                variation = random.uniform(0.85, 1.15)
                unit_price = round(base_price * variation, 2)
                
                # Validade entre 30 e 90 dias
                days_valid = random.randint(30, 90)
                valid_until = datetime.now() + timedelta(days=days_valid)
                
                offer = Offer(
                    product_id=product.id,
                    client_id=client.id,
                    unit_price=unit_price,
                    valid_until=valid_until
                )
                db.add(offer)
                offers.append(offer)
        
        db.commit()
        print(f"✅ {len(offers)} ofertas criadas!")
        
        print("\n" + "="*50)
        print("🎉 DATABASE POPULADO COM SUCESSO!")
        print("="*50)
        print(f"📊 Resumo:")
        print(f"   📦 Produtos: {len(products)}")
        print(f"   👥 Clientes: {len(clients)}")
        print(f"   💰 Ofertas:  {len(offers)}")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Erro ao popular banco: {e}")
        db.rollback()
        raise
    finally:
        # Fechar a sessão usando o generator
        try:
            next(db_generator)
        except StopIteration:
            pass

if __name__ == "__main__":
    seed_data()