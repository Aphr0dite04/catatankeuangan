# Import library yang dibutuhkan
import datetime
import locale
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

# Fungsi untuk menghitung sisa uang bulanan
def hitung_sisa_uang(uang_bulanan, pengeluaran_harian):
    sisa_uang = uang_bulanan - sum(pengeluaran_harian)
    return sisa_uang

# Fungsi untuk mencatat pengeluaran
def catat_pengeluaran(pengeluaran, tanggal, jumlah):
    pengeluaran.append((tanggal, jumlah))
    
# Fungsi untuk memformat uang agar lebih mudah dibaca
def format_uang(jumlah):
    return "Rp {:,}".format(int(jumlah)).replace(",", ".")
    
# Fungsi untuk ekspor data ke PDF
def ekspor_ke_pdf(pengeluaran, uang_bulanan):
    # Menyeting bahasa ke Bahasa Indonesia
    locale.setlocale(locale.LC_TIME, 'id_ID')
    pdf = canvas.Canvas("laporan_keuangan.pdf", pagesize=letter)

    # Menambahkan judul PDF
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, 750, "Laporan Keuangan Harian Arria Gemilang")
    pdf.line(50, 740, 550, 740)

    # Menyiapkan data tabel PDF
    data = [['Tanggal', 'Jumlah']]
    for tanggal, jumlah in pengeluaran:
        hari = tanggal.strftime("%A, %d %B %Y")
        data.append([hari, format_uang(jumlah)])

    # Membuat tabel PDF
    table = Table(data)

    # Menyeting tampilan tabel PDF
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), '#FFFFFF'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    # Menentukan ukuran dan posisi tabel
    table.wrapOn(pdf, 0, 0)
    table.drawOn(pdf, 50, 600)

    # Menghitung sisa uang setelah pengeluaran
    sisa_uang = hitung_sisa_uang(uang_bulanan, [jumlah for _, jumlah in pengeluaran])

    # Menampilkan sisa uang
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 580, f"Sisa uang: {format_uang(sisa_uang)}")

    pdf.save()
    print("Data pengeluaran berhasil diekspor ke PDF.")

def main():
    while True:
        try:
            uang_bulanan = float(input("Masukkan jumlah uang bulanan Anda: "))
            if uang_bulanan <= 0:
                print("Jumlah uang bulanan harus lebih dari 0. Silakan coba lagi.")
                continue
            break
        except ValueError:
            print("Input tidak valid. Masukkan angka yang benar.")
    pengeluaran = []

    # Menghitung jumlah hari dalam bulan ini
    now = datetime.datetime.now()
    jumlah_hari = datetime.date(now.year, now.month+1, 1) - datetime.date(now.year, now.month, 1)
    jumlah_hari = jumlah_hari.days

    for i in range(jumlah_hari):
        tanggal = now + datetime.timedelta(days=i)
        hari = tanggal.strftime("%A, %d %B %Y")

        while True:
            try:
                pengeluaran_hari_ini = float(input(f"Masukkan jumlah pengeluaran Anda untuk {hari} (0 untuk lanjut ke hari berikutnya): "))
                if pengeluaran_hari_ini < 0:
                    print("Jumlah pengeluaran harus tidak negatif. Silakan coba lagi.")
                    continue
                break
            except ValueError:
                print("Input tidak valid. Masukkan angka yang benar.")

        if pengeluaran_hari_ini == 0:
            break

        catat_pengeluaran(pengeluaran, tanggal, pengeluaran_hari_ini)
        sisa_uang = hitung_sisa_uang(uang_bulanan, [jumlah for _, jumlah in pengeluaran])
        print("Sisa uang Anda setelah pengeluaran hari ini: ", format_uang(sisa_uang))

    ekspor_ke_pdf(pengeluaran, uang_bulanan)

if __name__ == '__main__':
    main()