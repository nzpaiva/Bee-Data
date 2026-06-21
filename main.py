import sys

import oracledb

from application import Application

# CONFIGURAÇÕES DE CONEXÃO
DB_USER = "c##bee_data"
DB_PASSWORD = "abc123"
DB_DSN = "localhost:1521/FREE"


if __name__ == "__main__":
    try:
        app = Application(DB_USER, DB_PASSWORD, DB_DSN)
        app.run()
    except oracledb.Error as e:
        # Não tem o que fazer quando a aplicação nem consegue se conectar ao banco de dados
        print(f"\n[ERRO FATAL] Falha ao conectar ao banco de dados: {e}")
        sys.exit(1)
