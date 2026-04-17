
# Agradecimentos

Olá!

Primeiramente agradeço à Wellbe pela oportunidade de apresentar um pouco do meu conhecimento através desse desafio.

Na minha solução tentei explorar pontos extras que considerei interessante, não consegui inserir todos, mas acredito que o que foi desenvolvido atende à necessidade.

Para não fugir do que foi solicitado, desenvolvi o `selenium_challenge.py` que segue os passos originais. A solução mais completa ficou no fluxo de requisição.

No `run.py` podem ser iniciados os dois fluxos, conforme as opções disponíveis.

Para as invoices 2 e 4 (mesmo padrão), foi feita uma extração usando Tesseract — se estiver instalado no sistema, o arquivo zip de saída, além das invoices em imagem, terá um arquivo Excel com os dados extraídos (testado apenas com as invoices 2 e 4). Caso não esteja instalado, o fluxo seguirá normalmente sem gerar esse arquivo.

Deixei scripts extras para execução direta de cada etapa individualmente.

# Execução

Crie o arquivo `.env` com as mesmas variáveis do `.env.example` e ajuste a string de conexão do MySQL conforme o ambiente utilizado.

**Opcional:** instalar o Tesseract:

* https://github.com/UB-Mannheim/tesseract/wiki

1. `python -m venv .venv`
2. Windows: `.venv\Scripts\activate` | Linux: `source .venv/bin/activate`
3. `python -m pip install --upgrade pip`
4. `python -m pip install -r requirements.txt`
5. `alembic upgrade head`
6. `python run.py`
7. Opção 1 — navegação/extração com Selenium
8. Opção 2 — extração por requisição
