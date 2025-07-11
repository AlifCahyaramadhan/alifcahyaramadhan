from datetime import datetime
import os, csv

os.system("cls")

data_keuangan = []
file_csv = "data_keuangan_alif.csv"

kategori_pengeluaran = {
    "makan": 0,
    "transportasi": 0,
    "belanja": 0,
    "lainnya": 0
}

def simpan_ke_csv():
    with open(file_csv, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tipe", "jumlah", "kategori", "tanggal"])
        for data in data_keuangan:
            writer.writerow([
                data["tipe"],
                data["jumlah"],
                data.get("kategori", ""),
                data["tanggal"].strftime("%Y-%m-%d %H:%M:%S")
            ])

def baca_dari_csv():
    if not os.path.exists(file_csv):
        return
    with open(file_csv, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tipe = row["tipe"]
            jumlah = int(row["jumlah"])
            tanggal = datetime.strptime(row["tanggal"], "%Y-%m-%d %H:%M:%S")
            if tipe == "pemasukan":
                data_keuangan.append({
                    "tipe": tipe,
                    "jumlah": jumlah,
                    "tanggal": tanggal
                })
            elif tipe == "pengeluaran":
                kategori = row["kategori"] if row["kategori"] in kategori_pengeluaran else "lainnya"
                data_keuangan.append({
                    "tipe": tipe,
                    "jumlah": jumlah,
                    "kategori": kategori,
                    "tanggal": tanggal
                })
                kategori_pengeluaran[kategori] += jumlah

def tampilkan_csv():
    if not data_keuangan:
        print("Belum ada data yang tersimpan.")
        return
    print("\n=== Daftar Transaksi ===")
    for i, d in enumerate(data_keuangan, 1):
        waktu = d['tanggal'].strftime('%Y-%m-%d %H:%M:%S')
        if d["tipe"] == "pemasukan":
            print(f"{i}. {waktu} | {d['tipe']} | Rp{d['jumlah']}")
        else:
            print(f"{i}. {waktu} | {d['tipe']} | Rp{d['jumlah']} | {d['kategori']}")

def catat_pemasukan(jumlah):
    data_keuangan.append({
        "tipe": "pemasukan",
        "jumlah": jumlah,
        "tanggal": datetime.now()
    })
    simpan_ke_csv()
    print("Pemasukan dicatat.\n")

def catat_pengeluaran(jumlah, kategori):
    if kategori not in kategori_pengeluaran:
        kategori = "lainnya"
    data_keuangan.append({
        "tipe": "pengeluaran",
        "jumlah": jumlah,
        "kategori": kategori,
        "tanggal": datetime.now()
    })
    kategori_pengeluaran[kategori] += jumlah
    simpan_ke_csv()
    print("Pengeluaran dicatat.\n")

def laporan_bulanan(bulan, tahun):
    total_masuk = total_keluar = 0
    for data in data_keuangan:
        if data["tanggal"].month == bulan and data["tanggal"].year == tahun:
            if data["tipe"] == "pemasukan":
                total_masuk += data["jumlah"]
            elif data["tipe"] == "pengeluaran":
                total_keluar += data["jumlah"]
    print(f"\nLaporan Bulan {bulan}/{tahun}")
    print(f"Pemasukan  : Rp{total_masuk}")
    print(f"Pengeluaran: Rp{total_keluar}")
    print(f"Saldo      : Rp{total_masuk - total_keluar}\n")

def laporan_tahunan(tahun):
    total_masuk = total_keluar = 0
    for data in data_keuangan:
        if data["tanggal"].year == tahun:
            if data["tipe"] == "pemasukan":
                total_masuk += data["jumlah"]
            elif data["tipe"] == "pengeluaran":
                total_keluar += data["jumlah"]
    print(f"\nLaporan Tahun {tahun}")
    print(f"Pemasukan  : Rp{total_masuk}")
    print(f"Pengeluaran: Rp{total_keluar}")
    print(f"Saldo      : Rp{total_masuk - total_keluar}\n")

def tampilkan_kategori():
    print("\nPengeluaran per Kategori:")
    for kategori, total in kategori_pengeluaran.items():
        print(f" - {kategori.capitalize():<15}: Rp{total}")
    print()

def update_transaksi():
    tampilkan_csv()
    try:
        idx = int(input("Masukkan nomor transaksi yang ingin diubah (1-n): ")) - 1
        if idx < 0 or idx >= len(data_keuangan):
            print("Nomor tidak valid.")
            return
        transaksi = data_keuangan[idx]
        print(f"Data saat ini: {transaksi}")
        jumlah_baru = input("Jumlah baru (kosongkan jika tidak diubah): ")
        kategori_baru = input("Kategori baru (kosongkan jika tidak diubah): ")

        if jumlah_baru:
            if transaksi["tipe"] == "pengeluaran":
                kategori_pengeluaran[transaksi["kategori"]] -= transaksi["jumlah"]
            transaksi["jumlah"] = int(jumlah_baru)

        if transaksi["tipe"] == "pengeluaran" and kategori_baru:
            kategori_lama = transaksi["kategori"]
            kategori_baru = kategori_baru if kategori_baru in kategori_pengeluaran else "lainnya"
            transaksi["kategori"] = kategori_baru
            kategori_pengeluaran[kategori_baru] += transaksi["jumlah"]

        simpan_ke_csv()
        print("Transaksi berhasil diupdate.\n")
    except ValueError:
        print("Input tidak valid.\n")

def hapus_transaksi():
    tampilkan_csv()
    try:
        idx = int(input("Masukkan nomor transaksi yang ingin dihapus (1-n): ")) - 1
        if idx < 0 or idx >= len(data_keuangan):
            print("Nomor tidak valid.")
            return
        transaksi = data_keuangan.pop(idx)
        if transaksi["tipe"] == "pengeluaran":
            kategori_pengeluaran[transaksi["kategori"]] -= transaksi["jumlah"]
        simpan_ke_csv()
        print("Transaksi berhasil dihapus.\n")
    except ValueError:
        print("Input tidak valid.\n")

def menu():
    baca_dari_csv()
    while True:
        print("=== Manajemen Keuangan Sederhana ===")
        print("1. Catat Pemasukan")
        print("2. Catat Pengeluaran")
        print("3. Laporan Bulanan")
        print("4. Laporan Tahunan")
        print("5. Lihat Pengeluaran per Kategori")
        print("6. Tampilkan Semua Transaksi")
        print("7. Update Transaksi")
        print("8. Hapus Transaksi")
        print("9. Keluar")

        pilih = input("Pilih menu (1-9): ")

        if pilih == "1":
            try:
                jumlah = int(input("Jumlah pemasukan (Rp): "))
                catat_pemasukan(jumlah)
            except ValueError:
                print("Jumlah harus angka.\n")

        elif pilih == "2":
            try:
                jumlah = int(input("Jumlah pengeluaran (Rp): "))
                kategori = input("Kategori (makan/transportasi/belanja/lainnya): ").lower()
                catat_pengeluaran(jumlah, kategori)
            except ValueError:
                print("Jumlah harus angka.\n")

        elif pilih == "3":
            try:
                bulan = int(input("Masukkan bulan (1-12): "))
                tahun = int(input("Masukkan tahun: "))
                laporan_bulanan(bulan, tahun)
            except ValueError:
                print("Input bulan/tahun tidak valid.\n")

        elif pilih == "4":
            try:
                tahun = int(input("Masukkan tahun: "))
                laporan_tahunan(tahun)
            except ValueError:
                print("Tahun harus angka.\n")

        elif pilih == "5":
            tampilkan_kategori()

        elif pilih == "6":
            tampilkan_csv()

        elif pilih == "7":
            update_transaksi()

        elif pilih == "8":
            hapus_transaksi()

        elif pilih == "9":
            print("Keluar dari program. Terima kasih!")
            break

        else:
            print("Pilihan tidak dikenali.\n")

if __name__ == "__main__":
    menu()
