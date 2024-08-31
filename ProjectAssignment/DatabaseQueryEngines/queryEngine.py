from typing import Dict, List, Any


class Database:
    def __init__(self, columns: Dict[str, str], primary_key: str = None) -> None:
        self.database: List[List[Any]] = []
        self.columnToDatabaseIndexMapping: Dict[str, int] = (
            {}
        )  # maps column name with its index in the 'database' variable
        self.numColumns: int = len(columns)  # keeps track of number of columns
        self.numRows: int = 0  # keeps track of number of rows
        self.columnsSchema: Dict[str, str] = columns  # maps column name with its type
        self.primary_key = primary_key
        ctr = 0
        for col in columns:
            self.columnToDatabaseIndexMapping[col] = ctr
            ctr += 1

    # def Select(
    #     self, column: str, conditionType: str = "=", value: Any = None
    # ) -> "Database":
    #     if value is None:
    #         return self

    #     new_db = Database(self.columnsSchema, self.primary_key)
    #     col_index = self.columnToDatabaseIndexMapping[column]

    #     for row in self.database:
    #         if conditionType == "=" and row[col_index] == value:
    #             new_db.database.append(row)
    #         elif conditionType == ">" and row[col_index] > value:
    #             new_db.database.append(row)
    #         elif conditionType == "<" and row[col_index] < value:
    #             new_db.database.append(row)

    #     new_db.numRows = len(new_db.database)
    #     return new_db

    def insert(self, row: Dict[str, Any]) -> None:
        """Algorithm: Append the new row to the database matrix."""
        if len(row) != self.numColumns:
            raise ValueError("Row does not match the number of columns")
        new_row = [None] * self.numColumns
        for col, value in row.items():
            if col in self.columnToDatabaseIndexMapping:
                new_row[self.columnToDatabaseIndexMapping[col]] = value
        self.database.append(new_row)
        self.numRows += 1

    def alter(self, column_name: str, column_type: str) -> None:
        """Algorithm: Add a new column to the database matrix."""
        self.columnsSchema[column_name] = column_type
        self.columnToDatabaseIndexMapping[column_name] = self.numColumns
        self.numColumns += 1
        for row in self.database:
            row.append(None)

    def delete(self, column: str, conditionType: str, conditionValue: Any) -> None:
        """Algorithm: Remove rows that match the condition."""
        col_index = self.columnToDatabaseIndexMapping[column]
        self.database = [
            row
            for row in self.database
            if not (conditionType == "=" and row[col_index] == conditionValue)
            and not (conditionType == ">" and row[col_index] > conditionValue)
            and not (conditionType == "<" and row[col_index] < conditionValue)
        ]
        self.numRows = len(self.database)

    def update(self, primaryKey: str, parameters: Dict[str, Any]) -> None:
        # get the primary key from the user, and update all the parameters mentioned...if there isn't a parameter in the row, and it's there in the database schema, then add it with None value

        db = self.select(self.primary_key, "=", primaryKey)
        if len(db.database) == 0:
            raise ValueError("Primary key not found in the database")

        for row in db.database:
            for key, value in parameters.items():
                if key in self.columnsSchema:
                    row[self.columnToDatabaseIndexMapping[key]] = value
                else:
                    raise ValueError("Column not found in the database schema")

    def select(
        self, column: str = None, conditionType: str = "=", value: Any = None
    ) -> "Database":
        """Algorithm: Filter rows based on the condition."""
        if value is None:
            return self

        if column == None:
            return self

        new_db = Database(self.columnsSchema, self.primary_key)
        col_index = self.columnToDatabaseIndexMapping[column]

        for row in self.database:
            if conditionType == "=" and row[col_index] == value:
                new_db.database.append(row)
            elif conditionType == ">" and row[col_index] > value:
                new_db.database.append(row)
            elif conditionType == "<" and row[col_index] < value:
                new_db.database.append(row)

        new_db.numRows = len(new_db.database)
        return new_db

    def update(
        self, column: str, value: Any, conditionType: str, conditionValue: Any
    ) -> None:
        """Algorithm: Update rows that match the condition."""
        col_index = self.columnToDatabaseIndexMapping[column]
        for row in self.database:
            if conditionType == "=" and row[col_index] == conditionValue:
                row[col_index] = value
            elif conditionType == ">" and row[col_index] > conditionValue:
                row[col_index] = value
            elif conditionType == "<" and row[col_index] < conditionValue:
                row[col_index] = value


if __name__ == "__main__":
    db = Database({"name": "str", "age": "int"})
    db.insert({"name": "Alice", "age": 25})
    db.insert({"name": "Bob", "age": 30})
    db.insert({"name": "Charlie", "age": 35})
    print(db.select("age", ">", 30).database)
    db.delete("age", ">", 30)
    newDb = db.select("age", "=", 30)
    print(newDb.database)
    newDb = db.select()
    print(newDb.database)

    db.alter("height", "int")
    db.insert({"name": "Alice", "age": 25, "height": 5})
    print(db.select().database)
