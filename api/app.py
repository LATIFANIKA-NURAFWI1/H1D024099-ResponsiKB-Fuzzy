from flask import Flask, render_template, request
import math

app = Flask(__name__)
app.secret_key = 'fuzzy_edu_v2_2025'
app.jinja_env.globals.update(enumerate=enumerate, zip=zip)

BAKAT_LIST = [
    {
        "id": "mulut",
        "nama": "Bakat Mulut (Verbal)",
        "deskripsi": "Kemampuan alami untuk berbicara dengan lancar, persuasif, dan memikat. Cocok untuk profesi yang menuntut komunikasi verbal tinggi.",
        "contoh_profesi": ["Public Speaker", "Pengacara", "Broadcaster", "MC/Presenter", "Sales"],
        "prodi_cocok": ["Ilmu Komunikasi", "Hukum", "Psikologi", "Pendidikan", "Hubungan Internasional"]
    },
    {
        "id": "numerikal",
        "nama": "Bakat Numerikal",
        "deskripsi": "Kemampuan menghitung cepat dan memahami pola angka. Pandai berhitung dan mengolah data kuantitatif.",
        "contoh_profesi": ["Matematikawan", "Akuntan", "Analis Data", "Aktuaris", "Statistikawan"],
        "prodi_cocok": ["Matematika", "Akuntansi", "Statistika", "Ekonomi", "Teknik Informatika"]
    },
    {
        "id": "skolastik",
        "nama": "Bakat Skolastik",
        "deskripsi": "Kemampuan alami untuk belajar dan memahami konsep akademik dengan mudah. Cepat menguasai materi ilmiah.",
        "contoh_profesi": ["Ilmuwan", "Programmer", "Peneliti", "Akuntan", "Dosen"],
        "prodi_cocok": ["Teknik Informatika", "Kedokteran", "Farmasi", "Fisika", "Kimia"]
    },
    {
        "id": "absurd",
        "nama": "Bakat Abstrak/Kreatif",
        "deskripsi": "Kemampuan berpikir di luar kotak dan menciptakan ide-ide tidak biasa. Tinggi dalam imajinasi dan inovasi.",
        "contoh_profesi": ["Desainer", "Arsitek", "Seniman", "Inovator", "Game Developer"],
        "prodi_cocok": ["Desain Komunikasi Visual", "Arsitektur", "Seni Rupa", "Animasi", "Kriya"]
    },
    {
        "id": "mekanik",
        "nama": "Bakat Mekanik",
        "deskripsi": "Kemampuan alami untuk memahami dan memperbaiki mesin atau alat. Mudah memahami cara kerja sistem mekanis.",
        "contoh_profesi": ["Insinyur Mesin", "Teknisi", "Mekanik", "Engineer Otomotif"],
        "prodi_cocok": ["Teknik Mesin", "Teknik Otomotif", "Teknik Elektro", "Teknik Industri", "Teknik Sipil"]
    },
    {
        "id": "hubungan",
        "nama": "Bakat Hubungan Sosial",
        "deskripsi": "Kemampuan alami membaca emosi orang lain dan membangun koneksi sosial. Empati dan kecerdasan interpersonal tinggi.",
        "contoh_profesi": ["Psikolog", "Konselor", "HR Manager", "Diplomat", "Social Worker"],
        "prodi_cocok": ["Psikologi", "Ilmu Sosial", "Hubungan Internasional", "Kesejahteraan Sosial", "Bimbingan Konseling"]
    },
    {
        "id": "klerikal",
        "nama": "Bakat Klerikal (Ketelitian)",
        "deskripsi": "Kemampuan bekerja cepat namun tetap teliti. Cocok untuk pekerjaan tulis-menulis, laboratorium, dan administrasi.",
        "contoh_profesi": ["Laboran", "Administrasi", "Sekretaris Eksekutif", "Quality Control", "Apoteker"],
        "prodi_cocok": ["Farmasi", "Kimia", "Administrasi", "Ilmu Perpustakaan", "Akuntansi"]
    },
    {
        "id": "linguistik",
        "nama": "Bakat Bahasa (Linguistik)",
        "deskripsi": "Kemampuan alami menguasai bahasa, baik lisan maupun tulis. Cepat belajar bahasa baru dan ekspresif secara tertulis.",
        "contoh_profesi": ["Jurnalis", "Editor", "Penerjemah", "Pengacara", "Diplomat"],
        "prodi_cocok": ["Sastra Indonesia", "Sastra Inggris", "Jurnalistik", "Hubungan Internasional", "Hukum"]
    },
    {
        "id": "menyanyi",
        "nama": "Bakat Menyanyi/Musik",
        "deskripsi": "Kemampuan menyanyi dengan nada yang tepat dan suara merdu. Kepekaan terhadap irama dan melodi yang tinggi.",
        "contoh_profesi": ["Penyanyi Profesional", "Musisi", "Guru Musik", "Konduktor", "Komposer"],
        "prodi_cocok": ["Seni Musik", "Pendidikan Seni Musik", "Etnomusikologi"]
    },
    {
        "id": "menggambar",
        "nama": "Bakat Menggambar/Visual",
        "deskripsi": "Kemampuan alami menciptakan gambar yang indah atau realistis. Tinggi dalam estetika dan visualisasi.",
        "contoh_profesi": ["Desainer Grafis", "Ilustrator", "Arsitek", "Animator", "Fotografer"],
        "prodi_cocok": ["Desain Grafis", "Arsitektur", "DKV", "Seni Rupa", "Animasi"]
    },
    {
        "id": "spasial",
        "nama": "Bakat Spasial/Relasi Ruang",
        "deskripsi": "Kemampuan analisa ruang dan visualisasi tiga dimensi. Mudah memahami denah, peta, dan konstruksi.",
        "contoh_profesi": ["Arsitek", "Fotografer", "Pilot", "Insinyur Sipil", "Desainer Interior"],
        "prodi_cocok": ["Arsitektur", "Teknik Sipil", "Geografi", "Desain Interior", "Teknik Geologi"]
    },
]

MINAT_LIST = [
    {
        "id": "keilmuan",
        "nama": "Minat Keilmuan & Riset",
        "deskripsi": "Ketertarikan pada pengetahuan, penelitian, dan ilmu pengetahuan mendalam.",
        "prodi_cocok": ["SAINTEK", "Kedokteran", "Farmasi", "Fisika", "Biologi", "Kimia"]
    },
    {
        "id": "seni",
        "nama": "Minat Seni & Budaya",
        "deskripsi": "Ketertarikan pada seni melukis, menari, bermusik, teater, dan ekspresi kreatif.",
        "prodi_cocok": ["Seni Rupa", "Musik", "Tari", "DKV", "Film"]
    },
    {
        "id": "sosial",
        "nama": "Minat Kesejahteraan Sosial",
        "deskripsi": "Suka membantu orang lain, terlibat kegiatan sosial, pelayanan masyarakat.",
        "prodi_cocok": ["Kesejahteraan Sosial", "Psikologi", "Sosiologi", "Pendidikan"]
    },
    {
        "id": "bisnis",
        "nama": "Minat Dunia Usaha & Bisnis",
        "deskripsi": "Ketertarikan untuk berwirausaha, mengelola bisnis, dan strategi ekonomi.",
        "prodi_cocok": ["Manajemen", "Ekonomi", "Bisnis", "Kewirausahaan"]
    },
    {
        "id": "periklanan",
        "nama": "Minat Periklanan & Marketing",
        "deskripsi": "Kecintaan pada dunia kreatif yang mempromosikan produk atau ide. Cocok untuk marketing.",
        "prodi_cocok": ["Ilmu Komunikasi", "Periklanan", "Marketing", "DKV"]
    },
    {
        "id": "akuntansi",
        "nama": "Minat Akuntansi & Keuangan",
        "deskripsi": "Ketertarikan pada angka, pengelolaan keuangan, laporan keuangan, dan audit.",
        "prodi_cocok": ["Akuntansi", "Keuangan", "Perpajakan", "Manajemen Keuangan"]
    },
    {
        "id": "mekanik_minat",
        "nama": "Minat Mekanik & Teknologi",
        "deskripsi": "Kecintaan pada mesin, teknologi, dan rekayasa. Suka mengoprek dan memahami sistem teknis.",
        "prodi_cocok": ["Teknik Mesin", "Teknik Elektro", "Teknik Otomotif", "Teknik Industri"]
    },
    {
        "id": "fisik",
        "nama": "Minat Aktivitas Fisik & Olahraga",
        "deskripsi": "Ketertarikan pada aktivitas fisik, olahraga, kesehatan jasmani.",
        "prodi_cocok": ["Pendidikan Jasmani", "Keolahragaan", "Ilmu Keolahragaan", "Fisioterapi"]
    },
    {
        "id": "petualang",
        "nama": "Minat Petualangan & Alam",
        "deskripsi": "Kecintaan pada eksplorasi, tantangan alam, lingkungan, dan kehidupan luar ruang.",
        "prodi_cocok": ["Geografi", "Kehutanan", "Biologi", "Teknik Geologi", "Ilmu Lingkungan"]
    },
    {
        "id": "kuliner",
        "nama": "Minat Kuliner & Gizi",
        "deskripsi": "Ketertarikan pada dunia masak-memasak, gizi, teknologi pangan.",
        "prodi_cocok": ["Teknologi Pangan", "Gizi", "Tata Boga", "Agribisnis"]
    },
    {
        "id": "keagamaan",
        "nama": "Minat Keagamaan & Spiritual",
        "deskripsi": "Kecintaan pada aktivitas spiritual, ibadah, kajian agama, dan etika.",
        "prodi_cocok": ["Pendidikan Agama", "Syariah", "Filsafat", "Teologi"]
    },
    {
        "id": "teknologi",
        "nama": "Minat Teknologi & Informatika",
        "deskripsi": "Ketertarikan pada pemrograman, sistem komputer, kecerdasan buatan, dan digital.",
        "prodi_cocok": ["Teknik Informatika", "Sistem Informasi", "Ilmu Komputer", "Teknik Elektro"]
    },
    {
        "id": "kesehatan",
        "nama": "Minat Kesehatan & Kedokteran",
        "deskripsi": "Ketertarikan pada ilmu kesehatan, kedokteran, perawatan pasien.",
        "prodi_cocok": ["Kedokteran", "Keperawatan", "Farmasi", "Kebidanan", "Kesehatan Masyarakat"]
    },
    {
        "id": "hukum_minat",
        "nama": "Minat Hukum & Keadilan",
        "deskripsi": "Ketertarikan pada peraturan, keadilan, kebijakan, dan sistem hukum.",
        "prodi_cocok": ["Hukum", "Hubungan Internasional", "Administrasi Negara", "Ilmu Politik"]
    },
    {
        "id": "pendidikan",
        "nama": "Minat Pendidikan & Pengajaran",
        "deskripsi": "Kecintaan pada dunia pengajaran, mendidik generasi muda, dan pedagogik.",
        "prodi_cocok": ["PGSD", "Pendidikan Matematika", "Pendidikan Bahasa", "Bimbingan Konseling"]
    },
]

PRODI_DB = [
    # ---- ITB ----
    {"id": 1, "univ": "ITB", "nama_univ": "Institut Teknologi Bandung", "kota": "Bandung", "prodi": "Teknik Informatika",
     "jenis": "SAINTEK", "prospek": 96, "ukt_max": 12500000, "jarak_ref": {"Jakarta":130,"Bandung":5,"Yogyakarta":420,"Surabaya":750,"Semarang":380,"Purbalingga":360,"Malang":820,"Makassar":2400},
     "minat_cocok": ["teknologi","keilmuan"], "bakat_cocok": ["skolastik","numerikal","absurd"],
     "mapel": ["Matematika","Fisika","Informatika"], "deskripsi": "Program TI terbaik Indonesia, mencetak insinyur perangkat lunak & peneliti AI kelas dunia."},
    {"id": 2, "univ": "ITB", "nama_univ": "Institut Teknologi Bandung", "kota": "Bandung", "prodi": "Teknik Sipil",
     "jenis": "SAINTEK", "prospek": 84, "ukt_max": 11000000, "jarak_ref": {"Jakarta":130,"Bandung":5,"Yogyakarta":420,"Surabaya":750,"Semarang":380,"Purbalingga":360,"Malang":820},
     "minat_cocok": ["mekanik_minat","keilmuan"], "bakat_cocok": ["mekanik","spasial","numerikal"],
     "mapel": ["Matematika","Fisika"], "deskripsi": "Teknik Sipil ITB menghasilkan insinyur infrastruktur yang terlibat dalam proyek nasional strategis."},
    {"id": 3, "univ": "ITB", "nama_univ": "Institut Teknologi Bandung", "kota": "Bandung", "prodi": "Arsitektur",
     "jenis": "SAINTEK", "prospek": 78, "ukt_max": 11000000, "jarak_ref": {"Jakarta":130,"Bandung":5,"Yogyakarta":420,"Purbalingga":360},
     "minat_cocok": ["seni","mekanik_minat"], "bakat_cocok": ["spasial","menggambar","absurd"],
     "mapel": ["Matematika","Seni Rupa","Fisika"], "deskripsi": "Arsitektur ITB terkenal dengan pendekatan teknis dan estetika tinggi, lulusannya memimpin firma arsitek ternama."},
    {"id": 4, "univ": "ITB", "nama_univ": "Institut Teknologi Bandung", "kota": "Bandung", "prodi": "Teknik Kimia",
     "jenis": "SAINTEK", "prospek": 85, "ukt_max": 11000000, "jarak_ref": {"Jakarta":130,"Bandung":5,"Yogyakarta":420,"Purbalingga":360},
     "minat_cocok": ["keilmuan","mekanik_minat"], "bakat_cocok": ["skolastik","klerikal","numerikal"],
     "mapel": ["Kimia","Matematika","Fisika"], "deskripsi": "Lulusan Teknik Kimia ITB dibutuhkan industri petrokimia, farmasi, dan manufaktur skala nasional."},

    # ---- UI ----
    {"id": 5, "univ": "UI", "nama_univ": "Universitas Indonesia", "kota": "Depok", "prodi": "Kedokteran",
     "jenis": "SAINTEK", "prospek": 94, "ukt_max": 25000000, "jarak_ref": {"Jakarta":30,"Bandung":150,"Yogyakarta":530,"Surabaya":780,"Purbalingga":510,"Semarang":450},
     "minat_cocok": ["kesehatan","keilmuan","sosial"], "bakat_cocok": ["skolastik","klerikal","hubungan"],
     "mapel": ["Biologi","Kimia","Matematika","Fisika"], "deskripsi": "FK UI, fakultas kedokteran tertua dan terbaik Indonesia, menghasilkan dokter dan peneliti medis kelas dunia."},
    {"id": 6, "univ": "UI", "nama_univ": "Universitas Indonesia", "kota": "Depok", "prodi": "Ilmu Komputer",
     "jenis": "SAINTEK", "prospek": 95, "ukt_max": 15000000, "jarak_ref": {"Jakarta":30,"Bandung":150,"Yogyakarta":530,"Purbalingga":510},
     "minat_cocok": ["teknologi","keilmuan"], "bakat_cocok": ["skolastik","numerikal","absurd"],
     "mapel": ["Matematika","Fisika"], "deskripsi": "Ilmu Komputer UI salah satu yang paling kompetitif, lulusannya banyak berkarir di perusahaan teknologi global."},
    {"id": 7, "univ": "UI", "nama_univ": "Universitas Indonesia", "kota": "Depok", "prodi": "Hukum",
     "jenis": "SOSHUM", "prospek": 82, "ukt_max": 12000000, "jarak_ref": {"Jakarta":30,"Bandung":150,"Yogyakarta":530,"Purbalingga":510},
     "minat_cocok": ["hukum_minat","sosial"], "bakat_cocok": ["mulut","linguistik","hubungan"],
     "mapel": ["PKN","Sejarah","Bahasa Indonesia"], "deskripsi": "FH UI mencetak pengacara, hakim, notaris, dan pejabat tinggi negara yang disegani."},
    {"id": 8, "univ": "UI", "nama_univ": "Universitas Indonesia", "kota": "Depok", "prodi": "Akuntansi",
     "jenis": "SOSHUM", "prospek": 88, "ukt_max": 13000000, "jarak_ref": {"Jakarta":30,"Bandung":150,"Yogyakarta":530,"Purbalingga":510},
     "minat_cocok": ["akuntansi","bisnis"], "bakat_cocok": ["numerikal","klerikal","skolastik"],
     "mapel": ["Matematika","Ekonomi"], "deskripsi": "Akuntansi UI termasuk program Big4 accounting firm favorit, lulusannya mendominasi posisi CFO perusahaan nasional."},
    {"id": 9, "univ": "UI", "nama_univ": "Universitas Indonesia", "kota": "Depok", "prodi": "Psikologi",
     "jenis": "SOSHUM", "prospek": 80, "ukt_max": 13000000, "jarak_ref": {"Jakarta":30,"Bandung":150,"Yogyakarta":530,"Purbalingga":510},
     "minat_cocok": ["sosial","kesehatan","pendidikan"], "bakat_cocok": ["hubungan","mulut","linguistik"],
     "mapel": ["Biologi","Sosiologi","Bahasa Indonesia"], "deskripsi": "Psikologi UI membuka jalan ke profesi psikolog klinis, industrial, dan konselor berkelas tinggi."},

    # ---- UGM ----
    {"id": 10, "univ": "UGM", "nama_univ": "Universitas Gadjah Mada", "kota": "Yogyakarta", "prodi": "Kedokteran",
     "jenis": "SAINTEK", "prospek": 93, "ukt_max": 22000000, "jarak_ref": {"Yogyakarta":5,"Jakarta":560,"Bandung":420,"Surabaya":320,"Semarang":130,"Purbalingga":100,"Malang":380},
     "minat_cocok": ["kesehatan","keilmuan","sosial"], "bakat_cocok": ["skolastik","klerikal","hubungan"],
     "mapel": ["Biologi","Kimia","Matematika"], "deskripsi": "FK UGM, salah satu tertua dan terbaik, terkenal dengan pendekatan holistik dalam pendidikan dokter."},
    {"id": 11, "univ": "UGM", "nama_univ": "Universitas Gadjah Mada", "kota": "Yogyakarta", "prodi": "Teknik Informatika",
     "jenis": "SAINTEK", "prospek": 95, "ukt_max": 12000000, "jarak_ref": {"Yogyakarta":5,"Jakarta":560,"Bandung":420,"Surabaya":320,"Semarang":130,"Purbalingga":100},
     "minat_cocok": ["teknologi","keilmuan"], "bakat_cocok": ["skolastik","numerikal","absurd"],
     "mapel": ["Matematika","Fisika"], "deskripsi": "TI UGM bersanding dengan ITB sebagai tujuan utama calon insinyur perangkat lunak Indonesia."},
    {"id": 12, "univ": "UGM", "nama_univ": "Universitas Gadjah Mada", "kota": "Yogyakarta", "prodi": "Hukum",
     "jenis": "SOSHUM", "prospek": 81, "ukt_max": 10000000, "jarak_ref": {"Yogyakarta":5,"Jakarta":560,"Bandung":420,"Purbalingga":100},
     "minat_cocok": ["hukum_minat","sosial"], "bakat_cocok": ["mulut","linguistik","hubungan"],
     "mapel": ["PKN","Sejarah","Bahasa Indonesia"], "deskripsi": "Hukum UGM terkenal dengan tradisi akademik kuat dan jaringan alumni yang luas di institusi hukum nasional."},
    {"id": 13, "univ": "UGM", "nama_univ": "Universitas Gadjah Mada", "kota": "Yogyakarta", "prodi": "Manajemen",
     "jenis": "SOSHUM", "prospek": 85, "ukt_max": 12000000, "jarak_ref": {"Yogyakarta":5,"Jakarta":560,"Bandung":420,"Purbalingga":100},
     "minat_cocok": ["bisnis","akuntansi","periklanan"], "bakat_cocok": ["numerikal","hubungan","mulut"],
     "mapel": ["Ekonomi","Matematika"], "deskripsi": "Manajemen UGM mencetak manajer dan wirausahawan yang memimpin perusahaan BUMN maupun swasta nasional."},
    {"id": 14, "univ": "UGM", "nama_univ": "Universitas Gadjah Mada", "kota": "Yogyakarta", "prodi": "Kedokteran Gigi",
     "jenis": "SAINTEK", "prospek": 87, "ukt_max": 20000000, "jarak_ref": {"Yogyakarta":5,"Jakarta":560,"Bandung":420,"Purbalingga":100},
     "minat_cocok": ["kesehatan","keilmuan"], "bakat_cocok": ["skolastik","klerikal","spasial"],
     "mapel": ["Biologi","Kimia"], "deskripsi": "Kedokteran Gigi UGM merupakan salah satu yang terbaik, lulusannya dipercaya memimpin RS dan klinik gigi ternama."},

    # ---- UNAIR ----
    {"id": 15, "univ": "UNAIR", "nama_univ": "Universitas Airlangga", "kota": "Surabaya", "prodi": "Kedokteran",
     "jenis": "SAINTEK", "prospek": 93, "ukt_max": 20000000, "jarak_ref": {"Surabaya":5,"Malang":90,"Yogyakarta":320,"Jakarta":780,"Semarang":280,"Purbalingga":330},
     "minat_cocok": ["kesehatan","keilmuan"], "bakat_cocok": ["skolastik","klerikal","hubungan"],
     "mapel": ["Biologi","Kimia","Fisika"], "deskripsi": "FK UNAIR merupakan rujukan kesehatan nasional di kawasan Indonesia Timur dengan standar internasional."},
    {"id": 16, "univ": "UNAIR", "nama_univ": "Universitas Airlangga", "kota": "Surabaya", "prodi": "Farmasi",
     "jenis": "SAINTEK", "prospek": 88, "ukt_max": 14000000, "jarak_ref": {"Surabaya":5,"Malang":90,"Yogyakarta":320,"Jakarta":780,"Purbalingga":330},
     "minat_cocok": ["kesehatan","keilmuan"], "bakat_cocok": ["klerikal","skolastik","numerikal"],
     "mapel": ["Kimia","Biologi","Matematika"], "deskripsi": "Farmasi UNAIR termasuk terbaik di Indonesia, menghasilkan apoteker dan peneliti farmasi bertaraf nasional."},
    {"id": 17, "univ": "UNAIR", "nama_univ": "Universitas Airlangga", "kota": "Surabaya", "prodi": "Ilmu Hukum",
     "jenis": "SOSHUM", "prospek": 79, "ukt_max": 10000000, "jarak_ref": {"Surabaya":5,"Malang":90,"Yogyakarta":320,"Purbalingga":330},
     "minat_cocok": ["hukum_minat","sosial"], "bakat_cocok": ["mulut","linguistik"],
     "mapel": ["PKN","Bahasa Indonesia"], "deskripsi": "Hukum UNAIR favorit di Jawa Timur dengan koneksi kuat ke pengadilan dan kantor hukum terkemuka."},
    {"id": 18, "univ": "UNAIR", "nama_univ": "Universitas Airlangga", "kota": "Surabaya", "prodi": "Kedokteran Gigi",
     "jenis": "SAINTEK", "prospek": 86, "ukt_max": 18000000, "jarak_ref": {"Surabaya":5,"Yogyakarta":320,"Purbalingga":330},
     "minat_cocok": ["kesehatan","keilmuan"], "bakat_cocok": ["skolastik","klerikal","spasial"],
     "mapel": ["Biologi","Kimia"], "deskripsi": "FKG UNAIR salah satu terbaik di luar Jawa Barat, menghasilkan dokter gigi spesialis berkelas nasional."},

    # ---- ITS ----
    {"id": 19, "univ": "ITS", "nama_univ": "Institut Teknologi Sepuluh Nopember", "kota": "Surabaya", "prodi": "Teknik Sipil",
     "jenis": "SAINTEK", "prospek": 84, "ukt_max": 10000000, "jarak_ref": {"Surabaya":5,"Malang":90,"Yogyakarta":320,"Jakarta":780,"Purbalingga":330},
     "minat_cocok": ["mekanik_minat","keilmuan"], "bakat_cocok": ["mekanik","spasial","numerikal"],
     "mapel": ["Matematika","Fisika"], "deskripsi": "Teknik Sipil ITS dikenal menghasilkan insinyur infrastruktur yang membangun jalan tol, jembatan, dan gedung nasional."},
    {"id": 20, "univ": "ITS", "nama_univ": "Institut Teknologi Sepuluh Nopember", "kota": "Surabaya", "prodi": "Teknik Informatika",
     "jenis": "SAINTEK", "prospek": 94, "ukt_max": 10000000, "jarak_ref": {"Surabaya":5,"Malang":90,"Yogyakarta":320,"Purbalingga":330},
     "minat_cocok": ["teknologi","keilmuan"], "bakat_cocok": ["skolastik","numerikal","absurd"],
     "mapel": ["Matematika","Fisika"], "deskripsi": "TI ITS pesaing kuat ITB dan UGM dalam mencetak insinyur perangkat lunak unggulan nasional."},
    {"id": 21, "univ": "ITS", "nama_univ": "Institut Teknologi Sepuluh Nopember", "kota": "Surabaya", "prodi": "Statistika",
     "jenis": "SAINTEK", "prospek": 88, "ukt_max": 9000000, "jarak_ref": {"Surabaya":5,"Malang":90,"Yogyakarta":320,"Purbalingga":330},
     "minat_cocok": ["keilmuan","akuntansi"], "bakat_cocok": ["numerikal","skolastik","klerikal"],
     "mapel": ["Matematika"], "deskripsi": "Statistika ITS menghasilkan data scientist dan aktuaris yang sangat diminati industri keuangan dan teknologi."},
    {"id": 22, "univ": "ITS", "nama_univ": "Institut Teknologi Sepuluh Nopember", "kota": "Surabaya", "prodi": "Teknik Elektro",
     "jenis": "SAINTEK", "prospek": 89, "ukt_max": 9500000, "jarak_ref": {"Surabaya":5,"Malang":90,"Yogyakarta":320,"Purbalingga":330},
     "minat_cocok": ["mekanik_minat","teknologi"], "bakat_cocok": ["mekanik","numerikal","skolastik"],
     "mapel": ["Matematika","Fisika"], "deskripsi": "Teknik Elektro ITS favorit industri energi, telekomunikasi, dan manufaktur elektronik nasional."},

    # ---- UNDIP ----
    {"id": 23, "univ": "UNDIP", "nama_univ": "Universitas Diponegoro", "kota": "Semarang", "prodi": "Kedokteran",
     "jenis": "SAINTEK", "prospek": 91, "ukt_max": 16000000, "jarak_ref": {"Semarang":5,"Purbalingga":110,"Yogyakarta":125,"Jakarta":460,"Surabaya":280,"Malang":340},
     "minat_cocok": ["kesehatan","keilmuan"], "bakat_cocok": ["skolastik","klerikal","hubungan"],
     "mapel": ["Biologi","Kimia","Fisika"], "deskripsi": "FK UNDIP merupakan pilihan utama calon dokter di Jawa Tengah dengan RS Kariadi sebagai RS pendidikan unggulan."},
    {"id": 24, "univ": "UNDIP", "nama_univ": "Universitas Diponegoro", "kota": "Semarang", "prodi": "Teknik Elektro",
     "jenis": "SAINTEK", "prospek": 87, "ukt_max": 9000000, "jarak_ref": {"Semarang":5,"Purbalingga":110,"Yogyakarta":125,"Jakarta":460},
     "minat_cocok": ["mekanik_minat","teknologi"], "bakat_cocok": ["mekanik","numerikal"],
     "mapel": ["Matematika","Fisika"], "deskripsi": "Teknik Elektro UNDIP dikenal kuat di bidang sistem tenaga dan energi terbarukan."},
    {"id": 25, "univ": "UNDIP", "nama_univ": "Universitas Diponegoro", "kota": "Semarang", "prodi": "Ilmu Hukum",
     "jenis": "SOSHUM", "prospek": 78, "ukt_max": 8000000, "jarak_ref": {"Semarang":5,"Purbalingga":110,"Yogyakarta":125,"Jakarta":460},
     "minat_cocok": ["hukum_minat","sosial"], "bakat_cocok": ["mulut","linguistik"],
     "mapel": ["PKN","Sejarah","Bahasa Indonesia"], "deskripsi": "Hukum UNDIP salah satu program favorit di Jawa Tengah dengan lulusan mendominasi lembaga hukum regional."},
    {"id": 26, "univ": "UNDIP", "nama_univ": "Universitas Diponegoro", "kota": "Semarang", "prodi": "Ilmu Komunikasi",
     "jenis": "SOSHUM", "prospek": 76, "ukt_max": 7000000, "jarak_ref": {"Semarang":5,"Purbalingga":110,"Yogyakarta":125},
     "minat_cocok": ["periklanan","sosial","seni"], "bakat_cocok": ["mulut","linguistik","hubungan"],
     "mapel": ["Bahasa Indonesia","Sosiologi","Bahasa Inggris"], "deskripsi": "Ilmu Komunikasi UNDIP diminati mereka yang ingin berkarir di media, PR, dan industri kreatif."},

    # ---- UNPAD ----
    {"id": 27, "univ": "UNPAD", "nama_univ": "Universitas Padjadjaran", "kota": "Bandung", "prodi": "Ilmu Komunikasi",
     "jenis": "SOSHUM", "prospek": 77, "ukt_max": 8000000, "jarak_ref": {"Bandung":15,"Jakarta":180,"Yogyakarta":430,"Purbalingga":370},
     "minat_cocok": ["periklanan","sosial","seni"], "bakat_cocok": ["mulut","linguistik","hubungan"],
     "mapel": ["Bahasa Indonesia","Sosiologi","Bahasa Inggris"], "deskripsi": "Ilmu Komunikasi UNPAD terkenal melahirkan jurnalis, praktisi PR, dan kreator konten profesional."},
    {"id": 28, "univ": "UNPAD", "nama_univ": "Universitas Padjadjaran", "kota": "Bandung", "prodi": "Kedokteran",
     "jenis": "SAINTEK", "prospek": 92, "ukt_max": 20000000, "jarak_ref": {"Bandung":15,"Jakarta":180,"Yogyakarta":430,"Purbalingga":370},
     "minat_cocok": ["kesehatan","keilmuan"], "bakat_cocok": ["skolastik","klerikal","hubungan"],
     "mapel": ["Biologi","Kimia"], "deskripsi": "FK UNPAD termasuk tertua di Indonesia, dengan RSHS sebagai pusat rujukan kesehatan nasional."},
    {"id": 29, "univ": "UNPAD", "nama_univ": "Universitas Padjadjaran", "kota": "Bandung", "prodi": "Psikologi",
     "jenis": "SOSHUM", "prospek": 79, "ukt_max": 9000000, "jarak_ref": {"Bandung":15,"Jakarta":180,"Yogyakarta":430,"Purbalingga":370},
     "minat_cocok": ["sosial","kesehatan","pendidikan"], "bakat_cocok": ["hubungan","mulut"],
     "mapel": ["Biologi","Sosiologi"], "deskripsi": "Psikologi UNPAD populer dan kompetitif, lulusannya berkarir sebagai psikolog klinis, industri, dan pendidikan."},
    {"id": 30, "univ": "UNPAD", "nama_univ": "Universitas Padjadjaran", "kota": "Bandung", "prodi": "Farmasi",
     "jenis": "SAINTEK", "prospek": 86, "ukt_max": 11000000, "jarak_ref": {"Bandung":15,"Jakarta":180,"Yogyakarta":430,"Purbalingga":370},
     "minat_cocok": ["kesehatan","keilmuan"], "bakat_cocok": ["klerikal","skolastik"],
     "mapel": ["Kimia","Biologi"], "deskripsi": "Farmasi UNPAD menghasilkan apoteker dan peneliti farmasi yang kompetitif di industri farmasi nasional."},

    # ---- IPB ----
    {"id": 31, "univ": "IPB", "nama_univ": "Institut Pertanian Bogor", "kota": "Bogor", "prodi": "Teknologi Pangan",
     "jenis": "SAINTEK", "prospek": 83, "ukt_max": 8000000, "jarak_ref": {"Bogor":5,"Jakarta":70,"Bandung":130,"Yogyakarta":560,"Purbalingga":520},
     "minat_cocok": ["kuliner","keilmuan","petualang"], "bakat_cocok": ["klerikal","skolastik","numerikal"],
     "mapel": ["Kimia","Biologi","Matematika"], "deskripsi": "Teknologi Pangan IPB menghasilkan ahli pangan yang dibutuhkan industri makanan-minuman skala nasional dan ekspor."},
    {"id": 32, "univ": "IPB", "nama_univ": "Institut Pertanian Bogor", "kota": "Bogor", "prodi": "Agribisnis",
     "jenis": "SOSHUM", "prospek": 77, "ukt_max": 7000000, "jarak_ref": {"Bogor":5,"Jakarta":70,"Bandung":130,"Yogyakarta":560,"Purbalingga":520},
     "minat_cocok": ["bisnis","petualang","kuliner"], "bakat_cocok": ["numerikal","hubungan"],
     "mapel": ["Ekonomi","Biologi"], "deskripsi": "Agribisnis IPB mempersiapkan wirausahawan pertanian dan manajer bisnis agrikultur berskala industri."},
    {"id": 33, "univ": "IPB", "nama_univ": "Institut Pertanian Bogor", "kota": "Bogor", "prodi": "Kehutanan",
     "jenis": "SAINTEK", "prospek": 74, "ukt_max": 7000000, "jarak_ref": {"Bogor":5,"Jakarta":70,"Bandung":130,"Yogyakarta":560,"Purbalingga":520},
     "minat_cocok": ["petualang","keilmuan"], "bakat_cocok": ["spasial","mekanik"],
     "mapel": ["Biologi","Kimia","Geografi"], "deskripsi": "Kehutanan IPB terbaik di Indonesia, menghasilkan ahli lingkungan dan pengelola hutan tropis kelas dunia."},

    # ---- UB ----
    {"id": 34, "univ": "UB", "nama_univ": "Universitas Brawijaya", "kota": "Malang", "prodi": "Manajemen",
     "jenis": "SOSHUM", "prospek": 79, "ukt_max": 9000000, "jarak_ref": {"Malang":5,"Surabaya":90,"Yogyakarta":390,"Jakarta":860,"Purbalingga":400},
     "minat_cocok": ["bisnis","akuntansi","periklanan"], "bakat_cocok": ["numerikal","hubungan","mulut"],
     "mapel": ["Ekonomi","Matematika"], "deskripsi": "Manajemen UB mencetak manajer dan wirausahawan kompetitif di dunia bisnis nasional dan global."},
    {"id": 35, "univ": "UB", "nama_univ": "Universitas Brawijaya", "kota": "Malang", "prodi": "Teknik Informatika",
     "jenis": "SAINTEK", "prospek": 92, "ukt_max": 9500000, "jarak_ref": {"Malang":5,"Surabaya":90,"Yogyakarta":390,"Purbalingga":400},
     "minat_cocok": ["teknologi","keilmuan"], "bakat_cocok": ["skolastik","numerikal"],
     "mapel": ["Matematika","Fisika"], "deskripsi": "TI UB terus berkembang dengan laboratorium AI dan riset big data yang menghasilkan lulusan siap industri."},
    {"id": 36, "univ": "UB", "nama_univ": "Universitas Brawijaya", "kota": "Malang", "prodi": "Kedokteran",
     "jenis": "SAINTEK", "prospek": 90, "ukt_max": 18000000, "jarak_ref": {"Malang":5,"Surabaya":90,"Yogyakarta":390,"Purbalingga":400},
     "minat_cocok": ["kesehatan","keilmuan"], "bakat_cocok": ["skolastik","klerikal","hubungan"],
     "mapel": ["Biologi","Kimia"], "deskripsi": "FK UB berkembang pesat dengan RSSA sebagai RS pendidikan utama di kawasan Jawa Timur bagian selatan."},
    {"id": 37, "univ": "UB", "nama_univ": "Universitas Brawijaya", "kota": "Malang", "prodi": "Ilmu Komunikasi",
     "jenis": "SOSHUM", "prospek": 74, "ukt_max": 8000000, "jarak_ref": {"Malang":5,"Surabaya":90,"Yogyakarta":390,"Purbalingga":400},
     "minat_cocok": ["periklanan","sosial","seni"], "bakat_cocok": ["mulut","linguistik"],
     "mapel": ["Bahasa Indonesia","Sosiologi"], "deskripsi": "Ilmu Komunikasi UB dikenal dengan jurusan broadcasting dan media digital yang diminati industri kreatif."},

    # ---- UNS ----
    {"id": 38, "univ": "UNS", "nama_univ": "Universitas Sebelas Maret", "kota": "Surakarta", "prodi": "Pendidikan Guru SD",
     "jenis": "SOSHUM", "prospek": 73, "ukt_max": 5000000, "jarak_ref": {"Surakarta":5,"Yogyakarta":65,"Semarang":110,"Purbalingga":130,"Jakarta":550},
     "minat_cocok": ["pendidikan","sosial"], "bakat_cocok": ["mulut","hubungan","linguistik"],
     "mapel": ["Bahasa Indonesia","IPS","PKN"], "deskripsi": "PGSD UNS menghasilkan guru SD berkualitas yang siap mendidik generasi bangsa di seluruh Indonesia."},
    {"id": 39, "univ": "UNS", "nama_univ": "Universitas Sebelas Maret", "kota": "Surakarta", "prodi": "Ilmu Hukum",
     "jenis": "SOSHUM", "prospek": 76, "ukt_max": 6000000, "jarak_ref": {"Surakarta":5,"Yogyakarta":65,"Semarang":110,"Purbalingga":130},
     "minat_cocok": ["hukum_minat","sosial"], "bakat_cocok": ["mulut","linguistik"],
     "mapel": ["PKN","Sejarah"], "deskripsi": "Hukum UNS dikenal dengan program magang di pengadilan dan lembaga hukum negara yang kuat."},
    {"id": 40, "univ": "UNS", "nama_univ": "Universitas Sebelas Maret", "kota": "Surakarta", "prodi": "Teknik Industri",
     "jenis": "SAINTEK", "prospek": 83, "ukt_max": 7000000, "jarak_ref": {"Surakarta":5,"Yogyakarta":65,"Semarang":110,"Purbalingga":130},
     "minat_cocok": ["mekanik_minat","bisnis"], "bakat_cocok": ["mekanik","numerikal","skolastik"],
     "mapel": ["Matematika","Fisika","Ekonomi"], "deskripsi": "Teknik Industri UNS menghasilkan insinyur yang mahir mengintegrasikan sistem produksi dan manajemen bisnis."},

    # ---- UNSOED ----
    {"id": 41, "univ": "UNSOED", "nama_univ": "Universitas Jenderal Soedirman", "kota": "Purwokerto", "prodi": "Kedokteran",
     "jenis": "SAINTEK", "prospek": 88, "ukt_max": 14000000, "jarak_ref": {"Purwokerto":5,"Purbalingga":25,"Semarang":175,"Yogyakarta":180,"Jakarta":500},
     "minat_cocok": ["kesehatan","keilmuan"], "bakat_cocok": ["skolastik","klerikal","hubungan"],
     "mapel": ["Biologi","Kimia","Fisika"], "deskripsi": "FK UNSOED pilihan utama calon dokter dari wilayah Banyumas Raya, didukung RSUD Margono sebagai RS pendidikan."},
    {"id": 42, "univ": "UNSOED", "nama_univ": "Universitas Jenderal Soedirman", "kota": "Purwokerto", "prodi": "Ilmu Hukum",
     "jenis": "SOSHUM", "prospek": 72, "ukt_max": 5500000, "jarak_ref": {"Purwokerto":5,"Purbalingga":25,"Semarang":175,"Yogyakarta":180},
     "minat_cocok": ["hukum_minat","sosial"], "bakat_cocok": ["mulut","linguistik"],
     "mapel": ["PKN","Sejarah","Bahasa Indonesia"], "deskripsi": "Hukum UNSOED menjadi pilihan strategis bagi pelajar Jawa Tengah tengah yang ingin berkarir di bidang hukum."},
    {"id": 43, "univ": "UNSOED", "nama_univ": "Universitas Jenderal Soedirman", "kota": "Purwokerto", "prodi": "Teknik Informatika",
     "jenis": "SAINTEK", "prospek": 85, "ukt_max": 6500000, "jarak_ref": {"Purwokerto":5,"Purbalingga":25,"Semarang":175,"Yogyakarta":180},
     "minat_cocok": ["teknologi","keilmuan"], "bakat_cocok": ["skolastik","numerikal","absurd"],
     "mapel": ["Matematika","Fisika"], "deskripsi": "TI UNSOED berkembang pesat dengan fokus pada pengembangan software, AI, dan sistem informasi terapan."},
    {"id": 44, "univ": "UNSOED", "nama_univ": "Universitas Jenderal Soedirman", "kota": "Purwokerto", "prodi": "Manajemen",
     "jenis": "SOSHUM", "prospek": 73, "ukt_max": 6000000, "jarak_ref": {"Purwokerto":5,"Purbalingga":25,"Semarang":175,"Yogyakarta":180},
     "minat_cocok": ["bisnis","akuntansi"], "bakat_cocok": ["numerikal","hubungan"],
     "mapel": ["Ekonomi","Matematika"], "deskripsi": "Manajemen UNSOED pilihan efisien bagi pelajar Jawa Tengah tengah yang ingin berkarir di dunia bisnis."},
    {"id": 45, "univ": "UNSOED", "nama_univ": "Universitas Jenderal Soedirman", "kota": "Purwokerto", "prodi": "Agroteknologi",
     "jenis": "SAINTEK", "prospek": 70, "ukt_max": 5000000, "jarak_ref": {"Purwokerto":5,"Purbalingga":25,"Semarang":175,"Yogyakarta":180},
     "minat_cocok": ["petualang","keilmuan","kuliner"], "bakat_cocok": ["spasial","skolastik"],
     "mapel": ["Biologi","Kimia"], "deskripsi": "Agroteknologi UNSOED unggul dalam riset pertanian tropis, didukung lahan kampus yang luas dan lab modern."},
    {"id": 46, "univ": "UNSOED", "nama_univ": "Universitas Jenderal Soedirman", "kota": "Purwokerto", "prodi": "Ilmu Komunikasi",
     "jenis": "SOSHUM", "prospek": 71, "ukt_max": 5500000, "jarak_ref": {"Purwokerto":5,"Purbalingga":25,"Semarang":175,"Yogyakarta":180},
     "minat_cocok": ["periklanan","sosial","seni"], "bakat_cocok": ["mulut","linguistik"],
     "mapel": ["Bahasa Indonesia","Sosiologi"], "deskripsi": "Ilmu Komunikasi UNSOED terus berkembang, diminati pelajar yang ingin berkarir di media dan industri kreatif regional."},
    {"id": 47, "univ": "UNSOED", "nama_univ": "Universitas Jenderal Soedirman", "kota": "Purwokerto", "prodi": "Akuntansi",
     "jenis": "SOSHUM", "prospek": 74, "ukt_max": 6000000, "jarak_ref": {"Purwokerto":5,"Purbalingga":25,"Semarang":175,"Yogyakarta":180},
     "minat_cocok": ["akuntansi","bisnis"], "bakat_cocok": ["numerikal","klerikal"],
     "mapel": ["Ekonomi","Matematika"], "deskripsi": "Akuntansi UNSOED pilihan solid bagi pelajar Jawa Tengah tengah yang ingin berkarir di dunia keuangan dan audit."},

    # ---- UNNES ----
    {"id": 48, "univ": "UNNES", "nama_univ": "Universitas Negeri Semarang", "kota": "Semarang", "prodi": "Pendidikan Matematika",
     "jenis": "SAINTEK", "prospek": 74, "ukt_max": 5000000, "jarak_ref": {"Semarang":5,"Purbalingga":110,"Yogyakarta":125,"Jakarta":460},
     "minat_cocok": ["pendidikan","keilmuan"], "bakat_cocok": ["numerikal","skolastik","mulut"],
     "mapel": ["Matematika"], "deskripsi": "Pendidikan Matematika UNNES mencetak guru matematika unggul yang dibutuhkan sekolah menengah di seluruh Indonesia."},
    {"id": 49, "univ": "UNNES", "nama_univ": "Universitas Negeri Semarang", "kota": "Semarang", "prodi": "Pendidikan Bahasa Inggris",
     "jenis": "SOSHUM", "prospek": 72, "ukt_max": 5000000, "jarak_ref": {"Semarang":5,"Purbalingga":110,"Yogyakarta":125},
     "minat_cocok": ["pendidikan","seni"], "bakat_cocok": ["linguistik","mulut"],
     "mapel": ["Bahasa Inggris","Bahasa Indonesia"], "deskripsi": "Pendidikan Bahasa Inggris UNNES menghasilkan guru bahasa Inggris yang komunikatif dan berstandar internasional."},

    # ---- UNY ----
    {"id": 50, "univ": "UNY", "nama_univ": "Universitas Negeri Yogyakarta", "kota": "Yogyakarta", "prodi": "Pendidikan Teknik Informatika",
     "jenis": "SAINTEK", "prospek": 80, "ukt_max": 5500000, "jarak_ref": {"Yogyakarta":5,"Semarang":130,"Surakarta":65,"Purbalingga":100},
     "minat_cocok": ["teknologi","pendidikan"], "bakat_cocok": ["skolastik","numerikal"],
     "mapel": ["Matematika","Fisika"], "deskripsi": "Pend. Teknik Informatika UNY menghasilkan guru TI yang melek teknologi terkini dan dibutuhkan SMK se-Indonesia."},
    {"id": 51, "univ": "UNY", "nama_univ": "Universitas Negeri Yogyakarta", "kota": "Yogyakarta", "prodi": "Psikologi",
     "jenis": "SOSHUM", "prospek": 78, "ukt_max": 6000000, "jarak_ref": {"Yogyakarta":5,"Semarang":130,"Surakarta":65,"Purbalingga":100},
     "minat_cocok": ["sosial","kesehatan","pendidikan"], "bakat_cocok": ["hubungan","mulut"],
     "mapel": ["Biologi","Sosiologi"], "deskripsi": "Psikologi UNY dikenal dengan riset pendidikan dan klinis yang kuat, serta kolaborasi dengan institusi internasional."},

    # ---- UM ----
    {"id": 52, "univ": "UM", "nama_univ": "Universitas Negeri Malang", "kota": "Malang", "prodi": "Pendidikan Matematika",
     "jenis": "SAINTEK", "prospek": 73, "ukt_max": 5000000, "jarak_ref": {"Malang":5,"Surabaya":90,"Yogyakarta":390,"Purbalingga":400},
     "minat_cocok": ["pendidikan","keilmuan"], "bakat_cocok": ["numerikal","skolastik","mulut"],
     "mapel": ["Matematika"], "deskripsi": "Pend. Matematika UM dikenal dengan kurikulum berbasis penelitian yang menghasilkan guru matematika inovatif."},
    {"id": 53, "univ": "UM", "nama_univ": "Universitas Negeri Malang", "kota": "Malang", "prodi": "Desain Komunikasi Visual",
     "jenis": "SAINTEK", "prospek": 80, "ukt_max": 6000000, "jarak_ref": {"Malang":5,"Surabaya":90,"Yogyakarta":390,"Purbalingga":400},
     "minat_cocok": ["seni","periklanan","teknologi"], "bakat_cocok": ["menggambar","absurd","spasial"],
     "mapel": ["Seni Rupa","Matematika"], "deskripsi": "DKV UM menghasilkan desainer visual kreatif yang dibutuhkan agensi periklanan dan perusahaan media digital."},

    # ---- UNEJ ----
    {"id": 54, "univ": "UNEJ", "nama_univ": "Universitas Jember", "kota": "Jember", "prodi": "Kedokteran Gigi",
     "jenis": "SAINTEK", "prospek": 83, "ukt_max": 12000000, "jarak_ref": {"Jember":5,"Malang":110,"Surabaya":200,"Yogyakarta":480,"Purbalingga":510},
     "minat_cocok": ["kesehatan","keilmuan"], "bakat_cocok": ["skolastik","klerikal","spasial"],
     "mapel": ["Biologi","Kimia"], "deskripsi": "FKG UNEJ salah satu terbaik di Indonesia Timur, menghasilkan dokter gigi spesialis berkualitas tinggi."},
    {"id": 55, "univ": "UNEJ", "nama_univ": "Universitas Jember", "kota": "Jember", "prodi": "Agribisnis",
     "jenis": "SOSHUM", "prospek": 71, "ukt_max": 5500000, "jarak_ref": {"Jember":5,"Malang":110,"Surabaya":200,"Purbalingga":510},
     "minat_cocok": ["bisnis","petualang","kuliner"], "bakat_cocok": ["numerikal","hubungan"],
     "mapel": ["Ekonomi","Biologi"], "deskripsi": "Agribisnis UNEJ memanfaatkan potensi pertanian Jember sebagai laboratorium hidup untuk riset dan praktik lapangan."},
]

KOTA_ASAL = [
    "Jakarta","Depok","Bogor","Tangerang","Bekasi",
    "Bandung","Cimahi","Tasikmalaya","Garut","Cirebon",
    "Yogyakarta","Sleman","Bantul","Gunungkidul",
    "Semarang","Purbalingga","Purwokerto","Cilacap","Magelang","Kudus","Pati","Tegal","Pekalongan","Wonosobo",
    "Surakarta","Klaten","Boyolali","Wonogiri",
    "Surabaya","Malang","Kediri","Blitar","Jember","Banyuwangi","Madiun","Mojokerto","Sidoarjo",
    "Medan","Makassar","Palembang","Pekanbaru","Padang","Balikpapan","Banjarmasin","Denpasar","Pontianak","Manado",
    "Lainnya"
]

def trimf(x, a, b, c):
    if x <= a or x >= c: return 0.0
    elif a < x <= b: return (x - a) / (b - a)
    else: return (c - x) / (c - b)

def trapmf(x, a, b, c, d):
    if x <= a or x >= d: return 0.0
    elif a < x <= b: return (x - a) / (b - a)
    elif b < x <= c: return 1.0
    else: return (d - x) / (d - c)

def fuzz_nilai(x):
    return {
        'rendah': trapmf(x,0,0,60,72),
        'sedang': trimf(x,65,75,85),
        'tinggi': trapmf(x,80,90,100,100)
    }

def fuzz_ekonomi(x):
    return {
        'rendah': trapmf(x,0,0,3,5),
        'menengah': trimf(x,4,7,12),
        'tinggi': trapmf(x,10,15,100,100)
    }

def fuzz_jarak(x):
    return {
        'dekat': trapmf(x,0,0,80,180),
        'sedang': trimf(x,120,300,500),
        'jauh': trapmf(x,400,600,9999,9999)
    }

def fuzz_prospek(x):
    return {
        'rendah': trapmf(x,0,0,60,72),
        'sedang': trimf(x,65,75,85),
        'tinggi': trapmf(x,80,90,100,100)
    }

def hitung_jarak(kota_asal, kota_univ, jarak_ref_prodi):
    if kota_asal == kota_univ:
        return 5
    return jarak_ref_prodi.get(kota_asal, 600)

def hitung_skor_fuzzy(nilai_rapor, ekonomi_juta, kota_asal, bakat_ids, minat_ids, prodi):
    n = fuzz_nilai(nilai_rapor)
    e = fuzz_ekonomi(ekonomi_juta)
    jarak_km = hitung_jarak(kota_asal, prodi['kota'], prodi.get('jarak_ref', {}))
    j = fuzz_jarak(jarak_km)
    p = fuzz_prospek(prodi['prospek'])

    minat_score = 0
    for mid in minat_ids:
        if mid in prodi['minat_cocok']:
            minat_score += 1
    minat_norm = min(1.0, minat_score / max(len(minat_ids), 1))

    bakat_score = 0
    for bid in bakat_ids:
        if bid in prodi['bakat_cocok']:
            bakat_score += 1
    bakat_norm = min(1.0, bakat_score / max(len(bakat_ids), 1))

    ukt = prodi['ukt_max']
    if ekonomi_juta >= 15:   ukt_ok = 1.0
    elif ekonomi_juta >= 7:  ukt_ok = 1.0 if ukt <= 12000000 else 0.7
    elif ekonomi_juta >= 4:  ukt_ok = 1.0 if ukt <= 8000000 else 0.5
    else:                    ukt_ok = 1.0 if ukt <= 5000000 else 0.3

    alpha = {}

    # R1: Nilai tinggi + Minat cocok + Bakat cocok + Prospek tinggi → Sangat Tinggi
    r1 = min(n['tinggi'], minat_norm, bakat_norm, p['tinggi'])
    alpha['sangat_tinggi'] = max(alpha.get('sangat_tinggi',0), r1)

    # R2: Nilai tinggi + Minat cocok + Prospek tinggi + Jarak dekat → Sangat Tinggi
    r2 = min(n['tinggi'], minat_norm, p['tinggi'], j['dekat'])
    alpha['sangat_tinggi'] = max(alpha.get('sangat_tinggi',0), r2)

    # R3: Nilai sedang + Minat cocok + Bakat cocok + Prospek tinggi → Tinggi
    r3 = min(n['sedang'], minat_norm, bakat_norm, p['tinggi'])
    alpha['tinggi'] = max(alpha.get('tinggi',0), r3)

    # R4: Nilai tinggi + Bakat cocok + Prospek tinggi → Tinggi
    r4 = min(n['tinggi'], bakat_norm, p['tinggi'])
    alpha['tinggi'] = max(alpha.get('tinggi',0), r4 * 0.9)

    # R5: Nilai rendah → Rendah
    r5 = n['rendah']
    alpha['rendah'] = max(alpha.get('rendah',0), r5 * 0.85)

    # R6: Minat tidak cocok (minat_norm < 0.3) → kurangi
    if minat_norm < 0.3:
        alpha['rendah'] = max(alpha.get('rendah',0), 0.6 * (0.3 - minat_norm) / 0.3)

    # R7: Ekonomi rendah + UKT tidak terjangkau → Sangat Rendah
    r7 = min(e['rendah'], 1.0 - ukt_ok)
    alpha['sangat_rendah'] = max(alpha.get('sangat_rendah',0), r7 * 0.8)

    # R8: Jarak jauh + Ekonomi rendah → Rendah
    r8 = min(j['jauh'], e['rendah'])
    alpha['rendah'] = max(alpha.get('rendah',0), r8 * 0.7)

    # R9: Nilai sedang + Bakat cocok + Prospek sedang → Sedang
    r9 = min(n['sedang'], bakat_norm, p['sedang'])
    alpha['sedang'] = max(alpha.get('sedang',0), r9)

    # R10: Nilai tinggi + Ekonomi menengah + Prospek tinggi → Tinggi
    r10 = min(n['tinggi'], e['menengah'], p['tinggi'])
    alpha['tinggi'] = max(alpha.get('tinggi',0), r10)

    # R11: Nilai rendah + Bakat tidak cocok → Sangat Rendah
    r11 = min(n['rendah'], 1.0 - bakat_norm)
    alpha['sangat_rendah'] = max(alpha.get('sangat_rendah',0), r11 * 0.85)

    # R12: Jarak dekat + Ekonomi rendah + Prospek tinggi → Sedang
    r12 = min(j['dekat'], e['rendah'], p['tinggi'])
    alpha['sedang'] = max(alpha.get('sedang',0), r12)

    # R13: Prospek rendah → Sedang (max)
    r13 = p['rendah']
    alpha['sedang'] = max(alpha.get('sedang',0), r13 * 0.5)

    # R14: Nilai sedang + Minat sangat cocok + Jarak dekat → Tinggi
    r14 = min(n['sedang'], minat_norm if minat_norm > 0.5 else 0, j['dekat'])
    alpha['tinggi'] = max(alpha.get('tinggi',0), r14)

    # R15: Semua rendah → Sangat Rendah
    r15 = min(n['rendah'], 1.0 - minat_norm, 1.0 - bakat_norm)
    alpha['sangat_rendah'] = max(alpha.get('sangat_rendah',0), r15 * 0.9)

    # R16: Ekonomi tinggi + Nilai tinggi + Prospek tinggi → Sangat Tinggi
    r16 = min(e['tinggi'], n['tinggi'], p['tinggi'])
    alpha['sangat_tinggi'] = max(alpha.get('sangat_tinggi',0), r16)

    # R17: Jarak sedang + Nilai sedang + Prospek tinggi → Sedang
    r17 = min(j['sedang'], n['sedang'], p['tinggi'])
    alpha['sedang'] = max(alpha.get('sedang',0), r17 * 0.85)

    # R18: Bakat sangat cocok + Nilai sedang → Tinggi
    r18 = min(bakat_norm if bakat_norm > 0.6 else 0, n['sedang'])
    alpha['tinggi'] = max(alpha.get('tinggi',0), r18)

    # R19: Nilai tinggi + Jarak jauh + Ekonomi rendah → Sedang (ada kemungkinan meski jauh)
    r19 = min(n['tinggi'], j['jauh'], e['rendah'])
    alpha['sedang'] = max(alpha.get('sedang',0), r19 * 0.7)

    # R20: Minat tinggi + Bakat tinggi + Nilai sedang + Ekonomi menengah → Tinggi
    r20 = min(minat_norm if minat_norm > 0.5 else 0, bakat_norm if bakat_norm > 0.5 else 0, n['sedang'], e['menengah'])
    alpha['tinggi'] = max(alpha.get('tinggi',0), r20)

    if ukt_ok < 1.0:
        penalty = (1.0 - ukt_ok) * 0.25
        alpha['sangat_tinggi'] = max(0, alpha.get('sangat_tinggi',0) - penalty)
        alpha['tinggi'] = max(0, alpha.get('tinggi',0) - penalty * 0.6)

    centers = {'sangat_rendah':10,'rendah':28,'sedang':50,'tinggi':72,'sangat_tinggi':90}
    num = sum(alpha.get(k,0) * v for k,v in centers.items())
    den = sum(alpha.get(k,0) for k in centers)
    skor = num / den if den > 0 else 0
    return round(skor, 1)

def get_label(skor):
    if skor >= 80: return "Sangat Tinggi", "#10b981"
    elif skor >= 65: return "Tinggi", "#3b82f6"
    elif skor >= 45: return "Sedang", "#f59e0b"
    elif skor >= 25: return "Rendah", "#f97316"
    else: return "Sangat Rendah", "#ef4444"

def generate_penjelasan(skor, nilai_rapor, ekonomi, kota_asal, bakat_ids, minat_ids, prodi):
    items = []
    jarak_km = hitung_jarak(kota_asal, prodi['kota'], prodi.get('jarak_ref', {}))

    minat_match = [m for m in minat_ids if m in prodi['minat_cocok']]
    bakat_match = [b for b in bakat_ids if b in prodi['bakat_cocok']]

    if minat_match:
        items.append(f"✅ Minat kamu cocok ({len(minat_match)} dari {len(minat_ids)} minat)")
    else:
        items.append("⚠ Minat kamu kurang cocok dengan bidang ini")

    if bakat_match:
        items.append(f"✅ Bakat kamu mendukung ({len(bakat_match)} dari {len(bakat_ids)} bakat)")
    else:
        items.append("⚠ Bakat kamu kurang linear dengan prodi ini")

    if nilai_rapor >= 88: items.append(f"✅ Nilai rapor sangat kompetitif ({nilai_rapor:.1f})")
    elif nilai_rapor >= 75: items.append(f"✅ Nilai rapor cukup baik ({nilai_rapor:.1f})")
    else: items.append(f"⚠ Nilai rapor perlu ditingkatkan ({nilai_rapor:.1f})")

    ukt = prodi['ukt_max']
    if ekonomi >= 15: items.append(f"✅ Ekonomi sangat mendukung (UKT maks Rp{ukt//1000000:.0f}jt)")
    elif ekonomi >= 7:
        if ukt <= 12000000: items.append("✅ Ekonomi cukup, UKT terjangkau")
        else: items.append(f"⚠ UKT Rp{ukt//1000000:.0f}jt tergolong tinggi, cari beasiswa")
    else:
        if ukt <= 5000000: items.append("✅ UKT masih terjangkau meski ekonomi terbatas")
        else: items.append(f"❌ UKT Rp{ukt//1000000:.0f}jt bisa jadi kendala besar")

    if jarak_km <= 80: items.append(f"✅ Sangat dekat dari kotamu ({jarak_km} km)")
    elif jarak_km <= 300: items.append(f"ℹ Jarak cukup ({jarak_km} km), perlu biaya kos")
    else: items.append(f"⚠ Jarak jauh ({jarak_km} km), biaya hidup lebih tinggi")

    p = prodi['prospek']
    if p >= 90: items.append(f"✅ Prospek kerja sangat tinggi ({p}/100)")
    elif p >= 78: items.append(f"✅ Prospek kerja baik ({p}/100)")
    else: items.append(f"ℹ Prospek kerja sedang ({p}/100)")

    return items

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           bakat_list=BAKAT_LIST,
                           minat_list=MINAT_LIST,
                           kota_list=KOTA_ASAL)

@app.route('/hitung', methods=['POST'])
def hitung():
    errors = []
    try:
        sem_vals = []
        for i in range(1, 6):
            v = request.form.get(f'sem{i}', '').strip()
            sem_vals.append(float(v) if v else 0.0)

        nilai_rapor = sum(sem_vals) / len([v for v in sem_vals if v > 0]) if any(v > 0 for v in sem_vals) else 0

        try: ekonomi = float(request.form.get('ekonomi', 5))
        except: ekonomi = 5.0

        kota_asal = request.form.get('kota_asal', 'Jakarta')
        bakat_ids = request.form.getlist('bakat')
        minat_ids = request.form.getlist('minat')

        for i, v in enumerate(sem_vals):
            if v > 0 and not (0 <= v <= 100):
                errors.append(f"Nilai semester {i+1} harus antara 0-100")

        if not bakat_ids:
            errors.append("Pilih minimal 1 bakat")
        if not minat_ids:
            errors.append("Pilih minimal 1 minat")

        if errors:
            return render_template('index.html', bakat_list=BAKAT_LIST, minat_list=MINAT_LIST,
                                   kota_list=KOTA_ASAL, errors=errors)

        hasil = []
        for prodi in PRODI_DB:
            skor = hitung_skor_fuzzy(nilai_rapor, ekonomi, kota_asal, bakat_ids, minat_ids, prodi)
            label, warna = get_label(skor)
            penjelasan = generate_penjelasan(skor, nilai_rapor, ekonomi, kota_asal, bakat_ids, minat_ids, prodi)
            jarak_km = hitung_jarak(kota_asal, prodi['kota'], prodi.get('jarak_ref', {}))
            hasil.append({
                'prodi': prodi, 'skor': skor, 'label': label,
                'warna': warna, 'penjelasan': penjelasan, 'jarak_km': jarak_km
            })

        hasil.sort(key=lambda x: x['skor'], reverse=True)

        bakat_dipilih = [b for b in BAKAT_LIST if b['id'] in bakat_ids]
        minat_dipilih = [m for m in MINAT_LIST if m['id'] in minat_ids]

        input_data = {
            'sem_vals': sem_vals,
            'nilai_rapor': round(nilai_rapor, 2),
            'ekonomi': ekonomi,
            'kota_asal': kota_asal,
            'bakat_dipilih': bakat_dipilih,
            'minat_dipilih': minat_dipilih,
        }

        return render_template('hasil.html', hasil=hasil, input_data=input_data)

    except Exception as ex:
        return render_template('index.html', bakat_list=BAKAT_LIST, minat_list=MINAT_LIST,
                               kota_list=KOTA_ASAL, errors=[f"Error: {str(ex)}"])

if __name__ == '__main__':
    app.run(debug=True, port=5001)
