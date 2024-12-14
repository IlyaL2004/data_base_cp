-- Добавление продуктов в таблицу Products с размерами упаковок (длина, ширина, высота)
INSERT INTO public.categories ("name") VALUES
	 ('кофе'),
	 ('вещи');

INSERT INTO public.products (barcode,"name",package_size,weight,category_id) VALUES
	 ('123456789012','Эфиопский кофе','0.1*0.05*0.01',50.0,1),
	 ('234567890123','Магнит в виде кофе','0.25*0.25*0.35',500.0,2),
	 ('345678901234','Бразильский кофе','0.2*0.15*0.05',150.0,1),
	 ('456789012345','Колумбийский кофе','0.2*0.1*0.02',100.0,1),
	 ('567890123456','Росскийский кофе','0.15*0.1*0.05',150.0,1),
	 ('678901234567','Брелок в виде кофе','0.2*0.2*0.3',1000.0,2),
	 ('789012345678','Подушка в виде кофе','0.25*0.25*0.35',500.0,2),
	 ('890123456789','Футболка с принтом кофе','0.2*0.2*0.3',250.0,2),
	 ('901234567890','Наклеки с кофе','0.15*0.1*0.05',200.0,2),
	 ('012345678901','Немецкое кофе','0.1*0.05*0.01',55.0,1);

INSERT INTO public.suppliers ("name",phone,address) VALUES
	 ('ООО "ПродуктыПлюс"','+7 495 123-45-67','Москва, ул. Ленина, д. 10'),
	 ('ЗАО "Вкусные Дары"','+7 812 234-56-78','Санкт-Петербург, ул. Пушкина, д. 20'),
	 ('ИП "Сити Продукт"','+7 831 345-67-89','Нижний Новгород, ул. Советская, д. 15'),
	 ('ООО "Питание и Удовольствие"','+7 863 456-78-90','Ростов-на-Дону, ул. Гагарина, д. 5'),
	 ('ЗАО "Сладкие Моменты"','+7 343 567-89-01','Екатеринбург, ул. Мира, д. 12'),
	 ('ИП "Товары для всех"','+7 495 678-90-12','Москва, ул. Тверская, д. 45'),
	 ('ООО "Свежие Продукты"','+7 831 789-01-23','Нижний Новгород, ул. Ленина, д. 7'),
	 ('ЗАО "Экологические продукты"','+7 863 890-12-34','Ростов-на-Дону, ул. Нахимова, д. 30'),
	 ('ИП "Качество и Удобство"','+7 343 901-23-45','Екатеринбург, ул. Белинского, д. 25'),
	 ('ООО "Еда с Любовью"','+7 812 012-34-56','Санкт-Петербург, ул. Некрасова, д. 8');


INSERT INTO public.prices (barcode,start_date,end_date,price) VALUES
	 ('123456789012','2024-11-01',NULL,50.0),
	 ('234567890123','2024-11-01',NULL,45.0),
	 ('345678901234','2024-11-01',NULL,60.0),
	 ('456789012345','2024-11-01',NULL,80.0),
	 ('567890123456','2024-11-01',NULL,70.0),
	 ('678901234567','2024-11-01',NULL,90.0),
	 ('789012345678','2024-11-01',NULL,50.0),
	 ('890123456789','2024-11-01',NULL,100.0),
	 ('901234567890','2024-11-01',NULL,120.0),
	 ('012345678901','2024-11-01',NULL,55.0);

INSERT INTO public.deliveries (supplier_id,delivery_date) VALUES
	 (1,'2023-09-01'),
	 (2,'2023-09-05'),
	 (3,'2023-09-15');

INSERT INTO public.delivery_contents (delivery_id,barcode,quantity) VALUES
	 (1,'123456789012',5),
	 (1,'234567890123',6),
	 (2,'345678901234',5),
	 (2,'456789012345',5),
	 (2,'567890123456',5),
	 (3,'678901234567',5),
	 (3,'789012345678',5),
	 (3,'890123456789',5),
	 (3,'901234567890',5),
	 (3,'012345678901',5);

