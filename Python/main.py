import sys

import oracledb

from application import Application

# CONFIGURAÇÕES DE CONEXÃO
DB_USER = "a13687449"
DB_PASSWORD = "a895"
DB_DSN = "orclgrad1.icmc.usp.br:1521/pdb_elaine.icmc.usp.br"


if __name__ == "__main__":
    try:
        app = Application(DB_USER, DB_PASSWORD, DB_DSN)
        app.run()
    except oracledb.Error as e:
        # Não tem o que fazer quando a aplicação nem consegue se conectar ao banco de dados
        print(f"\n[ERRO FATAL] Falha ao conectar ao banco de dados: {e}")
        sys.exit(1)
