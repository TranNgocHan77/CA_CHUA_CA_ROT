import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from giao_dien_2 import giao_dien  # Giao diện phụ
from giao_dien import Ui_MainWindow_01  # Giao diện chính
from ultralytics import YOLO  # Nếu bạn sử dụng YOLOv8 từ ultralytics
from tomato import Tomato
from carrot import Carrot



class MainApp(QMainWindow):
    def __init__(self, confidence_threshold=0.55):
        super().__init__()
        # Số lượng cà rốt và cà chua
        self.carrot_count = 0
        self.tomato_count = 0
        
        self.setup_ui()
        self.setup_camera_and_model()

        # Tải mô hình YOLO
        self.model = YOLO(r"C:\Users\TRAN_NGOC_HAN\Desktop\BAO_CAO_XU_LY_ANH\CODE\tomato_carrot_best.pt")
        self.confidence_threshold = confidence_threshold
        
        self.To = Tomato()  # Đối tượng Tomato phải được định nghĩa trong file tomato.py
        self.Ca = Carrot()  # Đối tượng Tomato phải được định nghĩa trong file carrot.py
        self.TOMATO = False



    def setup_ui(self):

    
        """Khởi tạo giao diện chính và giao diện phụ."""
        # Giao diện chính
        self.ui_main = Ui_MainWindow_01()
        self.ui_main.setupUi(self)

        # Giao diện phụ
        self.ui_sub = giao_dien()
        self.sub_window = QMainWindow()  # Cửa sổ phụ
        self.ui_sub.setupUi(self.sub_window)

        # Kết nối nút nhấn
        self.ui_main.pushButton.clicked.connect(self.open_sub_window)
        self.ui_main.pushButton_2.clicked.connect(self.thoat)
        self.ui_sub.thoat.clicked.connect(self.thoat)

        # Video hiển thị trên QLabel
        self.videoLabel_1 = QLabel(self)
        self.ui_sub.video_1.addWidget(self.videoLabel_1)
        
        # Video hiển thị trên QLabel
        self.videoLabel_2 = QLabel(self)
        self.ui_sub.video_2.addWidget(self.videoLabel_2)
        
        # Video hiển thị trên QLabel
        self.videoLabel_3 = QLabel(self)
        self.ui_sub.video_3.addWidget(self.videoLabel_3)

        # Ảnh hiển thị trên QLabel
        self.imageLabel = QLabel(self)
        self.ui_sub.video_5.addWidget(self.imageLabel)
        
        # Video hiển thị trên QLabel
        self.videoLabel_4 = QLabel(self)
        self.ui_sub.video_4.addWidget(self.videoLabel_4)

        # Kết nối các nút chức năng
        self.ui_sub.camera.clicked.connect(self.start_video)

        self.ui_sub.chup_hinh.clicked.connect(self.capture_image)
 
        
        # Kết nối các tín hiệu từ UI tới hàm xử lý tương ứng
        self.ui_sub.ca_chua.clicked.connect(lambda: self.handle_button_click("t"))
        self.ui_sub.ca_rot.clicked.connect(lambda: self.handle_button_click("z"))

        self.ui_sub.tang_tuong_phan.clicked.connect(lambda: self.handle_button_click("w"))
        self.ui_sub.giam_tuong_phan.clicked.connect(lambda: self.handle_button_click("s"))
        self.ui_sub.do_sang_tang.clicked.connect(lambda: self.handle_button_click("d"))
        self.ui_sub.do_sang_giam.clicked.connect(lambda: self.handle_button_click("a"))

        self.ui_sub.do_mo_tang.clicked.connect(lambda: self.handle_button_click("b"))
        self.ui_sub.do_mo_giam.clicked.connect(lambda: self.handle_button_click("n"))
        self.ui_sub.bao_vien.clicked.connect(lambda: self.handle_button_click("v"))

        self.ui_sub.hoi_tu.clicked.connect(lambda: self.handle_button_click("k"))
        self.ui_sub.gian_no.clicked.connect(lambda: self.handle_button_click("h"))
        self.ui_sub.tang_iterations.clicked.connect(lambda: self.handle_button_click("j"))
        self.ui_sub.giam_iterations.clicked.connect(lambda: self.handle_button_click("l"))
        self.ui_sub.Do.clicked.connect(lambda: self.handle_button_click("r"))
        self.ui_sub.Cam.clicked.connect(lambda: self.handle_button_click("o"))
        self.ui_sub.tat_cai_dat.clicked.connect(lambda: self.handle_button_click("c"))
        

        # Hiển thị giao diện chính
        self.show()
        print("Số lượng cà rốt:", self.carrot_count)
        print("Số lượng cà chua:", self.tomato_count)
        

    # Hàm xử lý khi nhấn nút
    def handle_button_click(self, key):
        """Xử lý sự kiện nhấn nút và xuất ra ký tự."""
        # print(f"Ký tự được xuất ra: {key}")
        
        if key == 't':
            self.TOMATO = True  # Sửa từ `==` thành `=`
            print("TOMATO_TRUE")
            print("CARROT_FALSE")
        elif key == 'z':
            self.TOMATO = False
            print("TOMATO_FALSE")
            print("CARROT_TRUE")
                
        elif self.TOMATO:
            if key == 'w':  # Tăng độ tương phản
                self.To.contrast += 0.1
                print(f"Độ tương phản tăng: {self.To.contrast:.1f}")
            elif key == 's':  # Giảm độ tương phản
                self.To.contrast = max(0.1, self.To.contrast - 0.1)
                print(f"Độ tương phản giảm: {self.To.contrast:.1f}")
            elif key == 'd':  # Tăng độ sáng
                self.To.brightness += 10
                print(f"Độ sáng tăng: {self.To.brightness}")
                
            elif key == 'a':  # Giảm độ sáng
                self.To.brightness -= 10
                print(f"Độ sáng giảm: {self.To.brightness}")
            elif key == 'b':  # Tăng mức độ làm mờ
                self.To.blur_level += 1
                print(f"Mức độ làm mờ tăng: {self.To.blur_level}")
            elif key == 'n':  # Giảm mức độ làm mờ
                self.To.blur_level = max(0, self.To.blur_level - 1)
                print(f"Mức độ làm mờ giảm: {self.To.blur_level}")
            elif key == 'r':  # Lọc màu đỏ
                self.To.color_filter = 'red'
                print("Bộ lọc màu đỏ bật.")
            elif key == 'h':
                self.To.morph_action_ = True
                self.To.morph_action = 'dilate'
                print("Chế độ giãn nở bật.")
            elif key == 'k':
                self.To.morph_action_ = True
                self.To.morph_action = 'erode'
                print("Chế độ hội tụ bật.")      
            elif key == 'v':  # Bật/tắt chức năng bao viền
                self.To.draw_contours = not self.To.draw_contours
                status = "bật" if self.To.draw_contours else "tắt"
                print(f"Chế độ bao viền {status}.")          
            elif key == 'c':  # Tắt bộ lọc màu
                self.To.morph_action_ = False
                self.To.color_filter = None
                self.To.morph_action = None
                print("Tắt bộ lọc màu và chế độ giãn nở/hội tụ.")
            if self.To.morph_action_:
                if key == 'j':  # Tăng iterations
                    self.To.iterations += 1
                    print(f"Tăng số lần lặp: {self.To.iterations}")
                elif key == 'l':  # Giảm iterations
                    self.To.iterations = max(1, self.To.iterations - 1)
                    print(f"Giảm số lần lặp: {self.To.iterations}")
                        
        elif not self.TOMATO:
            if key == 'w':  # Tăng độ tương phản
                self.Ca.contrast += 0.1
                print(f"Độ tương phản tăng: {self.Ca.contrast:.1f}")
            elif key == 's':  # Giảm độ tương phản
                self.Ca.contrast = max(0.1, self.Ca.contrast - 0.1)
                print(f"Độ tương phản giảm: {self.Ca.contrast:.1f}")
            elif key == 'd':  # Tăng độ sáng
                self.Ca.brightness += 10
                print(f"Độ sáng tăng: {self.Ca.brightness}")
            elif key == 'a':  # Giảm độ sáng
                self.Ca.brightness -= 10
                print(f"Độ sáng giảm: {self.Ca.brightness}")
            elif key == 'b':  # Tăng mức độ làm mờ
                self.Ca.blur_level += 1
                print(f"Mức độ làm mờ tăng: {self.Ca.blur_level}")
            elif key == 'n':  # Giảm mức độ làm mờ
                self.Ca.blur_level = max(0, self.Ca.blur_level - 1)
                print(f"Mức độ làm mờ giảm: {self.Ca.blur_level}")
            elif key == 'o':  # Lọc màu cam
                self.Ca.color_filter = 'orange'
                print("Bộ lọc màu cam bật.")
            elif key == 'h':
                self.Ca.morph_action_ = True
                self.Ca.morph_action = 'dilate'
                print("Chế độ giãn nở bật.")
            elif key == 'k':
                self.Ca.morph_action_ = True
                self.Ca.morph_action = 'erode'
                print("Chế độ hội tụ bật.")      
            elif key == 'v':  # Bật/tắt chức năng bao viền
                self.Ca.draw_contours = not self.Ca.draw_contours
                status = "bật" if self.Ca.draw_contours else "tắt"
                print(f"Chế độ bao viền {status}.")          
            elif key == 'c':  # Tắt bộ lọc màu
                self.Ca.morph_action_ = False
                self.Ca.color_filter = None
                self.Ca.morph_action = None
                print("Tắt bộ lọc màu và chế độ giãn nở/hội tụ.")
                
            if self.Ca.morph_action_:
                if key == 'j':  # Tăng iterations
                    self.Ca.iterations += 1
                    print(f"Tăng số lần lặp: {self.Ca.iterations}")
                elif key == 'l':  # Giảm iterations
                    self.Ca.iterations = max(1, self.Ca.iterations - 1)
                    print(f"Giảm số lần lặp: {self.Ca.iterations}")


    def setup_camera_and_model(self):
        """Khởi tạo camera và mô hình YOLO."""
        self.ON = "OFF"
        self.cap = None  # Khởi tạo cap là None

    def start_video(self):
        """Bắt đầu hiển thị video từ webcam."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Không thể mở webcam")
            return

        # Khởi tạo một timer để cập nhật video
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Cập nhật frame mỗi 20 ms (50 FPS)

    def update_frame(self):
        """Cập nhật khung hình từ webcam."""
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                try:
                    # Resize frame nếu cần thiết
                    # frame = cv2.resize(frame, (410, 310))
                    
                    # Xử lý frame qua các đối tượng Tomato và Carrot
                    Tomato_frame, Tomato_frame_2, Tomato_frame_3 = self.To.process_frame(frame, frame)  # Đảm bảo có phương thức này
                    Carrot_frame, Carrot_frame_2, Carrot_frame_3 = self.Ca.process_frame(frame, Tomato_frame_3)
                    
                    
                    # Hiển thị frame gốc trên videoLabel_1
                    self.display_frame(Carrot_frame_3, self.videoLabel_1)
                    
                    Tomato_frame = cv2.resize(Tomato_frame, (410, 310))
                    # Hiển thị Tomato_frame_2 trên videoLabel_2
                    self.display_frame(Tomato_frame, self.videoLabel_2)
                    
                    Carrot_frame = cv2.resize(Carrot_frame, (410, 310))
                    # Hiển thị Tomato_frame_2 trên videoLabel_3
                    self.display_frame(Carrot_frame, self.videoLabel_3)
                    
                    frame = cv2.resize(frame, (410, 310))
                    # Hiển thị Tomato_frame_2 trên videoLabel_3
                    self.display_frame(frame, self.videoLabel_4)
                    
                    
                    # Có thể thêm logic hiển thị cho Carrot_frame nếu cần
                    
                except Exception as e:
                    print(f"Lỗi khi xử lý frame: {e}")
            else:
                print("Không thể đọc frame từ webcam")
        else:
            print("Webcam chưa được khởi tạo hoặc không hoạt động")

    def display_frame(self, frame, label):
        """Chuyển đổi và hiển thị khung hình lên QLabel."""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap)


    def detect_objects(self, frame):
        """Dự đoán đối tượng và vẽ bounding box."""
        results = self.model(frame)
        annotated_frame = frame.copy()

        # Biến đếm riêng từng loại
        self.carrot_count = 0
        self.tomato_count = 0

        for result in results:
            boxes = result.boxes  # Lấy các bounding box
            for box in boxes:
                # Chuyển tọa độ bounding box sang kiểu int
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                # Độ tin cậy
                conf = float(box.conf[0])
                # Lớp đối tượng
                cls = int(box.cls[0])
                # Tên lớp
                class_name = self.model.names[cls]

                # Nếu độ tin cậy vượt ngưỡng, vẽ bounding box và đếm số lượng
                if conf >= self.confidence_threshold:
                    if class_name == "carrot":
                        self.carrot_count += 1
                    elif class_name == "tomato":
                        self.tomato_count += 1

                    label = f"{class_name} {conf:.2f}"
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        annotated_frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                    )



        return annotated_frame

    def capture_image(self):
        """Chụp ảnh từ webcam và hiển thị kết quả."""
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite(r'C:\Users\TRAN_NGOC_HAN\Desktop\BAO_CAO_XU_LY_ANH\CODE\captured_image.jpg', frame)
                frame = cv2.resize(frame, (640, 310))
                processed_frame = self.detect_objects(frame)

                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                q_image_adjusted = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap_adjusted = QPixmap.fromImage(q_image_adjusted)
                self.imageLabel.setPixmap(pixmap_adjusted)
                print("Ảnh đã được chụp và hiển thị.")



    def open_sub_window(self):
        """Mở giao diện phụ."""
        self.sub_window.show()

    def thoat(self):
        """Thoát chương trình."""
        if hasattr(self, 'cap') and self.cap is not None and self.cap.isOpened():
            self.cap.release()
        QApplication.quit()

    def closeEvent(self, event):
        """Hàm gọi khi cửa sổ chính đóng."""
        self.thoat()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())
