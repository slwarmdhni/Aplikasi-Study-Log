catatan = []
# Target harian (menit). None berarti belum diatur.
target_harian = None

def tambah_catatan():
    """Minta input mapel, topik, durasi (menit) dan simpan ke list catatan."""
    mapel = input("Masukkan nama mata pelajaran: ").strip()
    topik = input("Masukkan topik: ").strip()

    # Validasi durasi agar berupa angka (menit)
    while True:
        durasi_input = input("Masukkan durasi belajar (menit): ").strip()
        if durasi_input.isdigit():
            durasi = int(durasi_input)
            break
        try:
            # Terima juga input desimal, mis. '45.0'
            durasi = int(float(durasi_input))
            break
        except ValueError:
            print("Durasi harus berupa angka. Silakan coba lagi.")

    # Simpan catatan sebagai dictionary sederhana
    catatan.append({
        'mapel': mapel,
        'topik': topik,
        'durasi': durasi
    })

    print("✅ Catatan berhasil ditambahkan!")


def lihat_catatan():
    """Tampilkan semua catatan yang tersimpan dalam satu tabel yang juga berisi ringkasan target.

    Selain itu, tampilkan ringkasan per mata pelajaran (jumlah catatan, total durasi, rata-rata) dalam tabel di bawah.
    """
    if not catatan:
        print("Belum ada catatan.")
        return

    # Hitung total dan status target
    total = sum(c['durasi'] for c in catatan)
    if target_harian is not None and target_harian > 0:
        tercapai_pct = min(100, int((total / target_harian) * 100))
        sisa = max(0, target_harian - total)
        target_str = str(target_harian)
        tercapai_str = f"{tercapai_pct}%"
        sisa_str = str(sisa)
    else:
        target_str = '-'
        tercapai_str = '-'
        sisa_str = '-'

    # Hitung lebar kolom berdasarkan konten + kolom ringkasan
    no_width = len(str(len(catatan)))
    mapel_width = max(len('Mata pelajaran'), max((len(c['mapel']) for c in catatan), default=0), len('TOTAL'))
    topik_width = max(len('Topik'), max((len(c['topik']) for c in catatan), default=0), len(f"{len(catatan)} catatan"))
    durasi_width = max(len('Durasi (menit)'), max((len(str(c['durasi'])) for c in catatan), default=0), len(str(total)))

    target_w = max(len('🎯 Target'), len(target_str))
    tercapai_w = max(len('📊 Tercapai'), len(tercapai_str))
    sisa_w = max(len('🔁 Sisa (menit)'), len(sisa_str))

    # Header lengkap
    header_parts = [f"{'No':>{no_width}}", f"{'Mata pelajaran':<{mapel_width}}", f"{'Topik':<{topik_width}}", f"{'Durasi (menit)':>{durasi_width}}", f"{'🎯 Target':>{target_w}}", f"{'📊 Tercapai':>{tercapai_w}}", f"{'🔁 Sisa (menit)':>{sisa_w}}"]
    header = '  '.join(header_parts)
    sep = '-' * len(header)

    print('\nDaftar catatan:')
    print(sep)
    print(header)
    print(sep)

    # Baris data (kolom ringkasan dikosongkan)
    for i, c in enumerate(catatan, start=1):
        row = f"{i:>{no_width}}.  {c['mapel']:<{mapel_width}}  {c['topik']:<{topik_width}}  {c['durasi']:>{durasi_width}}  {''.rjust(target_w)}  {''.rjust(tercapai_w)}  {''.rjust(sisa_w)}"
        print(row)

    print(sep)

    # Baris ringkasan di bawah tabel (diisi kolom ringkasan)
    summary = f"{'':>{no_width}}  {'TOTAL':<{mapel_width}}  {str(len(catatan)) + ' catatan':<{topik_width}}  {str(total):>{durasi_width}}  {target_str:>{target_w}}  {tercapai_str:>{tercapai_w}}  {sisa_str:>{sisa_w}}"
    print(summary)
    print(sep)

    # Ringkasan per mata pelajaran (gabungkan mapel seperti Sejarah, Seni Budaya, Ekonomi, PPKn)
    from collections import defaultdict
    grp = defaultdict(lambda: {'count': 0, 'total': 0})
    for c in catatan:
        grp[c['mapel']]['count'] += 1
        grp[c['mapel']]['total'] += c['durasi']

    if grp:
        # Hitung lebar kolom untuk ringkasan per mapel
        mapel_w = max(len('Mata pelajaran'), max((len(m) for m in grp), default=0))
        count_w = max(len('Jumlah'), max((len(str(g['count'])) for g in grp.values()), default=0))
        total_w = max(len('Total (menit)'), max((len(str(g['total'])) for g in grp.values()), default=0))
        avg_w = len('Rata-rata')

        header2 = f"{'Mata pelajaran':<{mapel_w}}  {'Jumlah':>{count_w}}  {'Total (menit)':>{total_w}}  {'Rata-rata':>{avg_w}}"
        sep2 = '-' * len(header2)

        print('\nRingkasan per mata pelajaran:')
        print(sep2)
        print(header2)
        print(sep2)

        # Baris per mapel
        for m, g in sorted(grp.items()):
            avg = g['total'] / g['count'] if g['count'] > 0 else 0
            # Tampilkan rata-rata dengan 1 desimal jika tidak bulat
            if avg.is_integer():
                avg_str = str(int(avg))
            else:
                avg_str = f"{avg:.1f}"
            print(f"{m:<{mapel_w}}  {g['count']:>{count_w}}  {g['total']:>{total_w}}  {avg_str:>{avg_w}}")

        print(sep2)


def total_waktu():
    """Hitung dan tampilkan total durasi belajar dari semua catatan.

    - Jika tidak ada catatan, tampilkan pesan yang sesuai.
    - Menampilkan total dalam menit dan juga dalam format jam + menit.
    - Mengembalikan total menit (int) untuk penggunaan programatik.
    """
    if not catatan:
        print("Belum ada catatan.")
        return 0

    total = sum(c['durasi'] for c in catatan)
    jam = total // 60
    menit = total % 60

    if jam > 0:
        print(f"⏱️ Total waktu belajar: {total} menit ({jam} jam {menit} menit)")
    else:
        print(f"⏱️ Total waktu belajar: {total} menit")

    return total


def set_target_harian():
    """Meminta pengguna mengatur target harian (menit)."""
    global target_harian
    while True:
        nilai = input("🎯 Masukkan target harian (menit): ").strip()
        if nilai.isdigit():
            target_harian = int(nilai)
            print("✅ Target harian disimpan!")
            break
        try:
            # terima juga angka desimal, dibulatkan ke int
            target_harian = int(float(nilai))
            print("✅ Target harian disimpan!")
            break
        except ValueError:
            print("Masukkan angka yang valid (menit). Coba lagi.")


def lihat_target_harian():
    """Tampilkan target harian dalam format tabel sederhana beserta progres saat ini."""
    global target_harian
    if target_harian is None:
        print("Belum ada target harian. Gunakan opsi untuk mengatur target terlebih dahulu.")
        return

    total = sum(c['durasi'] for c in catatan)
    tercapai = min(100, int((total / target_harian) * 100)) if target_harian > 0 else 0
    sisa = max(0, target_harian - total)

    # Buat tabel ringkas
    headers = ['🎯 Target (menit)', '⏱️ Total (menit)', '📊 Tercapai', '🔁 Sisa (menit)']
    vals = [str(target_harian), str(total), f"{tercapai}%", str(sisa)]

    col_widths = [max(len(h), len(v)) for h, v in zip(headers, vals)]
    sep = ' | '

    header_line = sep.join(h.ljust(w) for h, w in zip(headers, col_widths))
    val_line = sep.join(v.ljust(w) for v, w in zip(vals, col_widths))

    print('\nTarget Harian:')
    print('-' * len(header_line))
    print(header_line)
    print('-' * len(header_line))
    print(val_line)
    print('-' * len(header_line))


def target_menu():
    """Sub-menu untuk fitur target harian."""
    while True:
        print("\n--- Menu Target Harian 🎯 ---")
        print("1. Atur target harian")
        print("2. Lihat target & progres")
        print("3. Kembali")

        pilihan = input("Pilih: ")
        if pilihan == '1':
            set_target_harian()
        elif pilihan == '2':
            lihat_target_harian()
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak valid")


def menu():
    print("\n=== Study Log App ===")
    print("1. Tambah catatan belajar ✍️")
    print("2. Lihat catatan belajar 📋")
    print("3. Total waktu belajar ⏱️")
    print("4. Keluar ✅")
    print("5. Target harian 🎯")

while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_catatan()
    elif pilihan == "2":
        lihat_catatan()
    elif pilihan == "3":
        total_waktu()
    elif pilihan == "4":
        print("Terima kasih, terus semangat belajar!")
        break
    elif pilihan == "5":
        target_menu()
    else:
        print("Pilihan tidak valid")