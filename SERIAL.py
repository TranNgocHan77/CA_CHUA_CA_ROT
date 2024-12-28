import serial
import time

# Cấu hình cổng UART
PORT = "COM7"  # Thay COM3 bằng cổng kết nối Arduino của bạn (Linux: '/dev/ttyUSB0')
BAUD_RATE = 9600  # Tốc độ baud phải khớp với Arduino

# Kết nối với Arduino
try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"Đã kết nối với {PORT}")
    time.sleep(2)  # Chờ Arduino khởi động
except Exception as e:
    print(f"Lỗi khi kết nối với Arduino: {e}")
    exit()

# Hàm gửi dữ liệu
def send_data(tomato_count, carrot_count):
    # Tạo chuỗi dữ liệu theo định dạng: "T:<số lượng>,C:<số lượng>"
    data = f"T:{tomato_count},C:{carrot_count}\n"
    ser.write(data.encode())  # Gửi dữ liệu đến Arduino qua UART
    print(f"Đã gửi: {data.strip()}")

# Dữ liệu mẫu
tomato_count = 10
carrot_count = 5

try:
    while True:
        # # Cập nhật giá trị Tomato và Carrot (có thể thay đổi tùy ý)
        # tomato_count += 1
        # carrot_count += 2

        # Gửi dữ liệu
        send_data(tomato_count, carrot_count)

        # Đợi 2 giây trước khi gửi dữ liệu tiếp
        time.sleep(1)

except KeyboardInterrupt:
    print("Dừng chương trình...")
    ser.close()
