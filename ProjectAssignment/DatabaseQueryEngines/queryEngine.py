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
        self.primary_key: str = primary_key

        ctr = 0
        for col in columns:
            self.columnToDatabaseIndexMapping[col] = ctr
            ctr += 1

    def Select(
        self, column: str, conditionType: str = "=", value: Any = None
    ) -> "Database":
        if value is None:
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

    #
