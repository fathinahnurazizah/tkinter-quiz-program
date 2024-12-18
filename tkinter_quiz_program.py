'''
Made by :
1. Daffa Hadyan Navista
2. Donna Maya Puspita
3. Fathinah Nur Azizah
4. M. Naufal Ramadhan

'''
import tkinter as tk
from tkinter import messagebox, Toplevel
import json


# Fungsi untuk Login
def login(username_entry, password_entry, root):
    username = username_entry.get()
    password = password_entry.get()

    if username == '' or password == '':
        messagebox.showerror('Login', 'Please enter your username and password!')
    elif username == 'Mahasiswa Sains Data' and password == 'SD23':
        messagebox.showinfo('Login', 'Login success!')
        root.destroy()  # Tutup window login
        menu_utama()    # Panggil menu utama
    else:
        messagebox.showerror('Login', 'Incorrect username or password!')


# Fungsi Menu Utama
def menu_utama():
    menu_window = tk.Tk()
    menu_window.title("Menu Soal")
    menu_window.geometry("600x400")

    tk.Label(menu_window, text="Menu Utama", font=("Arial", 20), bg="#fcba03", fg="#000000").pack(pady=20)
    tk.Button(menu_window, text="Tambah Soal", command=form_tambah_soal, width=20, bg="#000000", fg="#ffffff").pack(pady=5)
    tk.Button(menu_window, text="Edit Soal", command=form_edit_soal, width=20, bg="#000000", fg="#ffffff").pack(pady=5)
    tk.Button(menu_window, text="Hapus Soal", command=form_hapus_soal, width=20, bg="#000000", fg="#ffffff").pack(pady=5)
    tk.Button(menu_window, text="Lihat Daftar Soal", command=lambda: tampilkan_daftar_soal(menu_window), width=20, bg="#000000", fg="#ffffff").pack(pady=5)
    tk.Button(menu_window, text="Mulai Kuis", command=mulai_kuis, width=20, bg="#000000", fg="#ffffff").pack(pady=5)
    tk.Button(menu_window, text="Keluar", command=menu_window.destroy, width=20, bg="#fcba03", fg="#ffffff").pack(pady=5)

    menu_window.mainloop()


# Fungsi Tambah, Edit, dan Hapus Soal
filename = "soal.json"
skor_filename = "skor.json"


def load_soal():
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat memuat data: {str(e)}")
        return []


def save_soal(soal_list):
    try:
        with open(filename, "w") as file:
            json.dump(soal_list, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan data: {str(e)}")


def tambah_soal(soal, jawaban):
    soal_list = load_soal()
    soal_list.append({"soal": soal, "jawaban": jawaban})
    save_soal(soal_list)
    return "Soal berhasil ditambahkan!"


def edit_soal(index, soal_baru, jawaban_baru):
    soal_list = load_soal()
    if 0 <= index < len(soal_list):
        soal_list[index] = {"soal": soal_baru, "jawaban": jawaban_baru}
        save_soal(soal_list)
        return "Soal berhasil diubah!"
    else:
        return "Indeks soal tidak valid."


def hapus_soal(index):
    soal_list = load_soal()
    if 0 <= index < len(soal_list):
        soal_list.pop(index)
        save_soal(soal_list)
        return "Soal berhasil dihapus!"
    else:
        return "Indeks soal tidak valid."

#Fungsi untuk menampilkan skor akhir
def load_skor():
    try:
        with open(skor_filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"skor": 0}

def simpan_skor(skor):
    try:
        with open(skor_filename, "w") as file:
            json.dump({"skor": skor}, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan skor: {str(e)}")


def tampilkan_skor_akhir():
    skor_data = load_skor()
    messagebox.showinfo("Skor Akhir", f"Skor Akhir Anda: {skor_data.get('skor', 0)}")


# Fungsi Rekursif untuk mencari soal berdasarkan kata kunci
def cari_soal_recursive(soal_list, keyword, index=0):
    if index >= len(soal_list):
        return None  # Jika tidak ditemukan
    if keyword in soal_list[index]['soal']:
        return soal_list[index]  # Ditemukan
    return cari_soal_recursive(soal_list, keyword, index + 1)


# Fungsi untuk Membuat Form
def buat_form(title, labels, button_text, submit_command):
    window = Toplevel()
    window.title(title)
    window.geometry("400x300")

    entries = []
    for label_text in labels:
        tk.Label(window, text=label_text, bg="#fcba03", fg="#000000").pack()
        entry = tk.Entry(window, width=40)
        entry.pack()
        entries.append(entry)

    tk.Button(window, text=button_text, command=submit_command, bg="#000000", fg="#ffffff").pack(pady=10)
    return window, entries


# Form Tambah, Edit, dan Hapus Soal
def tampilkan_daftar_soal(window):
    soal_list = load_soal()
    if not soal_list:
        messagebox.showinfo("Daftar Soal", "Belum ada soal yang tersedia.")
        return

    # Buat window baru untuk daftar soal
    daftar_window = Toplevel(window)
    daftar_window.title("Daftar Soal")
    daftar_window.geometry("500x400")

    # Tampilkan daftar soal
    tk.Label(daftar_window, text="Daftar Soal", font=("Arial", 16), bg="#fcba03", fg="#000000").pack(pady=10)
    for i, soal in enumerate(soal_list, start=1):
        tk.Label(daftar_window, text=f"{i}. {soal['soal']} (Jawaban: {soal['jawaban']})", wraplength=450, anchor="w", justify="left",
                 bg="#fcba03", fg="#000000").pack(anchor="w", padx=10, pady=5)

def form_tambah_soal():
    def submit_soal():
        soal = entry_soal.get()
        jawaban = entry_jawaban.get()
        messagebox.showinfo("Tambah Soal", tambah_soal(soal, jawaban))
        tambah_window.destroy()
        tampilkan_daftar_soal(menu_window)  # Menampilkan daftar soal setelah menambah

    tambah_window, entries = buat_form("Tambah Soal", ["Soal:", "Jawaban:"], "Tambah", submit_soal)
    entry_soal, entry_jawaban = entries

def form_edit_soal():
    def submit_edit():
        try:
            index = int(entry_index.get())
            soal_baru = entry_soal.get()
            jawaban_baru = entry_jawaban.get()
            messagebox.showinfo("Edit Soal", edit_soal(index, soal_baru, jawaban_baru))
            edit_window.destroy()
        except ValueError:
            messagebox.showerror("Edit Soal", "Indeks harus berupa angka!")

    edit_window, entries = buat_form("Edit Soal", ["Indeks Soal:", "Soal Baru:", "Jawaban Baru:"], "Simpan Perubahan", submit_edit)
    entry_index, entry_soal, entry_jawaban = entries


def form_hapus_soal():
    def submit_hapus():
        try:
            index = int(entry_index.get())
            messagebox.showinfo("Hapus Soal", hapus_soal(index))
            hapus_window.destroy()
        except ValueError:
            messagebox.showerror("Hapus Soal", "Indeks harus berupa angka!")

    hapus_window, entries = buat_form("Hapus Soal", ["Indeks Soal:"], "Hapus", submit_hapus)
    entry_index, = entries

def mulai_kuis():
    soal_list = load_soal()

    if not soal_list:
        messagebox.showinfo("Kuis", "Belum ada soal yang tersedia.")
        return

    # Inisialisasi skor
    skor = 0
    total_soal = len(soal_list)

    def tampilkan_soal(index):
        if index >= total_soal:
            # Jika soal habis, tampilkan skor akhir
            simpan_skor(skor)
            messagebox.showinfo("Kuis Selesai", f"Kuis selesai! Skor Anda: {skor}/{total_soal}")
            kuis_window.destroy()
            return

        # Tampilkan soal
        soal = soal_list[index]['soal']
        jawaban_benar = soal_list[index]['jawaban']
        soal_label.config(text=f"Soal {index + 1}: {soal}")
        jawaban_entry.delete(0, tk.END)

        def cek_jawaban():
            nonlocal skor
            jawaban_user = jawaban_entry.get()
            if jawaban_user.lower().strip() == jawaban_benar.lower().strip():
                skor += 1
                messagebox.showinfo("Kuis", "Jawaban benar!")
            else:
                messagebox.showinfo("Kuis", f"Jawaban salah! Jawaban yang benar adalah: {jawaban_benar}")
            tampilkan_soal(index + 1)

        submit_button.config(command=cek_jawaban)

    # Membuat jendela kuis
    kuis_window = Toplevel()
    kuis_window.title("Kuis")
    kuis_window.geometry("500x300")

    soal_label = tk.Label(kuis_window, text="", font=("Arial", 14),bg="#fcba03", fg="#000000",  wraplength=450)
    soal_label.pack(pady=20)

    jawaban_entry = tk.Entry(kuis_window, font=("Arial", 14))
    jawaban_entry.pack(pady=10)

    submit_button = tk.Button(kuis_window, text="Submit", font=("Arial", 12), bg="#000000", fg="#ffffff")
    submit_button.pack(pady=10)

    # Mulai dengan soal pertama
    tampilkan_soal(0)


# GUI Utama (Login)
def main():
    root = tk.Tk()
    root.title("Login Page")
    root.geometry("800x600")
    root.config(bg="#fcba03")

    # Menambahkan label utama di tengah
    tk.Label(root, text="Login Page", bg="#fcba03", font=("Arial", 30)).grid(row=0, column=0, columnspan=2, pady=50)

    # Label dan entry untuk username
    tk.Label(root, text="Username", bg="#ffffff", font=("Arial", 20)).grid(row=1, column=0, padx=20, pady=10, sticky='e')
    username_entry = tk.Entry(root, font=("Arial", 20))
    username_entry.grid(row=1, column=1, padx=20, pady=10)

    # Label dan entry untuk password
    tk.Label(root, text="Password", bg="#ffffff", font=("Arial", 20)).grid(row=2, column=0, padx=20, pady=10, sticky='e')
    password_entry = tk.Entry(root, font=("Arial", 20), show="*")
    password_entry.grid(row=2, column=1, padx=20, pady=10)

    # Tombol login di tengah
    tk.Button(root, text="Login", bg="#000000", fg="#ffffff", font=("Arial", 15),
              command=lambda: login(username_entry, password_entry, root)).grid(row=3, column=0, columnspan=2, pady=20)

    # Menentukan lebar kolom agar elemen lebih besar dan lebih terpusat
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)

    root.mainloop()

if __name__ == "__main__":
    main()