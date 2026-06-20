import sys

import oracledb

import validador

# CONFIGURAÇÕES DE CONEXÃO
DB_USER = "c##bee_data"
DB_PASSWORD = "abc123"
DB_DSN = "localhost:1521/FREE"


class Application:
    def __init__(self, db_user, db_password, db_dsn):
        """Estabelece a conexão com o banco de dados Oracle."""
        self.conn = oracledb.connect(user=db_user, password=db_password, dsn=db_dsn)

    def __del__(self):
        """Fecha a conexão com o banco de dados quando o objeto é destruído."""
        if self.conn is not None:
            self.conn.close()

    def register_worker_prompt(self):
        """Registra um novo funcionário no banco de dados."""
        try:
            print("\n" + "=" * 40)
            print("Registro de Funcionário")
            print("=" * 40 + "\n")

            VINCULOS = [
                ("CLT", "CLT"),
                ("PJ", "PJ"),
                ("AUTONOMO", "Autônomo"),
                ("TERCEIRIZADO", "Terceirizado"),
            ]
            FUNCOES = [
                ("TECNICO", "Técnico"),
                ("APICULTOR", "Apicultor"),
                ("SUPERVISOR", "Supervisor"),
                ("CONTROLE QUALIDADE", "Controle de Qualidade"),
                ("PRODUTOR", "Produtor"),
            ]

            cpf = self.read_until_success(
                "CPF (somente números ou xxx.xxx.xxx-xx): ", validador.cpf
            )
            name = self.read_until_success("Nome: ", validador.nome)
            telefone = self.read_until_success(
                "Telefone (com DDD): ", validador.telefone
            )
            endereco = self.read_until_success("Endereço: ", validador.endereco)
            email = self.read_until_success("Email: ", validador.email)
            data_contratacao = self.read_until_success(
                "Data de Contratação (dd/mm/yyyy): ", validador.data
            )
            salary = self.read_until_success("Salário (xxxx,xx): ", validador.salario)
            carteira = self.read_until_success("Carteira: ", validador.carteira)
            vinculo = self.read_option_until_success(
                "Vínculo: ", [it[1] for it in VINCULOS]
            )
            funcao = self.read_option_until_success(
                "Função: ",
                [it[1] for it in FUNCOES],
            )

            self.register_worker(
                {
                    "cpf": cpf,
                    "nome": name,
                    "telefone": telefone,
                    "endereco": endereco,
                    "email": email,
                    "data_contratacao": data_contratacao,
                    "salario": salary,
                    "carteira": carteira,
                    "vinculo": VINCULOS[vinculo][0],
                    "funcao": FUNCOES[funcao][0],
                }
            )
            print("\n[SUCESSO] Funcionário cadastrado com sucesso no sistema!")
        except oracledb.Error as e:
            # TODO: melhorar os erros
            (error_obj,) = e.args
            self.conn.rollback()
            print(f"\n[ERRO BANCO DE DADOS] {error_obj.message}")
        except EOFError:
            print(
                "\n[AVISO] Entrada interrompida pelo usuário. Nenhum dado foi registrado."
            )

    def register_worker(self, data):
        """Registra um novo funcionário no banco de dados."""
        QUERY = """
            INSERT INTO FUNCIONARIO (
                CPF, NOME, TELEFONE, ENDERECO, EMAIL, DATA_CONTRATACAO,
                SALARIO_BASE, CARTEIRA_TRABALHO, VINCULO_EMPREGATICIO, FUNCAO
            ) VALUES (
                :cpf, :nome, :telefone, :endereco, :email,
                TO_DATE(:data_contratacao, 'DD/MM/YYYY'), :salario, :carteira, :vinculo, :funcao
            )
        """

        with self.conn.cursor() as cursor:
            cursor.execute(
                QUERY,
                data,
            )
            self.conn.commit()

    def track_batch_prompt(self):
        print("\n" + "=" * 40)
        print("            RASTREIO DE LOTE")
        print("=" * 40)

        try:
            id = self.read_until_success("ID do lote: ", validador.lote)
            self.track_batch(id)
        except Exception:
            pass

    def track_batch(self, id_lote):
        try:
            sql_lote = """
                SELECT
                    L.ID_LOTE, L.COD_BARRAS, L.NUM_ORDEM, L.DATA_PROD, L.DATA_VAL,
                    L.STATUS, L.QUANTIDADE,
                    PROD.NOME AS NOME_PRODUTOR,
                    CONT.NOME AS NOME_CONTROLE
                FROM LOTE L
                INNER JOIN FUNCIONARIO PROD ON L.CPF_PRODUTOR_RESP = PROD.CPF
                INNER JOIN FUNCIONARIO CONT ON L.CPF_CONTROLE_QUALI = CONT.CPF
                WHERE L.ID_LOTE = :id_lote
            """

            sql_auditoria = """
                SELECT A.NOME, AL.DATA_APROVACAO, AL.NOTA, AL.SELO, AL.STATUS
                FROM AUDITOR_APROVA_LOTE AL
                JOIN AUDITOR A ON AL.CPF_AUDITOR = A.CPF_AUD
                WHERE AL.ID_LOTE = :id_lote
                ORDER BY AL.DATA_APROVACAO DESC
            """

            with self.conn.cursor() as cursor:
                # Executa a busca primária do Lote
                cursor.execute(sql_lote, {"id_lote": id_lote})
                lote = cursor.fetchone()

                if not lote:
                    print(f"\n[AVISO] Nenhum lote encontrado com o ID {id_lote}.")
                    return

                # Formatação segura das datas (caso estejam nulas no banco)
                data_prod = lote[3].strftime("%d/%m/%Y") if lote[3] else "N/A"
                data_val = lote[4].strftime("%d/%m/%Y") if lote[4] else "N/A"

                print("\n" + "-" * 40)
                print("        DETALHES DO LOTE")
                print("-" * 40)
                print(f"ID Lote           : {lote[0]}")
                print(f"Cód. Barras Produto: {lote[1]}")
                print(f"Nº Ordem do Dia   : {lote[2]}")
                print(f"Data de Produção  : {data_prod}")
                print(f"Data de Validade  : {data_val}")
                print(f"Quantidade        : {lote[6]}")
                print(f"Status Atual      : {lote[5]}")
                print(f"Produtor Resp.    : {lote[7]}")
                print(f"Resp. Qualidade   : {lote[8]}")

                # Busca as avaliações dos auditores
                cursor.execute(sql_auditoria, {"id_lote": id_lote})
                auditorias = cursor.fetchall()

                print("\n" + "-" * 40)
                print("      HISTÓRICO DE AUDITORIA")
                print("-" * 40)

                if auditorias:
                    for aud in auditorias:
                        data_aprov = aud[1].strftime("%d/%m/%Y") if aud[1] else "N/A"
                        print(f"Auditor   : {aud[0]}")
                        print(
                            f"Aprovação : {data_aprov} | Nota: {aud[2]} | Selo: {aud[3]}"
                        )
                        print(f"Status    : {aud[4]}")
                        print("-")
                else:
                    print("Nenhum registro de auditoria vinculado a este lote.")
        except:
            # TODO: melhorar os erros
            pass

    def read_until_success(self, prompt, validator=None):
        """Lê uma entrada do usuário até que seja válida."""
        while True:
            value = input(prompt + "\n  > ")

            if validator is None:
                return value
            else:
                try:
                    return validator(value)
                except ValueError as e:
                    print(e)
                    continue

    def read_option_until_success(self, prompt, options):
        """Lê uma opção do usuário até que seja válida."""
        while True:
            for index, option in enumerate(options):
                print(f"  {index + 1}.\t{option}")

            value = input(prompt + "\n  > ").strip()

            if value.isdigit():
                value = int(value)

                if 1 <= value <= len(options):
                    return value - 1

            print("Opção inválida.")

    def run(self):
        """Executa o loop principal da aplicação."""
        while True:
            print("\n" + "=" * 40)
            print("          SISTEMA APÍCOLA")
            print("=" * 40)
            print("  1.\tCadastrar Novo Funcionário")
            print("  2.\tRastrear Lote Produzido")
            print("  0.\tSair do Sistema")

            choice = input("Escolha uma opção: ")
            if choice == "1":
                self.register_worker_prompt()
            elif choice == "2":
                self.track_batch_prompt()
            elif choice == "0":
                break
            else:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        app = Application(DB_USER, DB_PASSWORD, DB_DSN)
        app.run()
    except oracledb.Error as e:
        # Não tem o que fazer quando a aplicação nem consegue se conectar ao banco de dados
        print(f"\n[ERRO FATAL] Falha ao conectar ao banco de dados: {e}")
        sys.exit(1)
