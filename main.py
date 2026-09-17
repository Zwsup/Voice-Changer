import sys
import threading
import numpy as np
import sounddevice as sd
import customtkinter as ctk
from pedalboard import (
    Pedalboard, PitchShift, Reverb, Distortion, Gain, 
    HighpassFilter, LowpassFilter, Limiter, Chorus, Delay, 
    Compressor, NoiseGate
)

# ==========================================
# 1. ULTRA KALİTELİ SES MOTORU
# ==========================================
class AudioEngine:
    def __init__(self, update_rms_callback):
        self.sample_rate = 48000
        self.block_size = 1024 # Cızırtısız pürüzsüz aktarım
        self.stream = None
        self.is_running = False
        self.update_rms_callback = update_rms_callback
        
        # Aktif efekt parametreleri
        self.current_preset = []
        self.board = self.build_board()

    def build_board(self):
        """Mükemmel kalite için temel filtrelerle efektleri birleştirir."""
        # 1. Aşama: Temizlik (Gürültü silme ve EQ)
        chain = [
            NoiseGate(threshold_db=-45.0, ratio=10, attack_ms=1.0, release_ms=100),
            HighpassFilter(cutoff_frequency_hz=80)
        ]
        
        # 2. Aşama: Seçilen Efektler
        chain.extend(self.current_preset)
        
        # 3. Aşama: Mastering (Ses patlamalarını önleme ve dengeleme)
        chain.extend([
            Compressor(threshold_db=-15, ratio=3.0, attack_ms=5.0),
            Limiter(threshold_db=-0.5)
        ])
        
        return Pedalboard(chain)

    def set_preset(self, effect_list):
        """Efekt listesini günceller."""
        self.current_preset = effect_list
        self.board = self.build_board()

    def audio_callback(self, indata, outdata, frames, time, status):
        if status:
            pass
        audio_data = indata[:, 0].astype(np.float32)
        rms = np.sqrt(np.mean(audio_data**2))
        self.update_rms_callback(rms)
        
        processed = self.board(audio_data, sample_rate=self.sample_rate)
        processed = np.nan_to_num(processed)
        outdata[:] = processed.reshape(-1, 1)

    def start(self):
        """Varsayılan Windows mikrofon ve hoparlörünü otomatik kullanır."""
        try:
            # device=None demek, Windows varsayılanlarını otomatik al demektir.
            self.stream = sd.Stream(
                device=None,
                samplerate=self.sample_rate,
                blocksize=self.block_size,
                channels=1,
                callback=self.audio_callback
            )
            self.stream.start()
            self.is_running = True
            return True
        except Exception as e:
            print(f"Hata: {e}")
            return False

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
        self.is_running = False


# ==========================================
# 2. DEVASA SES KÜTÜPHANESİ (100'e Doğru Altyapı)
# ==========================================
# Kendi zevkine göre efekt zincirleri ekleyerek burayı sonsuza kadar büyütebilirsin.
VOICE_PRESETS = {
    "İNSAN & VOKAL": {
        "Orijinal Ses": [],
        "Tok Erkek (Hafif)": [PitchShift(-2.5), Gain(2.0), LowpassFilter(6000)],
        "Derin Sesli Adam": [PitchShift(-5.0), Gain(3.0), LowpassFilter(4500)],
        "Anime Kızı / Tiz": [PitchShift(6.0), HighpassFilter(200)],
        "Helyum Balonu": [PitchShift(9.0)],
        "Trap Sanatçısı": [Chorus(rate_hz=1.2, depth=0.4), Reverb(room_size=0.4, wet_level=0.3), Delay(delay_seconds=0.1, mix=0.2)]
    },
    "SİNEMA & KARAKTERLER": {
        "Darth Vader": [PitchShift(-7.0), Distortion(drive_db=5), LowpassFilter(3000), Reverb(room_size=0.2)],
        "Dev Yaratık (Ogre)": [PitchShift(-9.0), Distortion(drive_db=10), LowpassFilter(2000), Gain(4.0)],
        "Minik Goblin": [PitchShift(7.0), Distortion(drive_db=4), HighpassFilter(400)],
        "Zombi Hırıltısı": [PitchShift(-6.0), Chorus(rate_hz=20.0, depth=0.8), Distortion(drive_db=8)],
        "Uzaylı Sinyali": [PitchShift(3.0), Chorus(rate_hz=50.0, depth=0.9), Reverb(room_size=0.6)]
    },
    "TEKNOLOJİ & CİHAZLAR": {
        "Eski Telsiz (Polis)": [HighpassFilter(500), LowpassFilter(2500), Distortion(drive_db=12)],
        "Bozuk Robot": [PitchShift(-1.0), Chorus(rate_hz=30.0, depth=1.0), Distortion(drive_db=15)],
        "Telefondaki Kişi": [HighpassFilter(400), LowpassFilter(3400), Gain(2.0)],
        "Anonim Hacker": [PitchShift(-4.0), Chorus(rate_hz=5.0, depth=0.5), LowpassFilter(4000)],
        "Megafon": [HighpassFilter(800), LowpassFilter(4000), Distortion(drive_db=8), Delay(delay_seconds=0.05, mix=0.3)]
    },
    "MEKAN & ATMOSFER": {
        "Büyük Katedral": [Reverb(room_size=0.9, wet_level=0.6, dry_level=0.7)],
        "Boş Mağara": [Delay(delay_seconds=0.3, mix=0.4), Reverb(room_size=0.7)],
        "Klostrofobik Kutu": [Reverb(room_size=0.1, wet_level=0.5)],
        "Rüya Boyutu": [PitchShift(2.0), Chorus(rate_hz=0.5, depth=0.8), Reverb(room_size=1.0, wet_level=0.5)]
    }
}


# ==========================================
# 3. KULLANICI ARAYÜZÜ (CustomTkinter)
# ==========================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ProVoiceStudio(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("One-Click Voice Studio")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        self.engine = AudioEngine(self.update_meter)
        self.setup_ui()

    def setup_ui(self):
        # ÜST PANEL: Tek Tuşla Başlatma
        self.top_frame = ctk.CTkFrame(self, height=100, corner_radius=10, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=20)
        
        self.toggle_btn = ctk.CTkButton(
            self.top_frame, text=" SES DEĞİŞTİRİCİYİ BAŞLAT ", 
            font=ctk.CTkFont(size=24, weight="bold"), 
            height=60, fg_color="#2ecc71", hover_color="#27ae60",
            command=self.toggle_engine
        )
        self.toggle_btn.pack(expand=True, fill="x")

        # GÖSTERGE PANELI (Ses Seviyesi)
        self.meter_bar = ctk.CTkProgressBar(self, height=15, progress_color="#2ecc71")
        self.meter_bar.pack(fill="x", padx=20, pady=(0, 20))
        self.meter_bar.set(0)

        # ORTA PANEL: Kategorize Edilmiş Devasa Kaydırılabilir Galeri
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="VOICE PRESETS (SES GALERİSİ)", label_font=ctk.CTkFont(size=16, weight="bold"))
        self.scroll_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        # Grid sistemi ile butonları yerleştirme
        self.scroll_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        row_idx = 0
        self.active_button = None # Hangi sesin seçili olduğunu takip etmek için
        
        for category, presets in VOICE_PRESETS.items():
            # Kategori Başlığı
            cat_label = ctk.CTkLabel(self.scroll_frame, text=f"— {category} —", font=ctk.CTkFont(size=14, weight="bold"), text_color="#3498db")
            cat_label.grid(row=row_idx, column=0, columnspan=4, pady=(20, 10), sticky="w")
            row_idx += 1
            
            col_idx = 0
            for name, effect_chain in presets.items():
                btn = ctk.CTkButton(
                    self.scroll_frame, text=name, 
                    height=40,
                    fg_color="#34495e", hover_color="#2980b9",
                    command=lambda n=name, ec=effect_chain: self.apply_preset(n, ec)
                )
                btn.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
                
                col_idx += 1
                if col_idx > 3: # 4 Sütunlu tasarım
                    col_idx = 0
                    row_idx += 1
            row_idx += 1

    def toggle_engine(self):
        """Motoru tek tıkla Windows varsayılanlarında açar/kapatır."""
        if not self.engine.is_running:
            success = self.engine.start()
            if success:
                self.toggle_btn.configure(text=" SİSTEM AKTİF - DURDUR ", fg_color="#e74c3c", hover_color="#c0392b")
        else:
            self.engine.stop()
            self.toggle_btn.configure(text=" SES DEĞİŞTİRİCİYİ BAŞLAT ", fg_color="#2ecc71", hover_color="#27ae60")
            self.meter_bar.set(0)

    def apply_preset(self, name, effect_chain):
        """Seçilen sesi doğrudan motora gönderir."""
        self.engine.set_preset(effect_chain)
        print(f"Aktif Ses: {name}")
        # Burada seçili butonu renklendirme gibi görsel geri bildirimler de eklenebilir.

    def update_meter(self, rms):
        """Mikrofona konuştuğunda ses seviyesini bar üzerinde gösterir."""
        meter_val = min(rms * 15, 1.0) # Hassasiyet ayarı
        self.after(10, lambda: self._set_meter_color(meter_val))

    def _set_meter_color(self, val):
        self.meter_bar.set(val)
        if val > 0.8:
            self.meter_bar.configure(progress_color="#e74c3c") # Kırmızı (Çok yüksek)
        elif val > 0.4:
            self.meter_bar.configure(progress_color="#f1c40f") # Sarı (Normal)
        else:
            self.meter_bar.configure(progress_color="#2ecc71") # Yeşil (Düşük)

    def on_closing(self):
        self.engine.stop()
        self.destroy()

if __name__ == "__main__":
    app = ProVoiceStudio()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()