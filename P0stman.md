1. Перевірка списку товарів
GET http://localhost:8000/product
2. Сортування від А до Я за назвою GET http://localhost:8000/product?sort_by=name&order=asc
3. Сортування від Я до А за назвою
GET http://localhost:8000/product?sort_by=name&order=desc
4. Сортування за ціною
GET http://localhost:8000/product?sort_by=price&order=asc
5. Сортування за категорією
GET http://localhost:8000/product?sort_by=category&order=asc
6. Фільтрація за категорією
GET http://localhost:8000/product?category_id=1

7. Фільтрація за ціною
GET http://localhost:8000/product?price_from=100&price_to=50000

8. Пагінація
GET http://localhost:8000/product?page=1&limit=20

9. Усі параметри разом
GET http://localhost:8000/product?category_id=1&price_from=100&price_to=50000&sort_by=price&order=asc&page=1&limit=20

Тестова - INSERT INTO category
(name, description, parent_category_id, status, date_added, date_modify)
VALUES
('Електроніка', 'Електронні пристрої', NULL, 1, NOW(), NOW());

INSERT INTO category
(name, description, parent_category_id, status, date_added, date_modify)
VALUES
('Смартфони', 'Мобільні телефони', 1, 1, NOW(), NOW()),
('Комп’ютери', 'Комп’ютерна техніка', 1, 1, NOW(), NOW()),
('Аксесуари', 'Аксесуари для техніки', 1, 1, NOW(), NOW());

10. Post http://localhost:8000/product
{
  "name": "iPhone 15 Pro Max",
  "categories": [2],
  "attributes": [
    {
      "name": "Колір",
      "value": "Natural Titanium"
    },
    {
      "name": "Пам'ять",
      "value": "256 GB"
    },
    {
      "name": "Дисплей",
      "value": "6.7 дюйма"
    }
  ],
  "images": [
    {
      "image": "catalog/iphone/15-pro-max-1.jpg",
      "sort_order": 0
    },
    {
      "image": "catalog/iphone/15-pro-max-2.jpg",
      "sort_order": 1
    }
  ]
}
11. Post http://localhost:8000/product/16 {
  "name": "iPhone 15 Pro Max",
  "categories": [2],
  "attributes": [
    {
      "name": "Колір",
      "value": "Natural Titanium"
    },
    {
      "name": "Пам'ять",
      "value": "256 GB"
    },
    {
      "name": "Дисплей",
      "value": "6.7 дюйма"
    }
  ],
  "images": [
    {
      "image": "catalog/iphone/15-pro-max-1.jpg",
      "sort_order": 0
    },
    {
      "image": "catalog/iphone/15-pro-max-2.jpg",
      "sort_order": 1
    }
  ]
}
12. Patch http://localhost:8000/product/16
{
  "name": "iPhone 15 Pro Max Updated",
  "price": 45999,
  "status": 1
}