# Agradecimentos

Olá!

Primeiramente agradeço a Wellbe pela oportunidade de apresentar um pouco do meu conhecimento através desse desafio aparentemente simples.

Na minha solução tentei explorar pontos extras que considerei ser interessante ter, não consegui inserir todos mas acredito que o que foi desenvolvido atende a necessidade.

Para não fugir do que foi solicitado, fiz o selenium_challenge.py que segue os passos originais.

A solução mais completa ficou no fluxo de requisição.

No run.py pode ser iniciado os dois fluxos, conforme as opções disponíveis.

Para as invoices 2 e 4 (mesmo padrão), fiz uma extração usando tesseract, se tiver instalado no sistema no arquivo zip de saída além das invoices em imagem terá um arquivo em excel com os dados extraídos (testados apenas com as invoices 2 e 4), mas, caso não tenha o fluxo seguirá normalmente sem gerar esse arquivo.

Deixei scripts extras para o caso de execução de uma etapa diretamente.

# Execução

crie o arquivo .env com as mesmas variáveis do .env.example e altere na string de conexão do mysql para o que será usado.

Opcional instalar o tesseract:

- https://github.com/UB-Mannheim/tesseract/wiki

1) python -m venv .venv
2) (windows) .venv\Scripts\activate | (linux) **source** .venv/bin/activate
3) python -m pip install --upgrade pip
4) python -m pip install -r requirements.txt
5) alembic upgrade head
6) python run.py
7) Opção 1, navegação/extração com selenium
8) Opção 2, extração por requisição
