## Наша обученная модель

https://drive.google.com/file/d/1sPbg-pHksOjTzGYFD-WcYleWIvVlzbxx/view?usp=sharing

## Зависимости

- Docker
- NVIDIA GPU с установленными драйверами и поддержкой CUDA

## Использование

1. Сначала установите Docker и драйверы NVIDIA GPU на вашем компьютере. 
Для этого проекта используется контейнер с версией CUDA 12.4.1.

2. Склонируйте репозиторий:

```bash
git clone https://github.com/sherstpasha/questions_sentement_bot
cd multi-task-bert
```

3. Соберите Docker контейнер:

```bash
docker build -t multi_task_bert .
```

4. Запустите контейнер с графическим процессором (при необходимости монтируйте папку с данными):

```bash
docker run --gpus all -it -v /путь/к/вашей/папке:/app/mounted_folder multi_task_bert
```

5. Теперь, когда вы находитесь в контейнере, вы можете запустить `train.py` с помощью следующей команды, чтобы начать обучение модели:

```bash
python3.10 train.py --epoch=100 --lr_start=5e-5 --train_data_path="mounted_folder/train_file.csv"
```

6. После окончания обучения в докере сохраняется модель с названием "best_model.pth". Чтобы перенести ее на вашу систему, выполните следующую команду `docker cp`, указав путь к файлу `best_model.pth` в контейнере и путь на вашей системе, куда вы хотите скопировать файл.

Вот пример:

```bash
docker cp <container_id>:/app/best_model.pth .
```

Где `<container_id>` - это идентификатор вашего контейнера, а `/путь/на/вашей/системе/` - путь к папке на вашей системе, куда вы хотите скопировать файл `best_model.pth`.

## Важно

Убедитесь, что ваши обучающие данные доступны в папке `/app` внутри контейнера перед запуском `train.py`.

---

### Описание файла CSV для обучения

Файл CSV с набором данных должен содержать следующие столбцы:

1. **is_relevant**: Бинарное значение (0 или 1), указывающее, является ли текст релевантным для какого-либо заданного критерия или вопроса.

2. **object**: Бинарное значение (0 или 1), определяющее объект или категорию, к которой относится текст (например, 1 может указывать на наличие объекта, а 0 - на его отсутствие).

3. **is_positive**: Бинарное значение (0 или 1), обозначающее, является ли текст положительным или отрицательным по отношению к какому-либо аспекту или контексту.

4. **text**: Строковое значение, содержащее текстовые данные или вопросы, требующие анализа или классификации. Все вопросы и ответы собраны в один абзац. 

Пример:

| is_relevant | object | is_positive | text                                                  |
|-------------|--------|-------------|-------------------------------------------------------|
| 1           | 0      | 1           | Что вам больше всего понравилось в теме вебинара? - Вебинар был очень познавательным. Какие вопросы остались без ответа после вебинара? - У меня остались вопросы по применению алгоритмов в реальной жизни. Какой формат вебинара вам было бы интересно видеть? - Мне больше всего подходит формат с презентациями и демонстрациями кода. Есть ли у вас предложения по улучшению вебинара? - Я предлагаю добавить больше практических заданий для участников. Какие темы вам было бы интересно увидеть в следующем вебинаре? - Было бы интересно услышать о применении алгоритмов в финансовой сфере. |


Для дополнения файла README.md с инструкцией по запуску предсказаний, можно использовать следующий текст:

---

## Получение предсказаний

Для получения предсказаний с использованием обученной модели и сохранения их в файл `predictions.csv`, выполните следующую команду:

```bash
python3 predict.py --file_path="mounted_folder/data_for_predict.csv" --model_path="mounted_folder/model.pth"
```
### Входные данные для предсказания

Ваши данные для предсказания должны быть оформлены следующим образом (пример одной строки данных):

| object | text                                                  |
|--------|-------------------------------------------------------|
| 0      | Что вам больше всего понравилось в теме вебинара? - Вебинар был очень познавательным. Какие вопросы остались без ответа после вебинара? - У меня остались вопросы по применению алгоритмов в реальной жизни. Какой формат вебинара вам было бы интересно видеть? - Мне больше всего подходит формат с презентациями и демонстрациями кода. Есть ли у вас предложения по улучшению вебинара? - Я предлагаю добавить больше практических заданий для участников. Какие темы вам было бы интересно увидеть в следующем вебинаре? - Было бы интересно услышать о применении алгоритмов в финансовой сфере. |


### Параметры команды
- `--file_path` указывает путь к CSV файлу с данными, для которых необходимо получить предсказания.
- `--model_path` указывает путь к файлу с сохранённой моделью.

Убедитесь, что указанные пути к файлам корректны и доступны из вашей рабочей среды. В указанном примере предполагается, что данные и модель находятся в папке `mounted_folder`, которая должна быть доступна в момент выполнения скрипта.

### Вывод

После выполнения команды, скрипт сохранит предсказания в файл `predictions.csv` в текущем рабочем каталоге. Результат будет содержать колонки `is_relevant`, `object`, и `is_positive`, каждая из которых представляет предсказание соответствующей модели.

Пример файла `predictions.csv`

| is_relevant | object | is_positive |
|-------------|--------|-------------|
| 1           | 0      | 1           |
| 1           | 0      | 1           |
| 1           | 0      | 1           |
| 1           | 0      | 1           |
| 1           | 0      | 1           |


## Извлечение файлов предсказаний из Docker контейнера

Для копирования файла с предсказаниями из контейнера в текущую директорию на вашем компьютере используйте следующую команду:

```bash
docker cp <container_id>:/app/predictions.csv .
```