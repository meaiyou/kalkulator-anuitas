import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Kalkulator Anuitas - Kelompok 7", page_icon="🧮", layout="centered")

# Styling CSS untuk background galaksi & kartu transparan mirip versi HTML
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(15, 23, 42, 0.7), rgba(15, 23, 42, 0.7)), 
                    url('https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        color: #f8fafc;
    }
    .card {
        background: rgba(30, 27, 75, 0.85);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(167, 139, 250, 0.3);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi State Halaman
if 'page' not in st.session_state:
    st.session_state.page = 'group'

# Helper Format Rupiah
def fmt_idr(val):
    return f"Rp {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ================= PAGE 1: IDENTITAS KELOMPOK =================
if st.session_state.page == 'group':
    st.markdown("<h1 style='text-align: center; color: white;'>Kalkulator & Simulasi Anuitas</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; margin-bottom: 30px;'>Aplikasi Matematika Keuangan untuk Ulangan / Nilai Tugas</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h2 style="margin-top: 0; color: #c4b5fd;">Selamat Datang!</h2>
        <p>Aplikasi kalkulator dan simulasi tabel pelunasan anuitas ini disusun oleh:</p>
        
        <div style="background-color: rgba(49, 46, 129, 0.6); border-left: 4px solid #a78bfa; padding: 15px 20px; border-radius: 8px; margin-top: 15px;">
            <h3 style="margin-top: 0; margin-bottom: 10px; color: #c4b5fd;">KELOMPOK 7</h3>
            <ol style="padding-left: 20px; margin: 0; font-size: 16px;">
                <li>Aira Safiratus Saniyah</li>
                <li>Alifa Maharany Harjanto Putri</li>
                <li>Lulu Ramadhani</li>
                <li>Nisrina Indah Taqiyyah</li>
                <li>Rakka Galeuh Sajatining Pamadegan</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Mulai Perhitungan ➔", use_container_width=True):
        st.session_state.page = 'input'
        st.rerun()

# ================= PAGE 2: FORM INPUT =================
elif st.session_state.page == 'input':
    st.markdown("<h1 style='text-align: center; color: white;'>Kalkulator & Simulasi Anuitas</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #c4b5fd; margin-top: 0;'>Input Parameter Soal Anuitas</h3>", unsafe_allow_html=True)
    
    satuan = st.selectbox("Jenis Periode pada Soal:", ["Bulanan (Bunga & Jangka Waktu per Bulan)", "Tahunan (Bunga & Jangka Waktu per Tahun)"])
    
    pinjaman = st.number_input("Besar Pinjaman / Modal Awal (M):", value=10000000.0, step=500000.0)
    
    if "Tahunan" in satuan:
        bunga_label = "Suku Bunga per Tahun (%):"
        periode_label = "Lama Periode (Jumlah Tahun):"
    else:
        bunga_label = "Suku Bunga per Bulan (%):"
        periode_label = "Lama Periode (Jumlah Bulan):"
        
    bunga = st.number_input(bunga_label, value=2.0, step=0.1)
    periode = st.number_input(periode_label, value=12, step=1, format="%d")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Hitung & Lihat Hasil ➔", use_container_width=True):
            if pinjaman <= 0 or bunga <= 0 or periode <= 0:
                st.error("Mohon isi semua data angka dengan benar!")
            else:
                st.session_state.pinjaman = pinjaman
                st.session_state.bunga = bunga
                st.session_state.periode = int(periode)
                st.session_state.satuan = satuan
                st.session_state.page = 'result'
                st.rerun()
    with col2:
        if st.button("⬅ Kembali", use_container_width=True):
            st.session_state.page = 'group'
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE 3: HASIL & TABEL & GRAFIK =================
elif st.session_state.page == 'result':
    st.markdown("<h1 style='text-align: center; color: white;'>Kalkulator & Simulasi Anuitas</h1>", unsafe_allow_html=True)
    
    M = st.session_state.pinjaman
    rate_input = st.session_state.bunga
    n = st.session_state.periode
    satuan = st.session_state.satuan
    is_tahun = "Tahunan" in satuan
    
    i = rate_input / 100
    A = M * (i / (1 - (1 + i) ** -n))
    total_pembayaran = A * n
    total_bunga = total_pembayaran - M
    
    # Card Hasil Ringkasan
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #c4b5fd; margin-top: 0;'>Hasil Perhitungan Anuitas</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="padding: 15px; background-color: rgba(49, 46, 129, 0.6); border-radius: 8px; border: 1px solid rgba(167, 139, 250, 0.3); margin-bottom: 15px;">
        <p style="margin: 8px 0; font-size: 16px;"><strong>Besar Anuitas (A):</strong> {fmt_idr(A)} / {'tahun' if is_tahun else 'bulan'}</p>
        <p style="margin: 8px 0; font-size: 16px;"><strong>Total Pembayaran:</strong> {fmt_idr(total_pembayaran)}</p>
        <p style="margin: 8px 0; font-size: 16px;"><strong>Total Bunga:</strong> {fmt_idr(total_bunga)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬅ Hitung Soal Lain / Ubah Input", use_container_width=True):
        st.session_state.page = 'input'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Perhitungan Data Tabel & Grafik
    sisa = M
    schedule_data = []
    chart_labels = []
    chart_bunga = []
    chart_angsuran = []
    
    for period in range(1, n + 1):
        bunga_val = sisa * i
        angsuran_val = A - bunga_val
        if period == n:
            angsuran_val = sisa
        sisa_akhir = max(0.0, sisa - angsuran_val)
        anuitas_aktif = bunga_val + angsuran_val
        
        p_label = f"{'Thn' if is_tahun else 'Bln'} {period}"
        schedule_data.append({
            "Periode": p_label,
            "Sisa Pinjaman Awal": fmt_idr(sisa),
            "Bunga": fmt_idr(bunga_val),
            "Angsuran Pokok": fmt_idr(angsuran_val),
            "Anuitas (A)": fmt_idr(anuitas_aktif),
            "Sisa Pinjaman Akhir": fmt_idr(sisa_akhir)
        })
        
        chart_labels.append(p_label)
        chart_bunga.append(bunga_val)
        chart_angsuran.append(angsuran_val)
        sisa = sisa_akhir

    # Grafik Bunga vs Angsuran
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #c4b5fd; margin-top: 0;'>Grafik Bunga vs Angsuran</h3>", unsafe_allow_html=True)
    df_chart = pd.DataFrame({
        "Angsuran Pokok": chart_angsuran,
        "Bunga": chart_bunga
    }, index=chart_labels)
    st.bar_chart(df_chart, color=["#a78bfa", "#f59e0b"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabel Pelunasan Anuitas
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #c4b5fd; margin-top: 0;'>Tabel Pelunasan Anuitas</h3>", unsafe_allow_html=True)
    df_table = pd.DataFrame(schedule_data)
    st.dataframe(df_table, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
