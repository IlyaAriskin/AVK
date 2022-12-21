import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from database.models import create_tables, drop_tables, User, Photo, Favourite, BlackList
from database.db_config import DSN


def create_connection():
    engine = sq.create_engine(DSN)
    return engine


class Vkinder:
    def __init__(self):
        self.engine = create_connection()
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def create_new_tables(self):
        """Добавление новых таблиц"""
        create_tables(self.engine)

    def drop_old_tables(self):
        """Удаление заполненных таблиц"""
        drop_tables(self.engine)

    def add_user_data(self, data: list):
        """Добавление информации о пользователе в базу данных"""
        for record in data:
            self.session.add(
                User(
                    user_id=record["id"],
                    first_name=record["first_name"],
                    last_name=record["last_name"],
                )
            )
        self.session.commit()

    def get_user(self, id: int):
        """Получение пользователя из базы данных"""
        return self.session.query(User).filter(User.id == id).first()

    def user_search(self, user_id: int):
        """Поиск пользователя в таблице User по user_id"""
        return self.session.query(User).filter(User.user_id == user_id).first()

    def get_all_user(self):
        """Получение всех пользователей из базы данных"""
        return self.session.query(User).all()

    def add_photo_urls(self, user_id: int, urls: list):
        """Добавление фотографии в базу данных"""
        for url in urls:
            self.session.add(
                Photo(
                    user_id=user_id,
                    url=url,
                )
            )
        self.session.commit()

    def get_photo_urls(self, user_id: int):
        """Получение фотографий из базы данных"""
        return self.session.query(Photo).filter(Photo.user_id == user_id).all()

    def add_to_favourite(self, user_id: int, first_name, last_name):
        """Добавление пользователя в таблицу Favourite"""
        self.session.add(
            Favourite(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
            )
        )
        self.session.commit()

    def check_favourite(self, user_id: int):
        """Проверка на наличие пользователя в таблице Favourite"""
        if (
            self.session.query(Favourite)
            .filter(Favourite.user_id == user_id)
            .first()
            is None
        ):
            return False
        else:
            return True

    def get_favourite(self):
        """Получение всех пользователей, добавленных в Favourite"""
        return self.session.query(Favourite).all()

    def add_to_blacklist(self, user_id: int, first_name, last_name):
        """Добавление пользователя в чёрный список"""
        self.session.add(
            BlackList(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
            )
        )
        self.session.commit()

    def check_blacklist(self, user_id: int):
        """Проверка на наличие пользователя в чёрном списке"""
        if (
            self.session.query(BlackList)
            .filter(BlackList.user_id == user_id)
            .first()
            is None
        ):
            return False
        else:
            return True

    def get_blacklist(self):
        return self.session.query(BlackList).all()