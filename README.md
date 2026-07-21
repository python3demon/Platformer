# Platformer

<div align="center">

<img src="assets/logo.png" alt="Logo" width="400">

**Динамичный 2D-платформер с кучей уровней, монеток и скрытых отсылок!**

[![Version 1.0.0](https://img.shields.io/badge/version-0.2.0--alpha-orange.svg)](https://github.com/python3demon/Platformer)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg?logo=python&logoColor=white)](https://www.python.org/downloads/latest/python3.14/)
[![Pygame 2.6.1](https://img.shields.io/badge/pygame-2.6.1-yellow.svg)](https://www.pygame.org/)
[![Linux](https://img.shields.io/badge/platform-linux-A9A9A9.svg?logo=linux&logoColor=white)](https://linux.org)
[![Windows](https://img.shields.io/badge/platform-windows-A9A9A9.svg?logo=windows&logoColor=white)](https://www.microsoft.com/ru-ru/software-download/windows11)

</div>


## О игре
**Platformer Game** — это классический 2D-платформер на движке Pygame, где вам предстоит пройти сквозь огонь, воду и **67 хардкорных уровней**. Здесь нет заумного лора или драматичного сюжета — только чистый кайф, затягивающий геймплей и проверка вашей реакции на прочность!

### Ключевые особенности:
* **Встроенный Sandbox-редактор**: Стройте свои уровни прямо во время игры и сохраняйте их в один клик.

> [!IMPORTANT]
> **Текущая версия:** `v0.1.0-dev` (В разработке)  
> Проект находится на стадии раннего архитектурного прототипа (Alpha). Полностью готова базовая структура игровых экранов, переписан физический движок под новую сетку и встроен визуальный редактор карт для разработчика.

### Что уже сделано в версии `v0.1.0-dev`:
- **Система экранов (Игровые стейты)**: Полноценное разделение на Главное меню, Выбор уровней, Настройки и Игровой процесс.
- **Сохранения через JSON**: Автоматическое чтение и запись профиля игрока (`name` и `level`) через файл `data.json`.
- **Встроенный редактор уровней**: Генерация блоков пола (ЛКМ) и лавы (ПКМ) прямо на лету во время игры с автоматическим экспортом по нажатию `Enter`.
- **Физический движок 64х64**: Откалиброванные раздельные коллизии по осям X и Y, стабильная гравитация и прыжки без ложных смертей.

### План разработки (To-Do):
- [x] Разработка базового прототипа интерфейса: меню, уровни, game (`v0.1.0-alpha`)
- [x] Перевод карты и игрока на сетку `64x64` (`v0.2.0-alpha`)
- [x] Калибровка коллизий с лавой и прыжков (`v0.2.1-alpha`)
- [x] Перенос процедурного кода из `main.py` в ООП-классы (Менеджер Стейтов) (`v0.2.2-alpha`)
- [x] Избавление от глобальных переменных и изоляция логики сохранения (`v0.2.3-alpha`)
- [x] Аннотация типов и рефакторинг структуры кода (`v0.2.4-alpha`)
- [ ] Смерть от падения в бездну (`player.rect.top >= height`) (`v0.2.5`)
- [ ] Автоматический переход на следующий уровень при выходе за правый край (`v0.2.6`)

### Управление

* `A` / `D` — Движение влево / вправо (медленно, но уверенно)
* `W` — Прыжок (высота — ровно 2 блока, полный контроль в воздухе!)
* `LMB` (Левая кнопка мыши) / `F` — Огонь лазером издалека

## Installation & Launch (For Users)

### Windows
Убедитесь, что у вас установлен [Python 3.14](https://www.python.org/downloads/latest/python3.14/)

1. Скачайте репозиторий архивом и распакуйте его на компьютер.
2. Зайдите в папку `install\Windows`.
3. Дважды кликните по файлу `install.bat`. 
4. Скрипт сам установит все зависимости и скомпилирует исходный код в исполняемый `.exe` файл. Игру можно будет найти и запустить в появившейся папке `Platformer`.

> [!WARNING]
> **Важное примечание:** Не перемещайте файлы по отдельности. Перемещайте игру целиком, перенося всю папку `Platformer`.
---

## 💻 Installation & Launch (For Programmers)

### Linux
```bash
# Клонируем репозиторий и переходим в папку проекта
git clone https://github.com/python3demon/Platformer.git
cd Platformer

# Создаем и активируем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip3 install -r requirements.txt

# Запуск игры
python3 main.py
```

### Windows
Для быстрой автоматической настройки вы можете просто запустить готовый файл `install.bat` из папки `install\Windows`, либо выполнить команды ручной настройки ниже.

```cmd
:: Клонируем репозиторий и переходим в папку проекта
git clone https://github.com/python3demon/Platformer.git
cd Platformer

:: Создаем и активируем виртуальное окружение
python -m venv venv
call venv\Scripts\activate.bat

:: Устанавливаем зависимости
pip install -r requirements.txt

:: Запуск игры из исходного кода
python main.py
```
Если же нужен готовый один .exe файл без консоли:
```cmd
pyinstaller --noconfirm --onefile --windowed --name "Platformer" main.py
```
Игра будет лежать **в папке `dist`**.

## Стек технологий
* **Language:** Python 3.14+
* **Library:** Pygame CE 2.6.1+
* **Environment:** Virtualenv

