import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk

def koneksi():
    con = sqlite3.connect("nilai_siswa.db")
    return con

# Membuat tabel jika belum ada
def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    con.commit()
    con.close()

def insertNilaiSiswa(nama_Siswa: str, biologi: int, fisika: int, inggris: int, prediksi_fakultas : str):
    con = koneksi()
    cur = con.cursor()
    cur.execute("INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) VALUES (?, ?, ?, ?, ?)", (nama_Siswa, biologi, fisika, inggris, prediksi_fakultas))
    con.commit()
    rowid = cur.lastrowid
    con.close()
    return rowid

def readNilaiSiswa():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows
create_table()

class nilai_siswa(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input dan Prediksi Fakultas")
        self.geometry("700x500")
        self.configure(bg="#f0f2f5")

        frm = tk.Frame(self, bg="#ffffff", padx=12, pady=12)
        frm.pack(padx=16, pady=12, fill="x")

        # Input fields
        tk.Label(frm, text="Nama Siswa:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.ent_nama = tk.Entry(frm, width=30)
        self.ent_nama.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Nilai Biologi:", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.ent_biologi = tk.Entry(frm, width=30)
        self.ent_biologi.grid(row=1, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Nilai Fisika:", bg="#ffffff").grid(row=2, column=0, sticky="w")
        self.ent_fisika = tk.Entry(frm, width=30)
        self.ent_fisika.grid(row=2, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Nilai Inggris:", bg="#ffffff").grid(row=3, column=0, sticky="w")
        self.ent_inggris = tk.Entry(frm, width=30)
        self.ent_inggris.grid(row=3, column=1, sticky="w", padx=6, pady=6)

        # Buttons frame
        btn_frame = tk.Frame(frm, bg="#ffffff")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(6, 0))

        self.btn_submit = tk.Button(btn_frame, text="Submit Nilai", width=15, command=self.insert_data)
        self.btn_submit.pack(side="left", padx=6)

        self.btn_refresh = tk.Button(btn_frame, text="Refresh Data", width=15, command=self.read_data)
        self.btn_refresh.pack(side="left", padx=6)

        # Treeview to display data
        cols = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=30, anchor="center")
        self.tree.heading("nama_siswa", text="Nama Siswa")
        self.tree.column("nama_siswa", width=200)
        self.tree.heading("biologi", text="Biologi")
        self.tree.column("biologi", width=70, anchor="center")
        self.tree.heading("fisika", text="Fisika")
        self.tree.column("fisika", width=70, anchor="center")
        self.tree.heading("inggris", text="Inggris")
        self.tree.column("inggris", width=70, anchor="center")
        self.tree.heading("prediksi_fakultas", text="Prediksi Fakultas")
        self.tree.column("prediksi_fakultas", width=150)
        self.tree.pack(padx=16, pady=(0, 12), fill="both", expand=True)

        self.read_data()

    def clear_inputs(self):
        self.ent_nama.delete(0, tk.END)
        self.ent_biologi.delete(0, tk.END)
        self.ent_fisika.delete(0, tk.END)
        self.ent_inggris.delete(0, tk.END)

    def validate_inputs(self):
        nama_siswa = self.ent_nama.get().strip()
        biologi_str = self.ent_biologi.get().strip()
        fisika_str = self.ent_fisika.get().strip()
        inggris_str = self.ent_inggris.get().strip()

        if not nama_siswa or not biologi_str or not fisika_str or not inggris_str:
            msg.showwarning("Peringatan", "Semua field harus diisi.")
            return None

        try:
            biologi = int(biologi_str)
            fisika = int(fisika_str)
            inggris = int(inggris_str)
            for nilai in (biologi, fisika, inggris):
                if nilai < 0 or nilai > 100:
                    raise ValueError
        except ValueError:
            msg.showerror("Error", "Nilai harus berupa angka antara 0-100.")
            return None

        return nama_siswa, biologi, fisika, inggris

    def prediksi_fakultas(self, biologi, fisika, inggris):
        # Logika prediksi sesuai nilai tertinggi
        if biologi > fisika and biologi > inggris:
            return "Kedokteran"
        elif fisika > biologi and fisika > inggris:
            return "Teknik"
        elif inggris > biologi and inggris >= fisika:
            return "Bahasa"
        else:
            return "Tidak dapat di prediksi"

    def insert_data(self):
        val = self.validate_inputs()
        if not val:
            return
        nama, biologi, fisika, inggris = val
        prediksi = self.prediksi_fakultas(biologi, fisika, inggris)

        try:
            new_id = insertNilaiSiswa(nama, biologi, fisika, inggris, prediksi)
            msg.showinfo("Sukses", f"Data disimpan (id={new_id}). Prediksi fakultas: {prediksi}")
            self.read_data()
            self.clear_inputs()
        except Exception as e:
            msg.showerror("DB Error", str(e))

    def read_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = readNilaiSiswa()
            for r in rows:
                self.tree.insert("", tk.END, values=r)
        except Exception as e:
            msg.showerror("DB Error", str(e))

if __name__ == "__main__":
    app = nilai_siswa()
    app.mainloop()