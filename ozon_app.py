import requests
import json


class ApiClass:
    """ Класс для работы с OzonApi """

    def __init__(self, url, client_id, api_key):

        self.client_id = client_id
        self.api_key = api_key
        self.url = url

        headers = {'POST': 'HTTP/1.1',
                   'Host': f'{self.url}',
                   'Client-Id': f'{self.client_id}',
                   'Api-Key': f'{self.api_key}',
                   'Content-Type': 'application/json'}

        self.headers = headers

    def _response(self, func_url, data):

        r = requests.post(f'https://{self.url}{func_url}', headers=self.headers, data=json.dumps(data))
        if r.status_code == 200:
            return r.json()
        else:
            return "Error"

    def category_tree(self, category_id):
        """ Получение категорий в виде дерева.
        Создание товаров доступно только в категориях последнего уровня, соответственно вам необходимо
        сопоставить именно эти категории с категориями своей площадки.Категории не создаются
        по запросу пользователя."""

        func_url = '/v1/category/tree'
        data = {
            "category_id": category_id,
            "language": "EN"
        }

        return self._response(func_url, data)

    def category_atribute(self, category_id):
        """ Возвращает список характеристик категории по ее идентификатору.
        У некоторых категорий есть системные характеристики, которые скрыты от пользователя,
        но по ним товары объединяются в группы. Например, "Название модели" для категорй "Одежда" и "Обувь" """

        func_url = "/v2/category/attribute"
        data = {
            "attribute_type": "required",
            "category_id": category_id,
            "language": "RU"}

        return self._response(func_url, data)

    def import_product(self):
        """Метод для загрузки товаров. В одном запросе можно передать до 1000 товаров.
        Возвращает task_id"""

        func_url = "/v2/product/import"

        data = {}

        return (self._response(func_url, data))['result']['task_id']

    def import_status(self, task_id):
        """ Статус добавления товара """

        func_url = "/v1/product/import/info"

        data = {
            "task_id": task_id
        }

        return self._response(func_url, data)

    def product_static(self, product_id, sku):
        """ Возвращает информацию о товаре по его идентификатору. Если указать только offer_id,
        то в результатах поиска будут только товары вашего магазина,
        даже если у другого продавца есть такие же артикулы """

        func_url = "/v2/product/info"

        data = {"offer_id": " ",
                "product_id": product_id,
                "sku": sku}

        return self._response(func_url, data)
