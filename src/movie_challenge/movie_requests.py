import requests
from urllib.parse import urlencode, quote
import time
from src.movie_challenge.rpachallenge_headers import search_headers
from src.config import RPA_CHALLENGE_API_KEY, logger

class RpaChallengeRequest:

    def __init__(self):
        self.api_key = RPA_CHALLENGE_API_KEY
        self.session = requests.Session()
        self.movies = []
        self.error_message = None
        
    def start_session(self):
        logger.info("Iniciando sessão")
        try:
            self.session.get("https://rpachallenge.com", timeout=10)
            logger.info("Sessão iniciada com sucesso")
            return True
        except Exception as e:
            self.error_message = f"Erro ao iniciar sessão: {e}"
            logger.error(self.error_message)
            return False

    def movie_search(self, text):
        """Busca filmes na API com paginação e tentativas automáticas em caso de falha."""
        logger.info("Iniciando busca por filme: %s", text)
        params = {
            "query": text, 
            "api_key": self.api_key,
            "sort_by": "popularity.desc",
            "page": 1
        }
    
        movies = []
        max_try = 10
        logger.info("Realizando busca por: %s", text)
        while max_try > 0:
            try:
                tmp_params = urlencode(params, quote_via=quote, safe=' ')
                url_search = f"https://api.themoviedb.org/3/search/movie?{tmp_params}"
                response = self.session.get(url_search, headers=search_headers)
                
                if response.status_code != 200:
                    logger.error("Erro na resposta da API: %s", response.text)
                    return False, f"Erro na resposta da API: {response.text}"
                
                data = response.json()
                movies += data.get("results")

                if  data.get("page") >= data.get("total_pages", 0) or data.get("page") > 999:
                    break

                logger.info("Página %i de %i processada", data.get("page"), data.get("total_pages", 0))
                params["page"] += 1
                time.sleep(2)

            except Exception as e:
                self.error_message = f"Falha ao realizar a busca: {e}"
                logger.error(self.error_message)
                max_try -= 1
                if max_try > 0:
                    print("Tentando novamente em 5 segundos...")
                    time.sleep(5)
    
        logger.info("Busca realizada com sucesso")
        logger.info("A busca retornou %i resultados", len(movies))

        self.movies = movies
        return True