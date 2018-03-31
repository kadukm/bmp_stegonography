import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk
from modules import steg_functions as steg_functions
from modules.coding_options import CodingOptions
from modules.scales_bar import ScalesBar


class MyWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.max_size = 350, 350
        self.frame_to_encode = tk.Frame(self)
        self.frame_to_decode = tk.Frame(self)
        self.scales_bar_to_encode = ScalesBar(self.frame_to_encode)
        self.scales_bar_to_decode = ScalesBar(self.frame_to_decode)
        self.way_to_encodefile = tk.Label(self.frame_to_encode)
        self.way_to_sourcefile = tk.Label(self.frame_to_encode)
        self.way_to_decodefile = tk.Label(self.frame_to_decode)
        self.frame_with_images_to_encode = tk.Frame(self.frame_to_encode)
        self.frame_with_image_to_decode = tk.Frame(self.frame_to_decode)

        self.extra_init()

    def extra_init(self):
        btn_to_encode = tk.Button(self, text='Кодирование',
                                  command=self._to_frame_to_encode)
        btn_to_encode.grid(row=0, column=0)

        btn_to_decode = tk.Button(self, text='Декодирование',
                                  command=self._to_frame_to_decode)
        btn_to_decode.grid(row=0, column=1)

        self._init_frame_to_encode()
        self._init_frame_to_decode()

        self.frame_to_encode.grid(row=1, column=0, columnspan=2)

    def _init_frame_to_encode(self):
        label_to_encodefile = tk.Label(self.frame_to_encode,
                                       text='Выберите файл для шифрования',
                                       font='Arial 11')
        label_to_encodefile.grid(row=0, column=0)
        btn_to_encodefile = tk.Button(self.frame_to_encode, text='Выбрать',
                                      command=self._open_to_encodefile)
        btn_to_encodefile.grid(row=0, column=1)
        self.way_to_encodefile.config(width=60, height=1)
        self.way_to_encodefile.grid(row=0, column=2)

        label_to_sourcefile = tk.Label(self.frame_to_encode,
                                       text='Выберите картинку-переносчика',
                                       font='Arial 11')
        label_to_sourcefile.grid(row=1, column=0)
        btn_to_sourcefile = tk.Button(self.frame_to_encode, text='Выбрать',
                                      command=self._open_to_sourcefile)
        btn_to_sourcefile.grid(row=1, column=1)
        self.way_to_sourcefile.config(width=60, height=1)
        self.way_to_sourcefile.grid(row=1, column=2)

        self.scales_bar_to_encode.grid(row=2, column=0, columnspan=3)

        btn_to_encodedfile = tk.Button(self.frame_to_encode,
                                       text='Зашифровать файл как...',
                                       command=self._save_to_encodedfile)
        btn_to_encodedfile.grid(row=3, column=0, columnspan=3)
        self.frame_with_images_to_encode.grid(row=4, column=0,
                                              columnspan=3, sticky='W')

    def _save_to_encodedfile(self):
        try:
            if self.way_to_encodefile['text'] == '':
                raise FileNotFoundError('Файл для шифрования не выбран')
            if self.way_to_sourcefile['text'] == '':
                raise FileNotFoundError('Картинка-переносчик не выбрана')
            options = CodingOptions(
                *self.scales_bar_to_encode.get_coding_options)
            with asksaveasfile(filetypes=(("BMP file", "*.bmp"),),
                               defaultextension='.bmp') as file_to_encoding:
                if file_to_encoding is None:
                    return
                if len(self.frame_with_images_to_encode.winfo_children()) > 1:
                    self.frame_with_images_to_encode.winfo_children()[1].destroy()
                data_to_encode = \
                    steg_functions.get_data_to_encode_from_file(
                        self.way_to_encodefile['text'])
                steg_functions.encode(data_to_encode,
                                      self.way_to_sourcefile['text'],
                                      options, file_to_encoding.name)
                encoded_image = Image.open(file_to_encoding.name)
                encoded_image.thumbnail(self.max_size, Image.ANTIALIAS)
                encoded_image2tk = ImageTk.PhotoImage(encoded_image)
                label_with_image = tk.Label(self.frame_with_images_to_encode,
                                            image=encoded_image2tk, width=350)
                label_with_image.image = encoded_image2tk
                label_with_image.pack(side='right')
                messagebox.showinfo('Success',
                                    ('Информация успешно зашифрована в ' +
                                     file_to_encoding.name.split('/')[-1]))
        except (ValueError, FileNotFoundError) as e:
            messagebox.showerror('Error', str(e))
        except AttributeError:
            pass
        except Exception as e:
            messagebox.showerror('Error', 'Unexpected error: ' + str(e))

    def _open_to_encodefile(self):
        try:
            with askopenfile() as opened_file_to_encode:
                if opened_file_to_encode is None:
                    return
                self.way_to_encodefile['text'] = opened_file_to_encode.name
        except AttributeError:
            pass

    def _open_to_sourcefile(self):
        try:
            with askopenfile() as opened_sourcefile:
                if opened_sourcefile is None:
                    return
                self.way_to_sourcefile['text'] = opened_sourcefile.name

                for child in self.frame_with_images_to_encode.winfo_children():
                    child.destroy()
                source_image = Image.open(opened_sourcefile.name)
                source_image.thumbnail(self.max_size, Image.ANTIALIAS)
                source_image2tk = ImageTk.PhotoImage(source_image)
                label_with_image = tk.Label(self.frame_with_images_to_encode,
                                            image=source_image2tk, width=350)
                label_with_image.image = source_image2tk
                label_with_image.pack(side='left')
        except AttributeError:
            pass

    def _init_frame_to_decode(self):
        label_to_decodefile = tk.Label(self.frame_to_decode,
                                       text='Выберите файл для декодирования',
                                       font='Arial 11')
        label_to_decodefile.grid(row=0, column=0)
        btn_to_decodefile = tk.Button(self.frame_to_decode, text='Выбрать',
                                      command=self._open_to_decodefile)
        btn_to_decodefile.grid(row=0, column=1)
        self.way_to_decodefile.config(width=60, height=1)
        self.way_to_decodefile.grid(row=0, column=2)

        self.scales_bar_to_decode.grid(row=1, column=0, columnspan=3)

        btn_to_decodedfile = tk.Button(self.frame_to_decode,
                                       text='Декодировать файл как...',
                                       command=self._save_to_decodedfile)
        btn_to_decodedfile.grid(row=2, column=0, columnspan=3)
        self.frame_with_image_to_decode.grid(row=3, column=0,
                                             columnspan=3, sticky='W')

    def _save_to_decodedfile(self):
        try:
            if self.way_to_decodefile['text'] == '':
                raise FileNotFoundError('Файл для декодирования не выбран')
            options = CodingOptions(
                *self.scales_bar_to_decode.get_coding_options)
            with asksaveasfile() as file_to_decoding:
                if file_to_decoding is None:
                    return
                decoded_data_with_polynomial = \
                    steg_functions.get_decoded_data_with_polynomial(
                        self.way_to_decodefile['text'], options)
                crc_is_right, decoded_data = \
                    steg_functions.get_and_check_decoded_data(
                        decoded_data_with_polynomial)
                if not crc_is_right:
                    user_wants_to_continue = \
                        messagebox.askokcancel(
                            'Warning', 'При передаче данные повредились.'
                                       'Продолжить, несмотря на это?')
                    if not user_wants_to_continue:
                        raise ValueError('Данные повреждены')
                steg_functions.decode(decoded_data, file_to_decoding.name)
                messagebox.showinfo('Success',
                                    ('Информация успешно декодирована в ' +
                                     file_to_decoding.name.split('/')[-1]))
        except (ValueError, FileNotFoundError) as e:
            messagebox.showerror('Error', str(e))
        except AttributeError:
            pass
        except Exception as e:
            messagebox.showerror('Error', 'Unexpected error: ' + str(e))

    def _open_to_decodefile(self):
        try:
            with askopenfile() as opened_file_to_decode:
                if opened_file_to_decode is None:
                    return
                self.way_to_decodefile['text'] = opened_file_to_decode.name

                for child in self.frame_with_image_to_decode.winfo_children():
                    child.destroy()
                max_width = 700
                encoded_image = Image.open(opened_file_to_decode.name)
                encoded_image.thumbnail((max_width, self.max_size[1]),
                                        Image.ANTIALIAS)
                encoded_image2tk = ImageTk.PhotoImage(encoded_image)
                label_with_image = tk.Label(self.frame_with_image_to_decode,
                                            image=encoded_image2tk, width=700)
                label_with_image.image = encoded_image2tk
                label_with_image.pack()
        except AttributeError:
            pass

    def _to_frame_to_encode(self):
        self.frame_to_decode.grid_forget()
        self.frame_to_encode.grid(row=1, column=0, columnspan=2)

    def _to_frame_to_decode(self):
        self.frame_to_encode.grid_forget()
        self.frame_to_decode.grid(row=1, column=0, columnspan=2)


def run():
    root = MyWindow(className='Steganography')
    root.mainloop()
