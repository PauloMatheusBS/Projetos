import mysql.connector

class BancoDB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="10.28.2.59",
            user="suporte",
            password="suporte",
            database="bancoparca"
        )
        self.cursor = self.conn.cursor()

    def autenticar_usuario(self, titular, senha):
        try:
            self.cursor.execute("SELECT tipo_perfil FROM perfis WHERE titular = %s AND senha = %s", (titular, senha))
            perfil = self.cursor.fetchone()
            return perfil[0] if perfil else None
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return None

    def criar_conta(self, titular):
        try:
            self.cursor.execute("INSERT INTO contas (titular) VALUES (%s)", (titular,))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return False
        
    def excluir_conta(self, titular):
        try:
            self.cursor.execute("DELETE FROM contas WHERE titular = %s", (titular,))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return False

    def depositar(self, titular, valor):
        try:
            self.cursor.execute("UPDATE contas SET saldo = saldo + %s WHERE titular = %s", (valor, titular))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return False

    def sacar(self, titular, valor):
        try:
            self.cursor.execute("SELECT saldo FROM contas WHERE titular = %s", (titular,))
            saldo = self.cursor.fetchone()[0]
            if saldo >= valor:
                self.cursor.execute("UPDATE contas SET saldo = saldo - %s WHERE titular = %s", (valor, titular))
                self.conn.commit()
                return True
            else:
                return False
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return False

    def transferir(self, titular_origem, valor, cpf_destino=None, numero_conta_destino=None):
        if self.sacar(titular_origem, valor):
            if cpf_destino:
                self.cursor.execute("SELECT titular FROM contas WHERE cpf = %s", (cpf_destino,))
                destinatario = self.cursor.fetchone()
                if destinatario:
                    return self.depositar(destinatario[0], valor)
            elif numero_conta_destino:
                self.cursor.execute("SELECT titular FROM contas WHERE numero_conta = %s", (numero_conta_destino,))
                destinatario = self.cursor.fetchone()
                if destinatario:
                    return self.depositar(destinatario[0], valor)
        return False


    def consultar_saldo(self, titular):
        try:
            self.cursor.execute("SELECT saldo FROM contas WHERE titular = %s", (titular,))
            saldo = self.cursor.fetchone()
            return saldo[0] if saldo else None
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return None

    def listar_contas(self):
        self.cursor.execute("SELECT * FROM contas")
        return self.cursor.fetchall()

    def fechar_conexao(self):
        self.cursor.close()
        self.conn.close()
