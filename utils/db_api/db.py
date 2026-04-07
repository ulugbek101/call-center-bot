import pymysql


class Database:
    def __init__(self, db_name, db_password, db_user, db_port, db_host):
        self.db_name = db_name
        self.db_password = db_password
        self.db_user = db_user
        self.db_port = db_port
        self.db_host = db_host

    def connect(self):
        return pymysql.Connection(
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self, sql: str, params: tuple = (), commit=False, fetchone=False, fetchall=False) -> dict | list:
        database = self.connect()
        cursor = database.cursor()

        cursor.execute(sql, params)
        data = None

        if fetchone:
            data = cursor.fetchone()

        elif fetchall:
            data = cursor.fetchall()

        if commit:
            database.commit()

        return data

    def get_user(self, activation_code: str) -> dict | None:
        """Return user from database if exists

        Args:
            activation_code (str): activation code of a user

        Returns:
            dict | None: user dict or None
        """
        sql = """
            SELECT * FROM users WHERE activation_code = %s AND is_activation_code_used = FALSE
        """
        return self.execute(sql, (activation_code,), fetchone=True)

    def save_attribute(self, attribute_name: str, value: str, telegram_id: str) -> None:
        """Saves user's attribute

        Args:
            attribute (str): user's attribute name, for example: first_name, last_name, ...
            telegram_id (str): user's telegram id
        """
        sql = f"""
            UPDATE users set {attribute_name}=%s WHERE telegram_id = %s
        """
        self.execute(sql, (value, telegram_id), commit=True)

    def activate_user(self, activation_code: str, telegram_id) -> None:
        """Activates user by activation code so that no one can use this activation code again

        Args:
            activate_user (str): activation code of a user
            telegram_id (str): telegram id of a user
        """
        sql = """
            UPDATE users SET is_activation_code_used = TRUE, telegram_id = %s WHERE activation_code = %s
        """
        self.execute(sql, (telegram_id, activation_code,), commit=True)
