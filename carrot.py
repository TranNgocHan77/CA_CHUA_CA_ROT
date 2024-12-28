
import cv2
import numpy as np

class Carrot:
    def __init__(self):

        self.contrast = 1.0  # Độ tương phản ban đầu
        self.brightness = 0  # Độ sáng ban đầu
        self.blur_level = 0  # Mức độ làm mờ ban đầu (0 là không làm mờ)
        self.color_filter = None  # Bộ lọc màu hiện tại (None: không lọc)
        self.morph_action = None 
        self.draw_contours = False
        self.width = 640     # Chiều rộng mặc định
        self.height = 480    # Chiều cao mặc định   
        self.frame_02 = None 
        self.frame_03 = None  
        self.gray = None 
        self.iterations = 1       # Số lần lặp mặc định
        self.morph_action_ = False
        self.So_luong_carrot = 0

    def resize_frame(self, frame):
        """
        Thay đổi kích thước khung hình.
        :param frame: Khung hình đầu vào.
        :return: Khung hình đã được thay đổi kích thước.
        """
        return cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_LINEAR)

    def adjust_contrast_brightness(self, frame):
        """
        Điều chỉnh độ tương phản và độ sáng của khung hình.
        :param frame: Khung hình đầu vào.
        :return: Khung hình sau khi điều chỉnh.
        """
        return cv2.convertScaleAbs(frame, alpha=self.contrast, beta=self.brightness)

    def apply_blur(self, frame):
        """
        Áp dụng làm mờ khung hình.
        :param frame: Khung hình đầu vào.
        :return: Khung hình sau khi làm mờ.
        """
        if self.blur_level > 0:
            ksize = max(1, self.blur_level * 2 + 1)  # Kernel size phải là số lẻ
            return cv2.GaussianBlur(frame, (ksize, ksize), 0)
        return frame

    def apply_morph(self, frame):
        # """Áp dụng giãn nở hoặc hội tụ lên khung hình RGB."""
        # kernel = np.ones((5, 5), np.uint8)  # Kernel 5x5
        # if self.morph_action == 'dilate':
        #     return cv2.dilate(frame, kernel, iterations=10)
        # elif self.morph_action == 'erode':
        #     return cv2.erode(frame, kernel, iterations=10)
        # return frame
        
        """
        Áp dụng giãn nở hoặc hội tụ lên khung hình RGB.
        :param frame: Khung hình đầu vào.
        :return: Khung hình đã áp dụng giãn nở hoặc hội tụ.
        """
        kernel = np.ones((5, 5), np.uint8)  # Kernel 5x5
        if self.morph_action == 'dilate':
            return cv2.dilate(frame, kernel, iterations=self.iterations)
        elif self.morph_action == 'erode':
            return cv2.erode(frame, kernel, iterations=self.iterations)

    def extract_color(self, frame, color):
        """
        Tách ngưỡng màu từ khung hình.
        :param frame: Khung hình đầu vào.
        :param color: Màu cần tách (red, orange, yellow).
        :return: Khung hình chỉ giữ lại màu được chọn.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Định nghĩa phạm vi màu HSV
        if color == 'orange':
            lower = np.array([10, 50, 50])
            upper = np.array([25, 255, 255])
            mask = cv2.inRange(hsv, lower, upper)

        else:
            return frame  # Không lọc nếu màu không hợp lệ

        # Áp dụng mặt nạ lên khung hình gốc
        filtered_frame =  cv2.bitwise_and(frame, frame, mask=mask)
        
        # # Chuyển vùng nền từ đen sang trắng
        # white_background = frame.copy()
        # white_background[:] = (255, 255, 255)  # Đặt toàn bộ nền là màu trắng
        # inv_mask = cv2.bitwise_not(mask)       # Mặt nạ ngược để lấy vùng nền
        # background_with_white = cv2.bitwise_and(white_background, white_background, mask=inv_mask)

        # # Kết hợp phần lọc màu với nền trắng
        # final_frame = cv2.add(filtered_frame, background_with_white)
        
        return filtered_frame


    def draw_contours_on_frame(self, frame):
        """
        Tìm và vẽ các đường viền trên khung hình.
        :param frame: Khung hình đầu vào.
        :return: Khung hình với các đường viền đã được vẽ.
        """
        self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.morph_action_ == True:
            self.gray = self.apply_morph(self.gray)
    
        # Áp dụng bộ lọc Canny để tìm viền
        edges = cv2.Canny(self.gray, threshold1=100, threshold2=200)

        # Tìm các vùng bao quanh (bounding boxes) của các đối tượng màu đen trong ảnh Canny
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Vẽ các hộp bao quanh và các điểm trung tâm
        output_image = self.frame_03
        center_points = []  # Danh sách lưu trữ các điểm trung tâm
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)  # Tính toán hộp bao quanh
            area = w * h  # Diện tích của đối tượng

            if area > 30:  # Lọc theo diện tích
            
                # Vẽ hộp bao quanh (màu xanh lá)
                cv2.rectangle(output_image, (x, y), (x + w, y + h), (128,0,128), 2)
                
                # Tính toán điểm trung tâm
                center_x = x + w // 2
                center_y = y + h // 2
                
                # Vẽ điểm trung tâm (màu đỏ)
                cv2.circle(output_image, (center_x, center_y), 5, (128,0,128), -1)
                
                # Hiển thị số thứ tự điểm trung tâm
                cv2.putText(output_image, str(i + 1), (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                cv2.putText(output_image, "CARROT", (x, y + h + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (128,0,128), 1)
                
                # Thêm điểm trung tâm vào danh sách
                center_points.append((center_x, center_y))
                
        self.So_luong_carrot = len(center_points)  # Ghi lại số lượng tomato


    def process_frame(self, frame, frame_03):
        """
        Xử lý khung hình với các hiệu ứng như điều chỉnh độ tương phản, độ sáng, làm mờ và tách màu.
        :param frame: Khung hình đầu vào.
        :return: Khung hình sau khi xử lý.
        """
        
        # Thay đổi kích thước khung hình
        frame = self.resize_frame(frame) 
        self.frame_02 = frame.copy()  
        # self.frame_03 = frame_03
        self.frame_03 = self.resize_frame(frame_03) 
        
        frame = self.adjust_contrast_brightness(frame)
        frame = self.apply_blur(frame)
        # frame = self.apply_morph(frame)
        if self.color_filter:
            frame = self.extract_color(frame, self.color_filter)
        if self.color_filter:
            frame = self.extract_color(frame, self.color_filter)
            
        if self.draw_contours:
            self.draw_contours_on_frame(frame)    

        return frame, self.frame_02, self.frame_03

    def read_and_display(self,frame):
        """
        Đọc và hiển thị video trong cửa sổ OpenCV.
        :param window_name: Tên cửa sổ hiển thị.
        :param exit_key: Phím để thoát chương trình.
        :param delay: Thời gian chờ giữa các khung hình (ms).
        """
        print(f"Đang phát video từ nguồn: {self.source}")
        print("Nhấn 'w' để tăng độ tương phản, 's' để giảm độ tương phản.")
        print("Nhấn 'd' để tăng độ sáng, 'a' để giảm độ sáng.")
        print("Nhấn 'b' để tăng mức độ làm mờ, 'n' để giảm mức độ làm mờ.")
        print("Nhấn 'r' để lọc màu đỏ, 'o' để lọc màu cam, 'y' để lọc màu vàng.")
        print("Nhấn 'c' để tắt bộ lọc màu.")

        while True:
            
            # Thay đổi kích thước khung hình
            resized_frame = self.resize_frame(frame) 
            
            self.frame_02 = resized_frame.copy()  
            self.frame_03 = resized_frame.copy()
            
            # Xử lý khung hình
            processed_frame = self.process_frame(resized_frame)

            # Hiển thị khung hình đã xử lý
            cv2.imshow("window_name", processed_frame)
            
            # Hien thi khung anh coppy
            cv2.imshow("Frame", self.frame_02)
            
            # Hien thi khung anh coppy
            cv2.imshow("Frame_03", self.frame_03)
            
            # Gray
            if self.draw_contours == True:
                cv2.imshow("xam", self.gray)

            # Kiểm tra phím nhấn
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Đã thoát.")
                break
            elif key == ord('w'):  # Tăng độ tương phản
                self.contrast += 0.1
                print(f"Độ tương phản tăng: {self.contrast:.1f}")
            elif key == ord('s'):  # Giảm độ tương phản
                self.contrast = max(0.1, self.contrast - 0.1)
                print(f"Độ tương phản giảm: {self.contrast:.1f}")
            elif key == ord('d'):  # Tăng độ sáng
                self.brightness += 10
                print(f"Độ sáng tăng: {self.brightness}")
            elif key == ord('a'):  # Giảm độ sáng
                self.brightness -= 10
                print(f"Độ sáng giảm: {self.brightness}")
            elif key == ord('b'):  # Tăng mức độ làm mờ
                self.blur_level += 1
                print(f"Mức độ làm mờ tăng: {self.blur_level}")
            elif key == ord('n'):  # Giảm mức độ làm mờ
                self.blur_level = max(0, self.blur_level - 1)
                print(f"Mức độ làm mờ giảm: {self.blur_level}")
            elif key == ord('o'):  # Lọc màu cam
                self.color_filter = 'orange'
                print("Bộ lọc màu cam bật.")

            elif key == ord('h'):
                self.morph_action_ = True
                self.morph_action = 'dilate'
                print("Chế độ giãn nở bật.")
            elif key == ord('k'):
                self.morph_action_ = True
                self.morph_action = 'erode'
                print("Chế độ hội tụ bật.")      
            elif key == ord('v'):  # Bật/tắt chức năng bao viền
                self.draw_contours = not self.draw_contours
                status = "bật" if self.draw_contours else "tắt"
                print(f"Chế độ bao viền {status}.")          
            elif key == ord('c'):  # Tắt bộ lọc màu
                self.morph_action_ = False
                self.color_filter = None
                print("Bộ lọc màu tắt.")
                self.morph_action = None
                print("Tắt chế độ giãn nở/hội tụ.")
                
            if self.morph_action_ == True:
                if key == ord('j'):  # Tăng iterations
                    self.iterations += 1
                    print(f"Tăng số lần lặp: {self.iterations}")
                elif key == ord('l'):  # Giảm iterations
                    self.iterations = max(1, self.iterations - 1)  # Giữ iterations >= 1
                    print(f"Giảm số lần lặp: {self.iterations}")                


        self.cleanup()

    def cleanup(self):
        """Giải phóng tài nguyên và đóng cửa sổ."""
        self.cap.release()
        cv2.destroyAllWindows()
        print("Đã giải phóng tài nguyên.")


