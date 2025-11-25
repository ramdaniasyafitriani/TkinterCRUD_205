import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk

def koneksi():
    con = sqlite3.connect("nilai_siswa.db")
    return con

#FUNGSI MEMBUAT TABEL BARU

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

#FUNGSI MENAMBAH DATA
def insertNilaiSiswa(nama_Siswa: str, biologi: int, fisika: int, inggris: int, prediksi_fakultas : str):
    con = koneksi()
    cur = con.cursor()
    cur.execute("INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) VALUES (?, ?, ?, ?, ?)", 
                (nama_Siswa, biologi, fisika, inggris, prediksi_fakultas))
    con.commit()
    rowid = cur.lastrowid
    con.close()
    return rowid

#FUNGSI MEMBACA DATA
def readNilaiSiswa():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows

#FUNGSI MENGUPDATE DATA
def updateNilaiSiswa(id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas):
    con = koneksi()
    cur = con.cursor()
    cur.execute(
        "UPDATE nilai_siswa SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=? WHERE id=?",
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas, id)
    )
    con.commit()
    con.close()
 
#FUNGSI MENGHAPUS DATA
def deleteNilaiSiswa(id):
    con = koneksi()
    cur = con.cursor()
    cur.execute("DELETE FROM nilai_siswa WHERE id=?", (id,))
    con.commit()
    con.close()

create_table()

#MEMBUAT KELAS UTAMA NILAI SISWA
class nilai_siswa(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input dan Prediksi Fakultas")
        self.geometry("700x500")
        self.configure(bg="#f0f2f5")

    # Frame for input fields and buttons
        frm = tk.Frame(self, bg="#C29FDF", padx=12, pady=12)
        frm.pack(padx=16, pady=12, fill="x")

        # Input fields
        tk.Label(frm, text="Nama Siswa:", bg="#f5dd54").grid(row=0, column=0, sticky="w")
        self.ent_nama = tk.Entry(frm, width=30)
        self.ent_nama.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Nilai Biologi:", bg="#eb982c").grid(row=1, column=0, sticky="w")
        self.ent_biologi = tk.Entry(frm, width=30)
        self.ent_biologi.grid(row=1, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Nilai Fisika:", bg="#e9b0b0").grid(row=2, column=0, sticky="w")
        self.ent_fisika = tk.Entry(frm, width=30)
        self.ent_fisika.grid(row=2, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Nilai Inggris:", bg="#73ca68").grid(row=3, column=0, sticky="w")
        self.ent_inggris = tk.Entry(frm, width=30)
        self.ent_inggris.grid(row=3, column=1, sticky="w", padx=6, pady=6)

        # Buttons frame
        btn_frame = tk.Frame(frm, bg="#99c3f3")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(6, 0))

        self.btn_submit = tk.Button(btn_frame, bg="#f17589", text="Submit Nilai", width=15, command=self.insert_data)
        self.btn_submit.pack(side="left", padx=6)

        self.btn_update = tk.Button(btn_frame, bg="#6DA5E6", text="Update Data", width=15, command=self.update_data)
        self.btn_update.pack(side="left", padx=6)

        self.btn_delete = tk.Button(btn_frame, bg="#64DFA1", text="Delete Data", width=15, command=self.delete_data)
        self.btn_delete.pack(side="left", padx=6)

        self.btn_refresh = tk.Button(btn_frame, bg="#FF305D", text="Refresh Data", width=15, command=self.read_data)
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

        self.tree.bind("<ButtonRelease-1>", lambda e: self.fill_inputs_from_selected())

        self.read_data()

    #FUNGSI MEMBERSIHKAN INPUT FIELDS
    def clear_inputs(self):
        self.ent_nama.delete(0, tk.END)
        self.ent_biologi.delete(0, tk.END)
        self.ent_fisika.delete(0, tk.END)
        self.ent_inggris.delete(0, tk.END)
        if hasattr(self, 'selected_id'):
            del self.selected_id

    #FUNGSI VALIDASI INPUT
    def validate_inputs(self):
        nama_siswa = self.ent_nama.get().strip()
        biologi_str = self.ent_biologi.get().strip()
        fisika_str = self.ent_fisika.get().strip()
        inggris_str = self.ent_inggris.get().strip()

        if not nama_siswa or not biologi_str or not fisika_str or not inggris_str:
            msg.showwarning("Peringatan", "Semua field harus diisi.")
            return None
        
        # Validasi nilai harus angka antara 0-100
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

    #FUNGSI PREDIKSI FAKULTAS
    def prediksi_fakultas(self, biologi, fisika, inggris):
        if biologi > fisika and biologi > inggris:
            return "Kedokteran"
        elif fisika > biologi and fisika > inggris:
            return "Teknik"
        elif inggris > biologi and inggris >= fisika:
            return "Bahasa"
        else:
            return "Tidak dapat diprediksi"

    #FUNGSI INSERT DATA
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

    #FUNGSI MENDAPATKAN BARIS TERPILIH
    def get_selected_row(self):
        selected = self.tree.focus()
        if not selected:
            msg.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu.")
            return None
        return self.tree.item(selected)['values']

    #FUNGSI MENGISI INPUT DARI BARIS TERPILIH
    def fill_inputs_from_selected(self):
        row = self.get_selected_row()
        if row:
            _id, nama, biologi, fisika, inggris, prediksi = row
            self.ent_nama.delete(0, tk.END)
            self.ent_biologi.delete(0, tk.END)
            self.ent_fisika.delete(0, tk.END)
            self.ent_inggris.delete(0, tk.END)
            self.ent_nama.insert(0, nama)
            self.ent_biologi.insert(0, biologi)
            self.ent_fisika.insert(0, fisika)
            self.ent_inggris.insert(0, inggris)
            self.selected_id = _id

    #FUNGSI UPDATE DATA
    def update_data(self):
        if not hasattr(self, 'selected_id'):
            msg.showwarning("Peringatan", "Pilih data yang ingin diupdate.")
            return
        val = self.validate_inputs()
        if not val:
            return
        nama, biologi, fisika, inggris = val
        prediksi = self.prediksi_fakultas(biologi, fisika, inggris)
        try:
            updateNilaiSiswa(self.selected_id, nama, biologi, fisika, inggris, prediksi)
            msg.showinfo("Sukses", f"Data berhasil diupdate. Prediksi fakultas: {prediksi}")
            self.read_data()
            self.clear_inputs()
        except Exception as e:
            msg.showerror("DB Error", str(e))

    #FUNGSI DELETE DATA
    def delete_data(self):
        row = self.get_selected_row()
        if not row:
            return
        _id = row[0]
        confirm = msg.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?")
        if confirm:
            try:
                deleteNilaiSiswa(_id)
                msg.showinfo("Sukses", "Data berhasil dihapus.")
                self.read_data()
                self.clear_inputs()
            except Exception as e:
                msg.showerror("DB Error", str(e))

    #FUNGSI MEMBACA DATA
    def read_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = readNilaiSiswa()
            for r in rows:
                self.tree.insert("", tk.END, values=r)
        except Exception as e:
            msg.showerror("DB Error", str(e))

#JALANKAN APLIKASI
if __name__ == "__main__":
    app = nilai_siswa()
    app.mainloop()
