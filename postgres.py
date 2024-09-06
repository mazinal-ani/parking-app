import psycopg2
from psycopg2 import sql

class PostgresDB:
    def __init__(self, dbname="geodata", user="postgres", password="parkingapptest", host="localhost", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Establish a connection to the database."""
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
    
    def close(self):
        """Close the cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Execute a query and return the results."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            return None
    
    def insert_data(self, table, columns, values):
        """Insert data into a table."""
        try:
            insert_query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
                table=sql.Identifier(table),
                columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
                values=sql.SQL(', ').join(map(sql.Placeholder, columns))
            )
            self.cursor.execute(insert_query, dict(zip(columns, values)))
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")
    
    def query(self, query):
        """Select data from a table and return a list of dictionaries."""
        try:
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]  # Get column names
            rows = self.cursor.fetchall()
            result = [dict(zip(columns, row)) for row in rows]  # Combine columns with row data
            return result
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            return None
    
    def update_data(self, table, set_clause, condition=None):
        """Update data in a table."""
        try:
            update_query = sql.SQL("UPDATE {table} SET {set_clause} {condition}").format(
                table=sql.Identifier(table),
                set_clause=sql.SQL(set_clause),
                condition=sql.SQL(condition) if condition else sql.SQL('')
            )
            self.cursor.execute(update_query)
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error updating data: {e}")
    
    def delete_data(self, table, condition):
        """Delete data from a table."""
        try:
            delete_query = sql.SQL("DELETE FROM {table} WHERE {condition}").format(
                table=sql.Identifier(table),
                condition=sql.SQL(condition)
            )
            self.cursor.execute(delete_query)
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error deleting data: {e}")
    
    def __del__(self):
        self.close()
