import requests
import json


class ApiClass:
    """ Класс для работы с OzonApi """

    def __init__(self, url: str, client_id: int, api_key: str):

        self.client_id = client_id
        self.api_key = api_key
        self.url = url

        headers = {'POST': 'HTTP/1.1',
                   'Host': f'{self.url}',
                   'Client-Id': f'{self.client_id}',
                   'Api-Key': f'{self.api_key}',
                   'Content-Type': 'application/json'}

        self.headers = headers

    def _response(self, func_url: str, data: dict):

        r = requests.post(f'https://{self.url}{func_url}', headers=self.headers, data=json.dumps(data))
        if r.status_code == 200:
            return r.json()
        else:
            return "Error"

    def category_tree(self, category_id: int) -> dict:
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

    def category_atribute(self, category_id: int) -> dict:
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

        data = {'items': [{'category_id': 17028760, 'price': 'old_price', 'vat': '0.2', 'vendor': 'MOTUL', 'dimension_unit': 'mm', 'weight_unit': 'g', 'height': 130, 'depth': 230, 'width': 90, 'images': [{'file_name': 'https://motul.store/upload/resize_cache/iblock/8f5/700_700_1/6100-SYN-CLEAN-5W30-1L.png', 'defaut': True}], 'attributes': [{'id': 7194, 'value': '1'}, {'id': 8084, 'value': '1095'}, {'id': 9048, 'value': '6100 SYN-CLEAN 5W30'}, {'id': 4382, 'value': ' x  x '}, {'id': 4383, 'value': ''}, {'id': 4386, 'collection': ['96']}, {'id': 4389, 'value': '10'}, {'id': 7206, 'collection': ['7']}, {'id': 7290, 'collection': '2'}, {'id': 7284, 'value': '25'}, {'id': 7286, 'value': '4'}], 'weight': 980, 'offer_id': '107947', 'old_price': '666', 'name': 'Моторные масла Motul 6100 SYN-CLEAN 5W30'}]}

        return self._response(func_url, data)

    def import_status(self, task_id: int) -> int:
        """ Статус добавления товара """

        func_url = "/v1/product/import/info"

        data = {
            "task_id": task_id
        }

        return self._response(func_url, data)

    def product_static(self, product_id: int, sku: int) -> dict:
        """ Возвращает информацию о товаре по его идентификатору. Если указать только offer_id,
        то в результатах поиска будут только товары вашего магазина,
        даже если у другого продавца есть такие же артикулы """

        func_url = "/v2/product/info"

        data = {"offer_id": " ",
                "product_id": product_id,
                "sku": sku}

        return self._response(func_url, data)
    
    def product_info_list(self, product_id):
        """ Позволяет получить список товаров. """

        func_url = '/v1/product/list'
        data = {"filter":
                {
                    "offer_id": ["1255959"],
                    "product_id": [product_id],
                    "visibility": "ALL"
                }, }

        return self._response(func_url, data)
