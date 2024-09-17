import pyaudio #для аудио ну блять запись микрофона кароч
import numpy as np # матешная залупа типа преобразовываем наши аудиоданные в масивы кароч)
import matplotlib.pyplot as plt # для графиков матплотлиб бля кто название придумал фызващлфывз
from matplotlib.animation import FuncAnimation
import tkinter as tk #чтобы окно приложение нашего открылось йоу
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime # эт чисто что бы определять когда по времени было замечено выше дохуя герц
from scipy.signal import butter, lfilter # дает функции для обработки сигналов но тут она нужна для фильтра баттерхуя который я спиздил

# Настройки аудио
CHUNK = 1024  # <- Количество оцифрованых звуковых блять фрагментов фыщвзащзфывхафыхвах сука я ток что на википедии узнал че это, которые мы будем считывать за один раз (чем больше, тем дольше)
FORMAT = pyaudio.paInt16  # <- Формат аудио данных (16 бит)
CHANNELS = 1  # <- Используем моно звук (один канал)
RATE = 44100  # <- Частота дискретизации, то есть сколько сэмплов(смешное слово) в секунду считывается

# Настройки отображения
DISPLAY_DURATION = 10  # <- Сколько секунд звука мы хотим отображать на графике(ну типа скок секунд звука будет на этой дорожке обосанной)
DISPLAY_POINTS = DISPLAY_DURATION * RATE // CHUNK  # <- Количество точек, которое нужно для отображения графика

# Настройки фильтра Баттерворта для аудио сигнала(СПИЗДИЛ С ИНЕТА НЕ ЕБУ КАК РАБОТАЕТ НО ВРОДЕ НОРМ ФВЫЗХЪАФЗЫХВАХХА)
B, A = butter(1, 0.5 / (RATE / 2), btype='low')  # <- Фильтр низких частот, пропускает только медленные изменения

# Инициализация PyAudio
p = pyaudio.PyAudio()  # <- Запускаем хуету эту
stream = p.open(format=FORMAT,  # <- Открываем аудиопоток
                channels=CHANNELS,
                rate=RATE,
                input=True,  # <- Мы будем записывать звук с микрофона
                frames_per_buffer=CHUNK)  # <- Читаем кусками по 1024 сэмпла(я умру щас нахуй это смешное слово)

is_paused = False  # <- Флаг, который определяет, находится ли приложение на паузе ( ну поднимается = пауща всего а если нет то ебошит )
audio_data = np.zeros(DISPLAY_POINTS * CHUNK, dtype=np.int16)  # <- Массив, куда мы будем складывать аудиоданные
high_freq_times = []  # <- Список, в котором мы будем хранить моменты, когда частота была выше 2000 Гц(2000 условное потом решим как оно епта ебошит)

# Фильтрация сигнала через фильтр Баттерворта(все еще не ебу че это)
def filter_signal(signal):
    return lfilter(B, A, signal)  # <- Пропускаем сигнал через фильтр, чтобы убрать высокие частоты

# Обновление графика сигнала
def update_plot(frame):
    global audio_data
    if not is_paused:
        # Читаем очередную порцию аудиоданных
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)  # <- Читаем 1024 сэмпла
        filtered_data = filter_signal(data)  # <- Фильтруем аудиоданные, чтобы убрать шумы

        # Сдвигаем старые данные и добавляем новые
        audio_data = np.roll(audio_data, -CHUNK)  # <- Сдвигаем старые данные влево на 1024 точки
        audio_data[-CHUNK:] = filtered_data  # <- В конец добавляем новые отфильтрованные данные ну тут вроде понятно всё

        # Готовим данные для графика
        x = np.arange(len(audio_data))  # <- Создаем массив индексов для оси X (ну типа [0, 1, 2,...])
        ax_main.set_xlim(0, DISPLAY_POINTS * CHUNK)  # <- Устанавливаем границы графика по оси X
        line_main.set_data(x, audio_data)  # <- Обновляем линию на графике новыми данными

        # Рассчитываем уровень громкости (RMS)
        rms = np.sqrt(np.mean(np.square(data)))  # <- RMS = квадратный корень из среднего квадрата значений
        decibels = 20 * np.log10(rms + 1e-6)  # <- Преобразуем громкость в децибелы (логарифмируем) тож спиздил с инета формулу вызхахфыв вроде похоже на правду
        decibel_label.config(text=f"Decibels: {decibels:.2f} dB")  # <- Обновляем текстовое поле с уровнем децибел

    return line_main,  # <- Возвращаем обновленную линию графика

# Обновление графика частоты ВСЕ ЧТО НАПИСАНО ТАМ ПРО ЧАСТОТУ Я БЛЯТЬ НАПИСАЛ ТАК КАК НАПИСАНО НА ВИКИПЕДИИ\ФОРУМАХ ДЛЯ БОТАНИКОВ
def update_freq_plot(frame):
    global high_freq_times
    if not is_paused:
        # Читаем новые аудиоданные
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)  # <- Читаем 1024 сэмпла
        filtered_data = filter_signal(data)  # <- Фильтруем их через фильтр

        # Применяем окно Хэмминга для сглаживания FFT
        window = np.hamming(len(filtered_data))  # <- Окно Хэмминга (для уменьшения утечек при FFT)
        data_windowed = filtered_data * window  # <- Применяем окно к данным

        # Выполняем преобразование Фурье (FFT)
        fft_data = np.fft.fft(data_windowed)  # <- Получаем спектр частот с помощью FFT
        fft_freq = np.fft.fftfreq(len(fft_data), 1 / RATE)  # <- Массив частот, соответствующих каждому элементу FFT
        fft_magnitude = np.abs(fft_data)  # <- Модуль комплексных чисел FFT, это амплитуды

        # Оставляем только положительные частоты
        positive_freqs = fft_freq[:len(fft_freq) // 2]  # <- Берем только положительные частоты
        positive_magnitude = fft_magnitude[:len(fft_magnitude) // 2]  # <- И их амплитуды

        # Рисуем новый спектр
        ax_freq.clear()  # <- Очищаем предыдущий график
        ax_freq.plot(positive_freqs, positive_magnitude, color='cyan', lw=2, alpha=0.75)  # <- Рисуем линию
        ax_freq.set_xlim(0, RATE // 2)  # <- Границы по X от 0 до половины частоты дискретизации
        ax_freq.set_ylim(0, np.max(positive_magnitude))  # <- Границы по Y - максимальная амплитуда
        ax_freq.set_facecolor('#121212')  # <- Устанавливаем темный фон графика

        # Находим пиковую частоту
        peak_freq_index = np.argmax(positive_magnitude)  # <- Индекс частоты с максимальной амплитудой
        peak_freq = positive_freqs[peak_freq_index]  # <- Соответствующая частота
        freq_label.config(text=f"Frequency: {peak_freq:.2f} Hz")  # <- Обновляем текстовое поле с частотой

        # Если частота выше 2000 Гц, запоминаем время
        if peak_freq > 2000:
            current_time = datetime.now().strftime("%H:%M")  # <- Получаем текущее время (часы:минуты)
            if not high_freq_times or high_freq_times[-1] != current_time:  # <- Проверяем, чтобы не было дубликатов
                high_freq_times.append(current_time)  # <- Добавляем новое время в список
                high_freq_times_text.set("High Frequency Times:\n" + "\n".join(high_freq_times))  # <- Обновляем текст

    return line_freq,  # <- Возвращаем обновленную линию частотного графика

# Переключение паузы
def toggle_pause():
    global is_paused
    is_paused = not is_paused  # <- Переключаем состояние паузы
    if is_paused:
        pause_button.config(text="\u25B6")  # <- Если пауза включена, меняем текст кнопки на плей
    else:
        pause_button.config(text="\u23F8")  # <- Если пауза выключена, меняем текст кнопки на пауз

# Интерфейс с Tkinter
root = tk.Tk()  # <- Создаем главное окно приложения
root.title("КТО ПРОЧИТАЛ ТОТ ЛОХ")  # <- Устанавливаем заголовок окна
root.configure(bg='#181818')  # <- Устанавливаем темную тему(черный = круто если не учитывать чернокожих) для фона окна

# Размеры окна
window_width = 1200  # <- Ширина окна
window_height = 800  # <- Высота окна
frame_width = int(window_width * 0.75)  # <- Ширина основной области с графиками
frame_height = int(window_height * 0.75)  # <- Высота основной области с графиками

# Дополнительные стили
frame_border = tk.Frame(root, bg='#303030', bd=2, relief=tk.RAISED)  # <- Создаем рамку для графиков
frame_border.place(x=20, y=20, width=frame_width, height=frame_height)  # <- Размещаем рамку на экране

freq_frame = tk.Frame(root, bg='#303030', bd=2, relief=tk.RAISED)  # <- Рамка для графика частот
freq_frame.place(x=frame_width + 40, y=20, width=window_width - frame_width - 60, height=200)  # <- Размещаем ее

# Основной график
fig_main, ax_main = plt.subplots(facecolor='#181818')  # <- Создаем объект для основного графика
line_main, = ax_main.plot([], [], lw=2.5, color='#00ff99')  # <- Создаем пустую линию для данных сигнала

# Настраиваем внешний вид графика
ax_main.set_ylim(-2**15, 2**15 - 1)  # <- Диапазон значений оси Y (макс/мин для 16-битного звука)
ax_main.set_xlim(0, DISPLAY_POINTS * CHUNK)  # <- Диапазон значений по оси X (количество точек)
ax_main.set_facecolor('#181818')  # <- Темный фон для графика
ax_main.get_xaxis().set_visible(False)  # <- Прячем ось X
ax_main.get_yaxis().set_visible(False)  # <- Прячем ось Y

canvas_main = FigureCanvasTkAgg(fig_main, master=frame_border)  # <- Привязываем график к интерфейсу Tkinter
canvas_widget_main = canvas_main.get_tk_widget()  # <- Получаем виджет графика
canvas_widget_main.pack(fill=tk.BOTH, expand=True)  # <- Размещаем виджет

# График частот
fig_freq, ax_freq = plt.subplots(facecolor='#121212')  # <- Создаем объект для частотного графика
line_freq, = ax_freq.plot([], [], lw=2.5, color='cyan')  # <- Создаем пустую линию для частотного спектра

# Настраиваем внешний вид частотного графика
ax_freq.set_xlim(0, RATE // 2)  # <- Ограничиваем по оси X до половины частоты дискретизации (Nyquist)
ax_freq.set_ylim(0, 1)  # <- Ограничиваем ось Y по умолчанию
ax_freq.set_facecolor('#121212')  # <- Темный фон
ax_freq.get_xaxis().set_visible(False)  # <- Прячем ось X
ax_freq.get_yaxis().set_visible(False)  # <- Прячем ось Y

canvas_freq = FigureCanvasTkAgg(fig_freq, master=freq_frame)  # <- Привязываем график частот к интерфейсу Tkinter
canvas_widget_freq = canvas_freq.get_tk_widget()  # <- Получаем виджет графика
canvas_widget_freq.pack(fill=tk.BOTH, expand=True)  # <- Размещаем виджет

# Кнопка паузы/продолжения
pause_button = tk.Button(root, text="\u23F8", command=toggle_pause, font=("Arial", 20),  # <- Кнопка паузы
                         bg="#404040", fg="white", bd=0, activebackground="#505050",
                         activeforeground="white", relief=tk.FLAT)
pause_button.place(x=20, y=window_height - 80, width=60, height=60)  # <- Размещение кнопки

# Метки для отображения
decibel_label = tk.Label(root, text="Decibels: 0.00 dB", font=("Arial", 14),  # <- Метка для децибел
                         bg='#181818', fg='white')
decibel_label.place(x=20, y=frame_height + 40, width=frame_width, height=30)  # <- Размещение метки

freq_label = tk.Label(root, text="Frequency: 0.00 Hz", font=("Arial", 14),  # <- Метка для частоты
                      bg='#181818', fg='white')
freq_label.place(x=window_width - 300, y=250, width=250, height=30)  # <- Размещение метки

high_freq_times_text = tk.StringVar()  # <- Переменная для хранения текстовых данных о времени высокой частоты
high_freq_times_text.set("High Frequency Times:\n")  # <- Устанавливаем начальное значение
high_freq_time_label = tk.Label(root, textvariable=high_freq_times_text, font=("Arial", 12),  # <- Метка для времени частот
                                bg='#181818', fg='#FF4D4D', anchor='w', justify='left')
high_freq_time_label.place(x=window_width - 300, y=290, width=250, height=500)  # <- Размещение метки

# Анимация графиков
ani_main = FuncAnimation(fig_main, update_plot, interval=100, cache_frame_data=False)  # <- Анимация для основного графика
ani_freq = FuncAnimation(fig_freq, update_freq_plot, interval=100, cache_frame_data=False)  # <- Анимация для частотного графика

# Параметры окна
root.geometry(f'{window_width}x{window_height}')  # <- Устанавливаем размеры окна
root.mainloop()  # <- Запуск главного цикла программы

# Остановка аудиострима
stream.stop_stream()  # <- Останавливаем поток аудио
stream.close()  # <- Закрываем поток
p.terminate()  # <- Завершаем работу с PyAudio
#ну вроде все нихуя лишнего бля озфываофцывошах помогите