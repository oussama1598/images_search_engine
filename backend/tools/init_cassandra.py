from backend.src.db import cassandra_db

if __name__ == '__main__':
    session = cassandra_db.get_session()

    session.execute("CREATE KEYSPACE mnist WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};")
    session.execute(
        "CREATE KEYSPACE imagenet WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};")
