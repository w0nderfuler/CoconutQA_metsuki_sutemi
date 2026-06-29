import pytest
from sqlalchemy.orm import Session
import allure
from Cinescope.DataGeneratorMovies import MovieData
from Cinescope.db_requester.models import AccountTransactionTemplate

@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами")
class TestAccountTransactionTemplate:

    @allure.story("Корректность перевода денег между двумя счетами")
    @allure.description("""
        Этот тест проверяет корректность перевода денег между двумя счетами.
        Шаги:
        1. Создание двух счетов: Stan и Bob.
        2. Перевод 200 единиц от Stan к Bob.
        3. Проверка изменения балансов.
        4. Очистка тестовых данных.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "metsuki_sutemi")
    @allure.title("Тест перевода денег между счетами 200 рублей")
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.bd
    def test_accounts_transaction_template(self, db_session: Session):
        # ====================================================================== Подготовка к тесту
        with allure.step("Создание текстовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(**MovieData.generate_account_transaction_data("Stan", 1000))
            bob = AccountTransactionTemplate(**MovieData.generate_account_transaction_data("Bob", 500))

            db_session.add_all([stan, bob])
            db_session.commit()

        @allure.step("Функция перевода денег: transfer_money")
        @allure.description("""
                   функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
                   и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
                   """)
        def transfer_money(session, from_account, to_account, amount):
            with allure.step("Получаем счета"):
                from_account = (
                session.query(AccountTransactionTemplate)
                .filter_by(user=from_account)
                .one()
            )
                to_account = (
                session.query(AccountTransactionTemplate)
                .filter_by(user=to_account)
                .one()
            )
            with allure.step("Проверяем, что на счете достаточно средств"):
                if from_account.balance < amount:
                    raise ValueError("Недостаточно средств на счете")

            with allure.step("Выполняем перевод"):
                from_account.balance -= amount
                to_account.balance += amount
            with allure.step("Сохраняем изменения"):
                session.commit()

        # ====================================================================== Тест
        with allure.step("Проверяем начальные балансы"):
            assert stan.balance == 1000
            assert bob.balance == 500

        try:
            with allure.step("Выполняем перевод 200 единиц от stan к bob"):
                transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

            db_session.refresh(stan)
            db_session.refresh(bob)

            with allure.step("Проверяем, что балансы изменились"):
                assert stan.balance == 800
                assert bob.balance == 700
        except Exception as error:
            with allure.step("ОШИБКА откаты транзакции"):
                db_session.rollback()
            pytest.fail(f"Ошибка при переводе денег: {error}")
        finally:
            with allure.step("Удаляем данные для тестирования из базы"):
                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()
