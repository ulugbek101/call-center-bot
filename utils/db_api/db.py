from typing import Tuple

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

    def execute(self, sql: str, params: tuple = (), commit=False, fetchone=False, fetchall=False) -> dict | list | None:
        """Execution function of SQL code passed to this function

        Args:
            sql (str): SQL code
            params (tuple, optional): parameters that should be passed to SQL code. Defaults to ().
            commit (bool, optional): Whether operation should be committed or not. Defaults to False.
            fetchone (bool, optional): Whether operation should return single object or not. Defaults to False.
            fetchall (bool, optional): Wether operation should return list of objects or not. Defaults to False.

        Returns:
            dict | list | None: single object, list of objects or None if fetchone or fetchall where not specified
        """

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

    def get_user_by_telegram_id(self, telegram_id: str) -> dict | None:
        """Return user from database if exists

        Args:
            telegram_id (str): user's telegram id

        Returns:
            dict | None: user dict or None
        """
        sql = """
            SELECT * FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchone=True)

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

    def get_user_points(self, user_id: str) -> int:
        """Return user's total points from database

        Args:
            user_id (str): user's id

        Returns:
            int: user's total points
        """
        sql = """
            SELECT SUM(amount) AS total_points FROM points WHERE user_id = %s
        """
        return self.execute(sql, (user_id,), fetchone=True).get("total_points")

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

    def check_user_activation(self, telegram_id: str) -> bool:
        """Checks user activation status

        Args:
            telegram_id (str): user's telegram id

        Returns:
            bool: True/False
        """

        sql = """
            SELECT * FROM users WHERE telegram_id = %s
        """
        return bool(self.execute(sql, (telegram_id,), fetchone=True))

    def get_milestones(self) -> list[dict]:
        """Returns milestones list from database

        Returns:
            list[dict]: list of milestone objects
        """

        sql = """
            SELECT * FROM milestones WHERE is_active = TRUE
        """
        return self.execute(sql, fetchall=True)

    def get_user_progress(self, telegram_id: str) -> Tuple[int, str]:
        """Returns user's progress as user's score and user's milestone where he/she reached

        Args:
            telegram_id (str): user's telegram id

        Returns:
            Tuple[int, str]: score, milestone name
        """
        user = self.get_user_by_telegram_id(telegram_id=telegram_id)
        user_points = self.get_user_points(user_id=user.get("id"))
        milestones = self.get_milestones()

        current_milestone = ""

        for milestone in milestones:
            if (user_points or 0) >= milestone.get("required_score"):
                current_milestone = milestone.get("name")

        return user_points, current_milestone
