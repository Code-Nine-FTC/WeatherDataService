from testcontainers.postgres import PostgresContainer


def test_connection():
    try:
        with PostgresContainer("postgres:16") as postgres:
            print(f"Conexão bem-sucedida! URL: {postgres.get_connection_url()}")
            return True
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return False


if __name__ == "__main__":
    test_connection()
