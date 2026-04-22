import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / 'banco.db'

def main():
    print(f"Seeding sample business tables in: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create produtos and itens_venda if not exists
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto TEXT NOT NULL
        );'''
    )

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            FOREIGN KEY(id_produto) REFERENCES produtos(id_produto)
        );'''
    )

    # Insert sample products if empty
    cur.execute('SELECT COUNT(*) FROM produtos')
    if cur.fetchone()[0] == 0:
        products = [
            ('Camiseta Azul',),
            ('Caneca Logo',),
            ('Notebook 14"',),
            ('Fone Bluetooth',),
            ('Cabo USB-C',),
        ]
        cur.executemany('INSERT INTO produtos (nome_produto) VALUES (?)', products)

    # Insert sample vendas (itens_venda)
    cur.execute('SELECT COUNT(*) FROM itens_venda')
    if cur.fetchone()[0] == 0:
        # Map product ids (assume autoincrement order)
        # Create some sales with varying quantities
        vendas = [
            (1, 10),
            (2, 5),
            (3, 7),
            (4, 2),
            (5, 12),
            (1, 3),
            (3, 4),
            (5, 1),
            (2, 6),
            (1, 8),
        ]
        cur.executemany('INSERT INTO itens_venda (id_produto, quantidade) VALUES (?, ?)', vendas)

    conn.commit()
    conn.close()
    print('Seeding complete.')

if __name__ == '__main__':
    main()
