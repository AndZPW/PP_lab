import undecorated
from pytest_mock import mocker

from app import user_by_nick, delete_user_by_nick, User, Budget, user, getUserByName, Account, budget, budget_by_id, \
    get_budget_by_id, delete_budget_by_id, account, account_by_id, get_account_by_id, delete_account_by_id, \
    init_database, get_user_roles, verify_password, login


class TestAPI:

    def test_login(self, mocker):
        undecorated_login = undecorated.undecorated(login)
        result = undecorated_login()
        assert result == ({'message': 'you login successful'}, 200)

    # User--------------------------------------------------------------
    def test_user_add_to(self, mocker):
        mocker.patch("app.db.session.add", return_value=True)
        mocker.patch("app.db.session.commit", return_value=True)
        result = User.add_to(User())

    def test_find_by_username(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = True
        result = User.find_by_username("sofia")
        assert result is True

    def test_user_find_by_phone(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = True
        result = User.find_by_phone("09876")
        assert result is True

    def test_user_find_by_email(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = True
        result = User.find_by_email("rrg@jj")
        assert result is True

    def test_user_find_by_id(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = True
        result = User.find_by_id("6")
        assert result is True

    def test_user_list(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.all.return_value = [User()]
        result = User.user_list()
        assert result == {'users': [{'email': None,
                                     'firstName': None,
                                     'id': None,
                                     'lastName': None,
                                     'password': None,
                                     'username': None}]}

    def test_generate_hash(self, mocker):
        mocker.patch('passlib.hash.argon2.hash', return_value=True)
        result = User.generate_hash("hhh")
        assert result == True

    def test_verify_hash(self, mocker):
        mocker.patch('passlib.hash.argon2.verify', return_value=True)
        result = User.verify_hash("hhh", "h")
        assert result == True

    def test_verify_password(self, mocker):
        mocker.patch('app.User.find_by_username', return_value=User())
        mocker.patch('passlib.hash.argon2.verify', return_value=True)
        undecorated_verify_password = undecorated.undecorated(verify_password)
        result = undecorated_verify_password("Sofia", "hh")
        assert result == 'Sofia'

    def test_get_user_roles(self, mocker):
        mocker.patch('app.User.find_by_username', return_value=User())
        undecorated_get_user_roles = undecorated.undecorated(get_user_roles)
        result = undecorated_get_user_roles("Sofia")
        assert result == None

    # Account---------------------------------------------------
    def test_account_add_to(self, mocker):
        mocker.patch("app.db.session.add", return_value=True)
        mocker.patch("app.db.session.commit", return_value=True)
        result = Account.add_to(Account())

    def test_account_find_by_id(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = True
        result = Account.find_by_id("5")
        assert result is True

    # Budget--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def test_budget_add_to(self, mocker):
        mocker.patch("app.db.session.add", return_value=True)
        mocker.patch("app.db.session.commit", return_value=True)
        result = Budget.add_to(Budget())

    def test_budget_find_by_record_id(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = True
        result = Budget.find_by_record_id("5")
        assert result is True

    # ---------------------------------------------------------------------
    def test_user(self, mocker):
        mocker.patch("flask_restful.reqparse.RequestParser.parse_args",
                     return_value={'id': 1, 'username': "sonya", 'firstName': "Sofia", 'lastName': "Tkach",
                                   'email': "sofia@gmail.com", 'password': "123"})
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        mocker.patch('passlib.hash.argon2.hash', return_value=True)
        mocker.patch('app.User.add_to', return_value=True)
        result = user()
        assert result == ({'message': 'everything is good'}, 200)

    def test_user_error(self, mocker):
        mocker.patch("flask_restful.reqparse.RequestParser.parse_args",
                     return_value={'id': "hello", 'username': "sonya", 'firstName': "Sofia", 'lastName': "Tkach",
                                   'email': "sofia@gmail.com", 'password': "123"})
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        mocker.patch('passlib.hash.argon2.hash', return_value=True)
        mocker.patch('app.User.add_to', return_value=True)
        result = user()
        assert result == ({'message': 'error'}, 500)

    def test_getUserByName(self, mocker):
        mocker.patch('app.User.find_by_username', return_value=User())
        undecorated_getUserByName = undecorated.undecorated(getUserByName)
        result = undecorated_getUserByName("Sofia")
        assert result == ({'email': None,
                           'firstName': None,
                           'id': None,
                           'lastName': None,
                           'password': None,
                           'username': None},
                          200)

    # ---------------------------------------------------------------------
    def test_user_by_nick(self, mocker):
        mocker.patch("flask_restful.reqparse.RequestParser.parse_args",
                     return_value={'id': 1, 'username': "sonya", 'firstName': "Sofia", 'lastName': "Tkach",
                                   'email': "sofia@gmail.com", 'password': "123"})
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.update.return_value = True
        mocker.patch("app.db.session.commit", return_value=True)

        undecorated_user_by_nick = undecorated.undecorated(user_by_nick)
        result = undecorated_user_by_nick("Sofia")
        assert result == {'message': 'item with Sofia is up to date'}

    def test_delete_user_by_nick(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = True
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.delete.return_value = True
        mocker.patch("app.db.session.commit", return_value=True)
        undecorated_user_by_nick = undecorated.undecorated(delete_user_by_nick)
        result = undecorated_user_by_nick("Sofia")
        assert result == ({'message': 'user with Sofia was deleted'}, 200)

    def test_delete_user_by_nick_2(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = None
        undecorated_user_by_nick = undecorated.undecorated(delete_user_by_nick)
        result = undecorated_user_by_nick("Sofia")
        assert result == ({'message': 'Something went wrong'}, 404)

        # ---------------------------------------------------------------------

    def test_budget(self, mocker):
        mocker.patch("flask_restful.reqparse.RequestParser.parse_args",
                     return_value={'title': "hh", 'record_id': "5", 'name_user': "Sofia", 'income': "8",
                                   'outcome': "6", 'date': "12.03.22", 'password': "2123", "available_balance": "9",
                                   "userId": "8"})
        mocker.patch('app.Budget.add_to', return_value=True)
        undecorated_budget = undecorated.undecorated(budget)
        result = undecorated_budget()
        # result = budget()
        assert result == ({"message": "everything is good"}, 200)

    def test_budget_error(self, mocker):
        mocker.patch("flask_restful.reqparse.RequestParser.parse_args",
                     return_value={'title': "hh", 'record_id': "5jbgjbj", 'name_user': "Sofia", 'income': "8",
                                   'outcome': "6", 'date': "12.03.22", 'password': "2123", "available_balance": "9",
                                   "userId": "8"})
        mocker.patch('app.Budget.add_to', return_value=True)
        undecorated_budget = undecorated.undecorated(budget)
        result = undecorated_budget()
        assert result == ({'message': 'error'}, 500)

    def test_budget_by_id(self, mocker):
        mocker.patch("flask_restful.reqparse.RequestParser.parse_args",
                     return_value={'title': "hh", 'record_id': "5", 'name_user': "Sofia", 'income': "8",
                                   'outcome': "6", 'date': "12.03.22", 'password': "2123", "available_balance": "9",
                                   "userId": "8"})
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.update.return_value = True
        mocker.patch("app.db.session.commit", return_value=True)
        undecorated_budget_by_id = undecorated.undecorated(budget_by_id)
        result = undecorated_budget_by_id("5")
        assert result == {'message': 'item with 5 is up to date'}


    def test_get_budget_by_id(self, mocker):
        mocker.patch('app.Budget.find_by_record_id', return_value=Budget())
        undecorated_get_budget_by_id = undecorated.undecorated(get_budget_by_id)
        result = undecorated_get_budget_by_id(5)
        assert result == ({'available_balance': None,
                           'date': None,
                           'income': None,
                           'name_user': None,
                           'outcome': None,
                           'password': None,
                           'record_id': None,
                           'title': None,
                           'userId': None},
                          200)

    def test_delete_budget_by_id(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = True
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.delete.return_value = True
        mocker.patch("app.db.session.commit", return_value=True)
        undecorated_budget_by_id = undecorated.undecorated(delete_budget_by_id)
        result = undecorated_budget_by_id("6")
        assert result == ({'message': 'user with 6 was deleted'}, 200)

    def test_delete_budget_by_id_2(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = None
        undecorated_budget_by_id = undecorated.undecorated(delete_budget_by_id)
        result = undecorated_budget_by_id("Sofia")
        assert result == ({'message': 'Something went wrong'}, 404)

    # ---------------------------------------------------------------------
    def test_account(self, mocker):
        mocker.patch("flask_restful.reqparse.RequestParser.parse_args",
                     return_value={'id': "5", 'number': "5", 'cv': "666", 'password': "8900",
                                   'available_balance': "677", 'userId': "13"})
        mocker.patch('app.Account.add_to', return_value=True)
        undecorated_account = undecorated.undecorated(account)
        result = undecorated_account()
        assert result == ({"message": "everything is good"}, 200)

    def test_account__error(self, mocker):
        mocker.patch("flask_restful.reqparse.RequestParser.parse_args",
                     return_value={'id': "5fjfjf", 'number': "5", 'cv': "666", 'password': "8900",
                                   'available_balance': "677", 'userId': "13"})
        mocker.patch('app.Account.add_to', return_value=True)
        undecorated_account = undecorated.undecorated(account)
        result = undecorated_account()
        assert result == ({'message': 'error'}, 500)

    def test_account_by_id(self, mocker):
        mocker.patch("flask_restful.reqparse.RequestParser.parse_args",
                     return_value={'id': "5", 'number': "5", 'cv': "666", 'password': "8900",
                                   'available_balance': "677", 'userId': "13"})
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.update.return_value = True
        mocker.patch("app.db.session.commit", return_value=True)
        undecorated_account_by_id = undecorated.undecorated(account_by_id)
        result = undecorated_account_by_id("5")
        assert result == {'message': 'item with 5 is up to date'}

    def test_get_account_by_id(self, mocker):
        mocker.patch('app.Account.find_by_id', return_value=Account())
        undecorated_get_account_by_id = undecorated.undecorated(get_account_by_id)
        result = undecorated_get_account_by_id(5)
        assert result == ({'available_balance': None,
                           'cv': None,
                           'id': None,
                           'number': None,
                           'password': None,
                           'userId': None},
                          200)

    def test_delete_account_by_id(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = True
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.delete.return_value = True
        mocker.patch("app.db.session.commit", return_value=True)
        undecorated_account_by_id = undecorated.undecorated(delete_account_by_id)
        result = undecorated_account_by_id("6")
        assert result == ({'message': 'account with 6 was deleted'}, 200)

    def test_delete_account_by_id_2(self, mocker):
        patch = mocker.patch('flask_sqlalchemy.model._QueryProperty.__get__')
        patch.return_value.filter_by.return_value.first.return_value = None
        undecorate_account_by_id = undecorated.undecorated(delete_account_by_id)
        result = undecorate_account_by_id("6")
        assert result == ({'message': 'Something went wrong'}, 404)

    def test_init_database(self, mocker):
        mocker.patch("app.db.drop_all", return_value=True)
        mocker.patch("app.db.create_all", return_value=True)
        mocker.patch("app.db.session.commit", return_value=True)
        result = init_database()
