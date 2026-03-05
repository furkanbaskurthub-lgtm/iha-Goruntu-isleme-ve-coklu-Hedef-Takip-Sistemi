"""
İHA HUD (Heads-Up Display) Overlay
Gerçek İHA görünümü için profesyonel arayüz
"""
import cv2
import numpy as np
from datetime import datetime
import math


class UAV_HUD:
    """İHA HUD overlay sistemi"""
    
    def __init__(self, width: int, height: int):
        """
        Args:
            width: Video genişliği
            height: Video yüksekliği
        """
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Renkler
        self.color_primary = (0, 255, 0)      # Yeşil
        self.color_secondary = (0, 200, 255)  # Turuncu
        self.color_warning = (0, 165, 255)    # Turuncu
        self.color_critical = (0, 0, 255)     # Kırmızı
        self.color_text = (255, 255, 255)     # Beyaz
        self.color_bg = (0, 0, 0)             # Siyah
    
    def draw_crosshair(self, frame: np.ndarray) -> np.ndarray:
        """Merkez nişangah çiz"""
        
        # Merkez daire
        cv2.circle(frame, (self.center_x, self.center_y), 30, self.color_primary, 2)
        cv2.circle(frame, (self.center_x, self.center_y), 3, self.color_primary, -1)
        
        # Çizgiler
        line_length = 50
        gap = 35
        
        # Üst
        cv2.line(frame, 
                (self.center_x, self.center_y - gap),
                (self.center_x, self.center_y - gap - line_length),
                self.color_primary, 2)
        
        # Alt
        cv2.line(frame,
                (self.center_x, self.center_y + gap),
                (self.center_x, self.center_y + gap + line_length),
                self.color_primary, 2)
        
        # Sol
        cv2.line(frame,
                (self.center_x - gap, self.center_y),
                (self.center_x - gap - line_length, self.center_y),
                self.color_primary, 2)
        
        # Sağ
        cv2.line(frame,
                (self.center_x + gap, self.center_y),
                (self.center_x + gap + line_length, self.center_y),
                self.color_primary, 2)
        
        return frame
    
    def draw_corner_brackets(self, frame: np.ndarray) -> np.ndarray:
        """Köşe parantezleri çiz"""
        
        margin = 20
        length = 40
        thickness = 2
        
        # Sol üst
        cv2.line(frame, (margin, margin), (margin + length, margin), 
                self.color_primary, thickness)
        cv2.line(frame, (margin, margin), (margin, margin + length), 
                self.color_primary, thickness)
        
        # Sağ üst
        cv2.line(frame, (self.width - margin, margin), 
                (self.width - margin - length, margin), 
                self.color_primary, thickness)
        cv2.line(frame, (self.width - margin, margin), 
                (self.width - margin, margin + length), 
                self.color_primary, thickness)
        
        # Sol alt
        cv2.line(frame, (margin, self.height - margin), 
                (margin + length, self.height - margin), 
                self.color_primary, thickness)
        cv2.line(frame, (margin, self.height - margin), 
                (margin, self.height - margin - length), 
                self.color_primary, thickness)
        
        # Sağ alt
        cv2.line(frame, (self.width - margin, self.height - margin), 
                (self.width - margin - length, self.height - margin), 
                self.color_primary, thickness)
        cv2.line(frame, (self.width - margin, self.height - margin), 
                (self.width - margin, self.height - margin - length), 
                self.color_primary, thickness)
        
        return frame
    
    def draw_telemetry_panel(
        self, 
        frame: np.ndarray,
        altitude: float = 100.0,
        speed: float = 0.0,
        heading: float = 0.0,
        gps: tuple = None,
        battery: int = 100,
        signal: int = 100
    ) -> np.ndarray:
        """Telemetri paneli çiz (sol üst)"""
        
        x = 60
        y = 30
        line_height = 25
        
        # Arka plan (yarı saydam)
        overlay = frame.copy()
        cv2.rectangle(overlay, (x-10, y-10), (x+250, y+line_height*7+10), 
                     self.color_bg, -1)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
        
        # Telemetri bilgileri
        telemetry = [
            f"ALT: {altitude:.1f}m",
            f"SPD: {speed:.1f}m/s",
            f"HDG: {heading:.0f}°",
            f"BAT: {battery}%",
            f"SIG: {signal}%",
        ]
        
        if gps:
            telemetry.append(f"GPS: {gps[0]:.5f},{gps[1]:.5f}")
        
        for i, text in enumerate(telemetry):
            color = self.color_primary
            
            # Uyarı renkleri
            if "BAT" in text and battery < 30:
                color = self.color_warning
            elif "BAT" in text and battery < 15:
                color = self.color_critical
            
            cv2.putText(frame, text, (x, y + i * line_height),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame
    
    def draw_target_info_panel(
        self,
        frame: np.ndarray,
        target_count: int,
        tracked_count: int,
        frame_num: int,
        total_frames: int
    ) -> np.ndarray:
        """Hedef bilgi paneli (sağ üst)"""
        
        x = self.width - 250
        y = 30
        line_height = 25
        
        # Arka plan
        overlay = frame.copy()
        cv2.rectangle(overlay, (x-10, y-10), (x+240, y+line_height*4+10),
                     self.color_bg, -1)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
        
        # Bilgiler
        info = [
            f"TARGETS: {target_count}",
            f"TRACKED: {tracked_count}",
            f"FRAME: {frame_num}/{total_frames}",
            f"TIME: {datetime.now().strftime('%H:%M:%S')}"
        ]
        
        for i, text in enumerate(info):
            cv2.putText(frame, text, (x, y + i * line_height),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color_secondary, 2)
        
        return frame
    
    def draw_horizon_line(self, frame: np.ndarray, pitch: float = 0.0) -> np.ndarray:
        """Yapay ufuk çizgisi"""
        
        # Basit yatay çizgi (pitch açısı ile hareket edebilir)
        y_offset = int(pitch * 2)  # Pitch'e göre hareket
        y = self.center_y + y_offset
        
        # Merkez çizgi
        line_length = 200
        cv2.line(frame,
                (self.center_x - line_length, y),
                (self.center_x + line_length, y),
                self.color_primary, 2)
        
        # Küçük işaretler
        for i in range(-3, 4):
            if i == 0:
                continue
            x_pos = self.center_x + i * 60
            mark_height = 10 if i % 2 == 0 else 5
            cv2.line(frame,
                    (x_pos, y - mark_height),
                    (x_pos, y + mark_height),
                    self.color_primary, 1)
        
        return frame
    
    def draw_altitude_ladder(self, frame: np.ndarray, altitude: float) -> np.ndarray:
        """Yükseklik merdiveni (sağ taraf)"""
        
        x = self.width - 80
        y_center = self.center_y
        
        # Mevcut yükseklik
        cv2.putText(frame, f"{altitude:.0f}m", (x, y_center),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.color_primary, 2)
        
        # Merdivenler
        for i in range(-2, 3):
            alt = altitude + i * 20
            y = y_center + i * 40
            
            if 0 <= y < self.height:
                cv2.line(frame, (x-20, y), (x-5, y), self.color_primary, 1)
                cv2.putText(frame, f"{alt:.0f}", (x-60, y+5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.color_primary, 1)
        
        return frame
    
    def draw_speed_ladder(self, frame: np.ndarray, speed: float) -> np.ndarray:
        """Hız merdiveni (sol taraf)"""
        
        x = 80
        y_center = self.center_y
        
        # Mevcut hız
        cv2.putText(frame, f"{speed:.0f}m/s", (x-60, y_center),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.color_primary, 2)
        
        # Merdivenler
        for i in range(-2, 3):
            spd = max(0, speed + i * 5)
            y = y_center + i * 40
            
            if 0 <= y < self.height:
                cv2.line(frame, (x+5, y), (x+20, y), self.color_primary, 1)
                cv2.putText(frame, f"{spd:.0f}", (x+25, y+5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.color_primary, 1)
        
        return frame
    
    def draw_compass(self, frame: np.ndarray, heading: float) -> np.ndarray:
        """Pusula (üst orta)"""
        
        x_center = self.center_x
        y = 60
        width = 300
        
        # Arka plan
        overlay = frame.copy()
        cv2.rectangle(overlay, (x_center - width//2, y-20), 
                     (x_center + width//2, y+20), self.color_bg, -1)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
        
        # Yönler
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        angles = [0, 45, 90, 135, 180, 225, 270, 315]
        
        for direction, angle in zip(directions, angles):
            # Heading'e göre pozisyon hesapla
            relative_angle = (angle - heading) % 360
            if relative_angle > 180:
                relative_angle -= 360
            
            # Ekranda göster
            if abs(relative_angle) < 90:
                x_pos = x_center + int(relative_angle * 2)
                
                if 0 < x_pos < self.width:
                    color = self.color_critical if direction == 'N' else self.color_primary
                    cv2.putText(frame, direction, (x_pos-10, y),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Merkez işareti
        cv2.line(frame, (x_center, y-25), (x_center, y-15), 
                self.color_critical, 2)
        
        # Heading değeri
        cv2.putText(frame, f"{heading:.0f}°", (x_center-30, y+40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.color_primary, 2)
        
        return frame
    
    def draw_mission_status(
        self,
        frame: np.ndarray,
        mission_id: str,
        status: str = "ACTIVE"
    ) -> np.ndarray:
        """Görev durumu (alt sol)"""
        
        x = 20
        y = self.height - 60
        
        # Arka plan
        overlay = frame.copy()
        cv2.rectangle(overlay, (x-5, y-25), (x+300, y+15), 
                     self.color_bg, -1)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
        
        # Durum rengi
        status_color = self.color_primary if status == "ACTIVE" else self.color_warning
        
        # Bilgiler
        cv2.putText(frame, f"MISSION: {mission_id}", (x, y-5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1)
        cv2.putText(frame, f"STATUS: {status}", (x, y+15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 2)
        
        return frame
    
    def draw_recording_indicator(self, frame: np.ndarray) -> np.ndarray:
        """Kayıt göstergesi (sağ alt)"""
        
        x = self.width - 100
        y = self.height - 40
        
        # Yanıp sönen kırmızı nokta
        if int(datetime.now().timestamp() * 2) % 2 == 0:
            cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)
            cv2.putText(frame, "REC", (x+15, y+5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return frame
    
    def draw_full_hud(
        self,
        frame: np.ndarray,
        altitude: float = 100.0,
        speed: float = 0.0,
        heading: float = 0.0,
        gps: tuple = None,
        battery: int = 100,
        signal: int = 100,
        target_count: int = 0,
        tracked_count: int = 0,
        frame_num: int = 0,
        total_frames: int = 0,
        mission_id: str = "MISSION_001",
        pitch: float = 0.0
    ) -> np.ndarray:
        """Tam HUD overlay çiz"""
        
        # Tüm HUD elementlerini çiz
        frame = self.draw_corner_brackets(frame)
        frame = self.draw_crosshair(frame)
        frame = self.draw_horizon_line(frame, pitch)
        frame = self.draw_telemetry_panel(frame, altitude, speed, heading, 
                                         gps, battery, signal)
        frame = self.draw_target_info_panel(frame, target_count, tracked_count,
                                           frame_num, total_frames)
        frame = self.draw_altitude_ladder(frame, altitude)
        frame = self.draw_speed_ladder(frame, speed)
        frame = self.draw_compass(frame, heading)
        frame = self.draw_mission_status(frame, mission_id)
        frame = self.draw_recording_indicator(frame)
        
        return frame


# Test
if __name__ == "__main__":
    # Test görüntüsü oluştur
    width, height = 1280, 720
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    # HUD oluştur
    hud = UAV_HUD(width, height)
    
    # HUD çiz
    frame = hud.draw_full_hud(
        frame,
        altitude=150.5,
        speed=12.3,
        heading=45.0,
        gps=(39.9334, 32.8597),
        battery=85,
        signal=95,
        target_count=12,
        tracked_count=8,
        frame_num=150,
        total_frames=1000,
        mission_id="BAYKAR_001"
    )
    
    # Kaydet
    cv2.imwrite('test_hud.jpg', frame)
    print("✅ Test HUD oluşturuldu: test_hud.jpg")
