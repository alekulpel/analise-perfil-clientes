import pandas as pd
import random
from faker import Faker
import numpy as np

fake = Faker('pt_BR')
random.seed(42)
np.random.seed(42)

ESTADOS = ['SP', 'RJ', 'MG', 'RS', 'PR', 'BA', 'PE', 'CE', 'DF']

def gerar_dados_clientes(n=10000):
    dados = []

    for i in range(n):
        idade = random.randint(18, 70)
        renda = round(np.random.normal(loc=5000, scale=2000), 2)
        renda = max(renda, 1200)  # valor mínimo razoável
        tempo_cliente = random.randint(1, 60)

        ticket_medio = round(np.random.normal(300, 120), 2)
        ticket_medio = max(ticket_medio, 30)

        qtd_compras = random.randint(0, tempo_cliente)

        tipo = random.choices(
            ['Produto', 'Serviço', 'Ambos'],
            weights=[0.4, 0.3, 0.3],
            k=1
        )[0]

        genero = random.choice(['Masculino', 'Feminino'])

        visitas = random.randint(0, 30)
        reclamacoes = np.random.poisson(0.5)
        satisfacao = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.1, 0.3, 0.3, 0.2])[0]

        # Churn com chance maior se satisfação for baixa ou poucas compras
        churn_prob = 0.1 + 0.3 * (satisfacao < 3) + 0.2 * (qtd_compras == 0)
        churn = int(random.random() < churn_prob)

        cliente = {
            'id_cliente': i + 1,
            'nome': fake.name(),
            'idade': idade,
            'genero': genero,
            'estado': random.choice(ESTADOS),
            'renda_mensal': renda,
            'tipo_cliente': tipo,
            'qtd_compras_ultimos_12m': qtd_compras,
            'ticket_medio': ticket_medio,
            'tempo_como_cliente': tempo_cliente,
            'visitas_site_mes': visitas,
            'reclamacoes_12m': reclamacoes,
            'satisfacao': satisfacao,
            'churn': churn
        }

        dados.append(cliente)

    return pd.DataFrame(dados)

if __name__ == "__main__":
    df_clientes = gerar_dados_clientes(1000)
    df_clientes.to_csv('data/raw/clientes.csv', index=False)
    print("Base de dados gerada em 'data/raw/clientes.csv'")
