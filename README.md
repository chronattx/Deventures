# DEVENTURES
#### Игра о фэнтези-страданиях.
## Авторы
Степан Максимычев (ZuttoZutto) отвечает за дизайн, музыку и их внедрение.

Дмитрий Николаев (kapusta0148) отвечает за интерфейсы.

Алексей Карташов (kartash) отвечает за внутренние механики.

## Идея игры
Кратко, Deventures (Depressing adventures) - игра-платформер в жанре RPG с видом Top-Down. Игрок проходит уровни,
сражаясь и учавствуя в диалогах, и каждый элемент игры заставляет его испытывать душевные муки. 

## Описание игровой стратегии
Часто основной целью игр является убийство времени или получение удовольствия. Аватары игрока являются идеалами, делают
то, что человек хочет в реальной жизни, но не имеет возможности. Мы считаем это неправильным, такие игры заставляют
человека деградировать. Поэтому главные герои нашей игры страдают, а диалоги, сюжет и битвы должны иметь смысл.

Игра разбита на уровни, каждый уровень представляет собой локацию. В локации есть комнаты, между которыми можно ходить.
Внутри комнаты есть сущности: герой, враги, мирные, объекты. В одной из комнат есть босс, победив которого можно перейти
на следующий уровень.

Герой - персонаж, которым управляет игрок, враги - управляемые своими специальными алгоритмами персонажи, атакующие
героя, мирные - персонажи, с которыми можно вести диалог. У каждого из них может быть оружие (отдельный класс), с
помощью которого можно наносить урон окружающим сущностям.

**Функции:**

1. Локации, по которым можно ходить
2. Механики боя с врагами
3. Диалоги с npc
4. Зависимость концовки от действий

**Фишки:**

1. Проработанный сюжет 
2. Механики заточенные под раскрытие идеи игры
3. Красивые спрайты и фоны

## Установка
Для установки приложения:
1. Распакуйте архив с файлами в нужную вам директорию.
2. Откройте терминал в директории проекта.
3. Выполните команду для установки зависимостей.
```commandline
pip install -r requirements.txt
```
4. Запустите приложение, открыв файл `start_menu.py`
5. Для удобной последующей работой с ним можно создать ярлык.

## Описание конечных технологий
+ `python3`: Основной язык программирования для реализации игры.
+ `pygame`: Библиотека для разработки основных механик игры.
+ `pygame_light2d`: Модуль pygame для создания света.
+ `aseprite`: Приложение для рисования картинок.
+ Различные нейросети для создания картинок.

## Описание структуры классов программы
+ Класс `GameObject` предназначен для отображения статичных объектов на карте.
+ Класс `Weapon` используется для реализации механик и отображения оружия.
+ Класс `BaseObject` - базовый класс для работы с объектами, имеющими хитбокс.
+ Класс `BaseCharacter` - класс, наследуемый от `BaseObject`, имеющий общие методы для главного героя, врага и мирного.
+ Класс `Hero` - класс, наследуемый от `BaseCharacter`, реализует механику героя.
+ Класс `Enemy` - класс, наследуемый от `BaseCharacter`, реализует механику врага.
+ Класс `Peaceful` - класс, наследуемый от `BaseCharacter`, реализует механику мирного.
+ Класс `Objects` используется для хранения в нём экземпляра героя и NPC.
+ Класс `Camera` реализует перемещение карты в зависимости от положения игрока.
+ Класс `Room` используется для отрисовки комнаты и обработки стен.
+ Класс `NPC` используется для отрисовки и реализации механики NPC.
+ Класс `DialogBox` используется для отрисовки и обработки диалогов.

## [Презентация](https://docs.google.com/presentation/d/1yTa5Li_EemPQd8RLBC_09uj5QtDuH5mrqvz_7m0jeJk/edit?usp=sharing)
## [Видео](https://drive.google.com/file/d/1ce_KdhqEH6XWFaxF512fQltq1UlBFYEJ/view?usp=sharing)
