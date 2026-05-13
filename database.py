"""
Database Module
Handles connections to SQL Server and query execution.
"""

import pyodbc
from typing import List, Dict, Tuple, Any, Optional


class Database:
    """Manages database connections and query execution."""
    
    def __init__(self, server: str, database: str, username: str = None, password: str = None):
        """
        Initialize database connection.
        
        Args:
            server: SQL Server name or connection string
            database: Database name
            username: Optional username for authentication
            password: Optional password for authentication
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """
        Establish connection to SQL Server.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            if self.username and self.password:
                # SQL Authentication
                connection_string = (
                    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                    f'SERVER={self.server};'
                    f'DATABASE={self.database};'
                    f'UID={self.username};'
                    f'PWD={self.password}'
                )
            else:
                # Windows Authentication
                connection_string = (
                    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                    f'SERVER={self.server};'
                    f'DATABASE={self.database};'
                    f'Trusted_Connection=yes'
                )
            
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            print(f"✓ Connected to database: {self.database}")
            return True
        except pyodbc.Error as e:
            print(f"✗ Database connection failed: {e}")
            return False
    
    def disconnect(self) -> None:
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")
    
    def execute_query(self, query: str, params: Tuple = None) -> bool:
        """
        Execute a query (INSERT, UPDATE, DELETE).
        
        Args:
            query: SQL query string
            params: Optional tuple of parameters for parameterized queries
        
        Returns:
            bool: True if execution successful, False otherwise
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            self.connection.rollback()
            print(f"✗ Query execution failed: {e}")
            return False
    
    def fetch_one(self, query: str, params: Tuple = None) -> Optional[Dict[str, Any]]:
        """
        Fetch a single row from the database.
        
        Args:
            query: SQL SELECT query
            params: Optional tuple of parameters
        
        Returns:
            Dictionary with column names as keys, or None if no results
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            row = self.cursor.fetchone()
            if row:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, row))
            return None
        except pyodbc.Error as e:
            print(f"✗ Fetch one failed: {e}")
            return None
    
    def fetch_all(self, query: str, params: Tuple = None) -> List[Dict[str, Any]]:
        """
        Fetch all rows from the database.
        
        Args:
            query: SQL SELECT query
            params: Optional tuple of parameters
        
        Returns:
            List of dictionaries with column names as keys
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except pyodbc.Error as e:
            print(f"✗ Fetch all failed: {e}")
            return []
    
    def execute_scalar(self, query: str, params: Tuple = None) -> Optional[Any]:
        """
        Execute a query and return a single scalar value.
        
        Args:
            query: SQL query
            params: Optional tuple of parameters
        
        Returns:
            The scalar value or None
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            row = self.cursor.fetchone()
            return row[0] if row else None
        except pyodbc.Error as e:
            print(f"✗ Scalar execution failed: {e}")
            return None
    
    def is_connected(self) -> bool:
        """Check if database connection is active."""
        return self.connection is not None
