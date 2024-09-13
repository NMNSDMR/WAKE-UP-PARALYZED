import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from scipy.signal import butter, lfilter

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

DISPLAY_DURATION = 10
DISPLAY_POINTS = DISPLAY_DURATION * RATE // CHUNK

B, A = butter(1, 0.1, btype='low')

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

is_paused = False

audio_data = np.zeros(DISPLAY_POINTS * CHUNK, dtype=np.int16)

high_freq_times = []

def filter_signal(signal):
    return lfilter(B, A, signal)

def update_plot(frame):
    global audio_data
    if not is_paused:
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        filtered_data = filter_signal(data)
        audio_data = np.roll(audio_data, -CHUNK)
        audio_data[-CHUNK:] = filtered_data

        x = np.arange(len(audio_data))
        ax_main.set_xlim(0, DISPLAY_POINTS * CHUNK)
        line_main.set_data(x, audio_data)
        
        rms = np.sqrt(np.mean(np.square(data)))
        decibels = 20 * np.log10(rms + 1e-6)
        decibel_label.config(text=f"Decibels: {decibels:.2f} dB")

    return line_main,

def update_freq_plot(frame):
    global high_freq_times
    if not is_paused:
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        filtered_data = filter_signal(data)
        window = np.hamming(len(filtered_data))
        data_windowed = filtered_data * window
        
        fft_data = np.fft.fft(data_windowed)
        fft_freq = np.fft.fftfreq(len(fft_data), 1 / RATE)
        fft_magnitude = np.abs(fft_data)
        
        positive_freqs = fft_freq[:len(fft_freq) // 2]
        positive_magnitude = fft_magnitude[:len(fft_magnitude) // 2]
        
        ax_freq.clear()
        ax_freq.plot(positive_freqs, positive_magnitude, color='white')
        ax_freq.set_xlim(0, RATE // 2)
        ax_freq.set_ylim(0, np.max(positive_magnitude))
        ax_freq.set_facecolor('black')
        ax_freq.get_xaxis().set_visible(False)
        ax_freq.get_yaxis().set_visible(False)

        peak_freq_index = np.argmax(positive_magnitude)
        peak_freq = positive_freqs[peak_freq_index]
        freq_label.config(text=f"Frequency: {peak_freq:.2f} Hz")

        if peak_freq > 400:
            current_time = datetime.now().strftime("%H:%M")
            if not high_freq_times or high_freq_times[-1] != current_time:
                high_freq_times.append(current_time)
                high_freq_times_text.set("High Frequency Times:\n" + "\n".join(high_freq_times))

    return line_freq,

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.config(text="\u25B6")
    else:
        pause_button.config(text="\u23F8")

root = tk.Tk()
root.title("Audio Recorder")
root.configure(bg='black')

window_width = 1200
window_height = 800
frame_width = int(window_width * 0.75)
frame_height = int(window_height * 0.75)

freq_window_width = 250
freq_window_height = 200

frame_border = tk.Frame(root, bg='white', bd=2)
frame_border.place(x=20, y=20, width=frame_width, height=frame_height)

freq_frame = tk.Frame(root, bg='white', bd=2)
freq_frame.place(x=window_width - freq_window_width - 20, y=20, width=freq_window_width, height=freq_window_height)

fig_main, ax_main = plt.subplots(facecolor='black')
line_main, = ax_main.plot([], [], lw=1.5, color='white')

ax_main.set_ylim(-2**15, 2**15 - 1)
ax_main.set_xlim(0, DISPLAY_POINTS * CHUNK)
ax_main.set_facecolor('black')
ax_main.get_xaxis().set_visible(False)
ax_main.get_yaxis().set_visible(False)

canvas_main = FigureCanvasTkAgg(fig_main, master=frame_border)
canvas_widget_main = canvas_main.get_tk_widget()
canvas_widget_main.pack(fill=tk.BOTH, expand=True)

fig_freq, ax_freq = plt.subplots(facecolor='black')
line_freq, = ax_freq.plot([], [], lw=1.5, color='white')

ax_freq.set_xlim(0, RATE // 2)
ax_freq.set_ylim(0, 1)
ax_freq.set_facecolor('black')
ax_freq.get_xaxis().set_visible(False)
ax_freq.get_yaxis().set_visible(False)

canvas_freq = FigureCanvasTkAgg(fig_freq, master=freq_frame)
canvas_widget_freq = canvas_freq.get_tk_widget()
canvas_widget_freq.pack(fill=tk.BOTH, expand=True)

pause_button = tk.Button(root, text="\u23F8", command=toggle_pause, font=("Arial", 20), bg="gray", fg="white", bd=0)
pause_button.place(x=20, y=window_height - 80, width=40, height=40)

decibel_label = tk.Label(root, text="Decibels: 0.00 dB", font=("Arial", 12), bg='black', fg='white')
decibel_label.place(x=20, y=frame_height + 40, width=frame_width, height=30)

freq_label = tk.Label(root, text="Frequency: 0.00 Hz", font=("Arial", 12), bg='black', fg='white')
freq_label.place(x=window_width - freq_window_width - 20, y=freq_window_height + 40, width=freq_window_width, height=30)

high_freq_times_text = tk.StringVar()
high_freq_times_text.set("High Frequency Times:\n")
high_freq_time_label = tk.Label(root, textvariable=high_freq_times_text, font=("Arial", 12), bg='black', fg='red', anchor='w', justify='left')
high_freq_time_label.place(x=window_width - freq_window_width - 20, y=freq_window_height + 70, width=freq_window_width, height=frame_height - freq_window_height - 90)

ani_main = FuncAnimation(fig_main, update_plot, interval=50, cache_frame_data=False)
ani_freq = FuncAnimation(fig_freq, update_freq_plot, interval=50, cache_frame_data=False)

root.geometry(f'{window_width}x{window_height}')
root.mainloop()

stream.stop_stream()
stream.close()
p.terminate()
