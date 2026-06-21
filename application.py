import oracledb

import validador


def formatar_erro(e):
    # Erros customizados
    if 20000 <= e.code <= 20015:
        msg = e.message.split(": ", 1)[-1].split("\n")[0]
        print(f"  > {msg}")

    # Primary Keys e Unique Constraints
    elif e.code == 1:
        msg = e.message.upper()

        if "PK_FUNCIONARIO" in msg:
            print("  > Já existe um funcionário cadastrado com este CPF.")
        elif "PK_AUDITOR" in msg:
            print("  > Já existe um auditor cadastrado com este CPF.")
        elif "UK_APIARIO" in msg:
            print(
                "  > Este funcionário já é responsável por outro apiário (limite de 1 por pessoa)."
            )
        elif "UK_SENSOR" in msg or "UK_SENSOR_PS" in msg:
            print(
                "  > Já existe um sensor vinculado a esta colmeia ou número de série duplicado."
            )
        elif "UK_LOTE" in msg:
            print("  > Já existe um lote com este produto, ordem e data.")
        else:
            print(
                "  > Você tentou inserir uma informação que já existe e deve ser única."
            )

    # Erros de restrição
    elif e.code == 2290:
        msg = e.message.upper()

        if "CK_VINCULO_EMPREGATICIO" in msg:
            print("  > Vínculo inválido. Permitidos: CLT, PJ, AUTÔNOMO ou TERCERIZADO.")
        elif "CK_FUNCAO" in msg:
            print(
                "  > Função inválida. Permitidos: TECNICO, APICULTOR, SUPERVISOR, CONTROLE QUALIDADE ou PRODUTOR."
            )
        elif "CK_COORDENADA_LAT" in msg or "CK_COORDENADA_LON" in msg:
            print(
                "  > Coordenada inválida. Latitude deve ser entre -90/90 e Longitude entre -180/180."
            )
        elif "CK_ORIGEM" in msg:
            print("  > Origem de insumo inválida. Permitidos: EXTERNO ou INTERNO.")
        elif "CK_INTERVENCAO" in msg:
            print(
                "  > Tipo de intervenção inválida. Permitidos: EXTRACAO ou MANUTENSAO."
            )
        else:
            print(
                "  > Os dados inseridos não cumprem as regras de formatação do banco."
            )

    # Erros de chave estrangeira
    elif e.code == 2291:
        print(
            "  > Referência inválida: Você tentou vincular a um registro (CPF, Apiário, Colmeia, etc.) que não existe no sistema."
        )

    # Erros de campos obrigatórios
    elif e.code == 1400:
        print(
            "  > Campo obrigatório em branco: Você deixou de preencher um dado essencial."
        )

    # Erros de tamanho do dado
    elif e.code == 12899:
        print(
            "  > Limite excedido: Um dos textos digitados é maior do que o espaço disponível no banco de dados."
        )

    # Erro desconhecido
    else:
        print(f"  > Erro desconhecido ({e.code}): {e.message}")


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
                ("AUTÔNOMO", "Autônomo"),
                ("TERCERIZADO", "Terceirizado"),
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
            salario = self.read_until_success("Salário (xxxx,xx): ", validador.salario)
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
                    "salario": salario,
                    "vinculo": VINCULOS[vinculo][0],
                    "funcao": FUNCOES[funcao][0],
                }
            )
            print("\n[SUCESSO] Funcionário cadastrado com sucesso no sistema!")
        except oracledb.Error as e:
            (error_obj,) = e.args
            self.conn.rollback()
            print("\n[ERRO BANCO DE DADOS]")
            formatar_erro(error_obj)
        except EOFError:
            print(
                "\n[AVISO] Entrada interrompida pelo usuário. Nenhum dado foi registrado."
            )

    def register_worker(self, data):
        """Registra um novo funcionário no banco de dados."""
        QUERY = """
            INSERT INTO FUNCIONARIO (
                CPF, NOME, TELEFONE, ENDERECO, EMAIL, DATA_CONTRATACAO,
                SALARIO_BASE, VINCULO_EMPREGATICIO, FUNCAO
            ) VALUES (
                :cpf, :nome, :telefone, :endereco, :email,
                TO_DATE(:data_contratacao, 'DD/MM/YYYY'), :salario, :vinculo, :funcao
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
        except oracledb.Error as e:
            (error_obj,) = e.args
            print("\n[ERRO BANCO DE DADOS]")
            formatar_erro(error_obj)
        except EOFError:
            print("\n[FINALIZADO]")

    def track_batch(self, id_lote):
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
                    print(f"Aprovação : {data_aprov} | Nota: {aud[2]} | Selo: {aud[3]}")
                    print(f"Status    : {aud[4]}")
                    print("-")
            else:
                print("Nenhum registro de auditoria vinculado a este lote.")

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
            print(prompt)

            for index, option in enumerate(options):
                print(f"  {index + 1}.\t{option}")

            value = input("\n  > ").strip()

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

            match input("Escolha uma opção:\n  > "):
                case "1":
                    self.register_worker_prompt()
                case "2":
                    self.track_batch_prompt()
                case "0":
                    break
                case _:
                    print("Opção inválida. Tente novamente.")
