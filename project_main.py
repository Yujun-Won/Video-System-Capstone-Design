from tkinter import ttk, Tk, Canvas, filedialog, FLAT
from PIL import ImageTk, Image
import cv2
import numpy as np

class ImageMaker:
    def __init__(self, window):
        self.window = window
        self.activation()
        
    def activation(self):
        self.window.title("Final_Project: Photo Effect Editor")
        self.window.geometry("750x450+300+300")
        
        # 메인 프레임
        self.frame_menu = ttk.Frame(self.window, width=780, height=440)
        self.frame_menu.pack()
        self.frame_menu.config(relief=FLAT, padding=(50, 20))
        
        # 이미지를 띄우는 캔버스
        self.canvas = Canvas(self.frame_menu, bg="gray", width=400, height=400)
        self.canvas.grid(row=0, column=5, rowspan=10)

        ttk.Label(self.frame_menu, text="Photo Effect", font=('Helvetica', 17)).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=7, text="Binary", command=self.binary_action).grid(
            row=1, column=0, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=7, text="Grayscale", command=self.grayscale_action).grid(
            row=2, column=0, padx=5, pady=5)
        ttk.Label(self.frame_menu, text="").grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=7, text="Sketch", command=self.sketch_action).grid(
            row=4, column=0, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=7, text="Cartoon", command=self.cartoon_action).grid(
            row=5, column=0, padx=5, pady=5)
        ttk.Label(self.frame_menu, text="").grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=7, text="Pop Art 1", command=self.popart1_action).grid(
            row=7, column=0, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=7, text="Pop Art 2", command=self.popart2_action).grid(
            row=8, column=0, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=7, text="Pop Art 3", command=self.popart3_action).grid(
            row=9, column=0, padx=5, pady=5)
        
        # 회전
        ttk.Label(self.frame_menu, text="Rotation", font=('Helvetica', 17)).grid(row=0, column=10, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=10, text="Rotate Left", command=self.rotate_left_action).grid(
            row=1, column=10, padx=5, pady=3)
        ttk.Button(self.frame_menu, width=10, text="Rotate Right", command=self.rotate_right_action).grid(
            row=2, column=10, padx=5, pady=3)

        # 반전
        ttk.Label(self.frame_menu, text="Flip", font=('Helvetica', 17)).grid(row=3, column=10, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=10, text="Vertical Flip", command=self.vertical_action).grid(
            row=4, column=10, padx=5, pady=3)
        ttk.Button(self.frame_menu, width=10, text="Horizontal Flip", command=self.horizontal_action).grid(
            row=5, column=10, padx=5, pady=3)

        # 이미지 불러오기, 저장, 초기화
        ttk.Label(self.frame_menu, text="------MENU------", font=('Helvetica', 17)).grid(row=6, column=10, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=10, text="Image Load", command=self.upload_action).grid(
            row=7, column=10, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=10, text="Save", command=self.save_action).grid(
            row=8, column=10, padx=5, pady=5)
        ttk.Button(self.frame_menu, width=10, text="Reset", command=self.reset_action).grid(
            row=9, column=10, padx=5, pady=5)

    """ Photo Effect Function """
    def binary_action(self):
        # <흑백 효과 - Binary>
        # Threshold를 127로 설정하여 Binary Image로 변환
        img = self.edited_image
        H, W, C = img.shape
        gray_img = img.copy()

        for i in range(H):
            for j in range(W):
                grayscale = (img.item(i,j,0) + img.item(i,j,1) + img.item(i,j,2)) / 3
                gray_img[i, j] = round(grayscale)

        binary = np.where(gray_img > 127, 255, 0).astype(np.uint8)
        self.filtered_image = binary
        self.display_image(self.filtered_image)

    def grayscale_action(self):
        # <흑백 효과>
        # 입력한 이미지를 grayscale로 변환
        # gray_img = cv2.cvtColor(self.edited_image, cv2.COLOR_BGR2GRAY)
        img = self.edited_image
        H, W, C = img.shape
        gray_img = img.copy()

        for i in range(H):
            for j in range(W):
                grayscale = (img.item(i,j,0) + img.item(i,j,1) + img.item(i,j,2)) / 3
                gray_img[i, j] = round(grayscale)
        self.filtered_image = gray_img
        self.display_image(self.filtered_image)

    # <스케치 효과>
    # 입력한 이미지를 grayscale로 변환 -> GLPF를 통해 Smoothing -> 둘을 나눔  
    def sketch_action(self):
        gray_img = cv2.cvtColor(self.edited_image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray_img, (21, 21), sigmaX=0)
        self.filtered_image = cv2.divide(gray_img, blur, scale=256)
        self.display_image(self.filtered_image)

    # <카툰 효과>
    # 입력한 이미지를 grayscale로 변환 -> GLPF를 통해 Smoothing -> Laplacian을 사용하여 Edge Detection -> Thresholding한 이미지를 반전
    # -> Erosion을 이용하여 Edge를 강조한 후, Median Filter를 사용하여 Blur
    # -> 입력한 컬러 이미지도 GLPF로 Smoothing -> 컬러 이미지와 grayscale 이미지를 합성  
    def cartoon_action(self):

        img = self.edited_image
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.GaussianBlur(img_gray, (11, 11), 0)
        edges = cv2.Laplacian(img_gray, -1, None, 5)
        _, sketch = cv2.threshold(edges, 90, 255, cv2.THRESH_BINARY_INV)

        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
        sketch = cv2.erode(sketch, kernel)
        sketch = cv2.medianBlur(sketch, 3)
        img_sketch = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

        img_paint = cv2.GaussianBlur(img, (5, 5), sigmaX=0)
        self.filtered_image = cv2.bitwise_and(img_paint, img_sketch, mask=sketch)
        self.display_image(self.filtered_image)

    # <팝아트 효과>
    def popart1_action(self):
        palette = [             # (B, G, R)
            (0, 0, 0),          # 블랙
            (164, 46, 105),     # 진한 보라
            (13, 100, 210),     # 짙은 오렌지
            (50, 170, 240),     # 연한 오렌지
            (164, 227, 255),    # 베이지
            (242, 250, 253)     # 화이트
        ]
        img = self.edited_image
        H, W, C = img.shape
        output = img.copy()

        # Grayscale로 변환
        for i in range(H):
            for j in range(W):
                grayscale = (img.item(i,j,0) + img.item(i,j,1) + img.item(i,j,2)) / 3
                output[i, j] = round(grayscale)

        # Histogram Equalization
        histogram, bin = np.histogram(output.ravel(), 256, [0, 256])
        cdf = np.cumsum(histogram)
        cdf = (cdf - cdf.min()) * 255 / ((H * W) - cdf.min())
        cdf = cdf.astype(np.uint8)
        equalized_img = cdf[output]
        output = equalized_img

        # Threshold를 이용하여 Slicing
        threshold_1 = 255 * (1/6)
        threshold_2 = 255 * (2/6)
        threshold_3 = 255 * (3/6)
        threshold_4 = 255 * (4/6)
        threshold_5 = 255 * (5/6)
        for i in range(H):
            for j in range(W):
                if img.item(i, j, 0) < threshold_1:
                    output[i, j] = 0
                elif img.item(i, j, 0) < threshold_2:
                    output[i, j] = 1
                elif img.item(i, j, 0) < threshold_3:
                    output[i, j] = 2
                elif img.item(i, j, 0) < threshold_4:
                    output[i, j] = 3
                elif img.item(i, j, 0) < threshold_5:
                    output[i, j] = 4
                else :
                    output[i, j] = 5
        imgs = output.astype(np.uint8)

        # 결과에 GLPF를 취해 Smoothing & palette의 이미지에 할당
        imgs = cv2.GaussianBlur(imgs, (5, 5), sigmaX=0)
        for i in range(H):
            for j in range(W):
                output[i, j] = palette[imgs.item(i, j, 0)]
        self.filtered_image = output
        self.display_image(self.filtered_image)

    def popart2_action(self):
        palette = [
            (148, 58, 108),     # 짙은 퍼플
            (58, 19, 189),      # 밝은 버건디
            (233, 151, 35),     # 어두운 하늘
            (60, 200, 255),     # 노랑
            (141, 243, 197),    # 메로나
            (208, 246, 250)     # 밝은 베이지
        ]
        img = self.edited_image
        H, W, C = img.shape
        output = img.copy()

        # Grayscale로 변환
        for i in range(H):
            for j in range(W):
                grayscale = (img.item(i,j,0) + img.item(i,j,1) + img.item(i,j,2)) / 3
                output[i, j] = round(grayscale)

        # Histogram Equalization
        histogram, bin = np.histogram(output.ravel(), 256, [0, 256])
        cdf = np.cumsum(histogram)
        cdf = (cdf - cdf.min()) * 255 / ((H * W) - cdf.min())
        cdf = cdf.astype(np.uint8)
        equalized_img = cdf[output]
        output = equalized_img

        # Threshold를 이용하여 Slicing
        threshold_1 = 255 * (1/6)
        threshold_2 = 255 * (2/6)
        threshold_3 = 255 * (3/6)
        threshold_4 = 255 * (4/6)
        threshold_5 = 255 * (5/6)
        for i in range(H):
            for j in range(W):
                if img.item(i, j, 0) < threshold_1:
                    output[i, j] = 0
                elif img.item(i, j, 0) < threshold_2:
                    output[i, j] = 1
                elif img.item(i, j, 0) < threshold_3:
                    output[i, j] = 2
                elif img.item(i, j, 0) < threshold_4:
                    output[i, j] = 3
                elif img.item(i, j, 0) < threshold_5:
                    output[i, j] = 4
                else :
                    output[i, j] = 5
        imgs = output.astype(np.uint8)

        # 결과에 GLPF를 취해 Smoothing & palette의 이미지에 할당
        imgs = cv2.GaussianBlur(imgs, (5, 5), sigmaX=0)
        for i in range(H):
            for j in range(W):
                output[i, j] = palette[imgs.item(i, j, 0)]
        self.filtered_image = output
        self.display_image(self.filtered_image)

    def popart3_action(self):
        palette = [
            (148, 58, 108),     # 보라
            (255, 204, 229),    # 연보라
            (25, 238, 174),     # 연두
            (0, 255, 247),      # 노랑
            (204, 255, 255),    # 연한 노랑
            (255, 255, 51)      # 코랄
        ]
        img = self.edited_image
        H, W, C = img.shape
        output = img.copy()

        # Grayscale로 변환
        for i in range(H):
            for j in range(W):
                grayscale = (img.item(i,j,0) + img.item(i,j,1) + img.item(i,j,2)) / 3
                output[i, j] = round(grayscale)

        # Histogram Equalization
        histogram, bin = np.histogram(output.ravel(), 256, [0, 256])
        cdf = np.cumsum(histogram)
        cdf = (cdf - cdf.min()) * 255 / ((H * W) - cdf.min())
        cdf = cdf.astype(np.uint8)
        equalized_img = cdf[output]
        output = equalized_img

        # Threshold를 이용하여 Slicing
        threshold_1 = 255 * (1/6)
        threshold_2 = 255 * (2/6)
        threshold_3 = 255 * (3/6)
        threshold_4 = 255 * (4/6)
        threshold_5 = 255 * (5/6)
        for i in range(H):
            for j in range(W):
                if img.item(i, j, 0) < threshold_1:
                    output[i, j] = 0
                elif img.item(i, j, 0) < threshold_2:
                    output[i, j] = 1
                elif img.item(i, j, 0) < threshold_3:
                    output[i, j] = 2
                elif img.item(i, j, 0) < threshold_4:
                    output[i, j] = 3
                elif img.item(i, j, 0) < threshold_5:
                    output[i, j] = 4
                else :
                    output[i, j] = 5
        imgs = output.astype(np.uint8)

        # 결과에 GLPF를 취해 Smoothing & palette의 이미지에 할당
        imgs = cv2.GaussianBlur(imgs, (5, 5), sigmaX=0)
        for i in range(H):
            for j in range(W):
                output[i, j] = palette[imgs.item(i, j, 0)]
        self.filtered_image = output
        self.display_image(self.filtered_image)

    """ 우측 버튼의 함수 """
    def rotate_left_action(self):
        self.filtered_image = cv2.rotate(self.filtered_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.display_image(self.filtered_image)

    def rotate_right_action(self):
        self.filtered_image = cv2.rotate(self.filtered_image, cv2.ROTATE_90_CLOCKWISE)
        self.display_image(self.filtered_image)

    def vertical_action(self):
        self.filtered_image = cv2.flip(self.filtered_image, 0)
        self.display_image(self.filtered_image)

    def horizontal_action(self):
        self.filtered_image = cv2.flip(self.filtered_image, 2)
        self.display_image(self.filtered_image)

    # 이미지 불러오기
    def upload_action(self):
        self.canvas.delete("all")
        self.filename = filedialog.askopenfilename()
        self.original_image = cv2.imread(self.filename) # 원본 이미지
        self.edited_image = cv2.imread(self.filename)
        self.filtered_image = cv2.imread(self.filename)
        self.display_image(self.original_image)
    
    # 이미지 저장하기
    def save_action(self):
        original_file_type = self.filename.split('.')[-1]   # 기존 파일명의 확장자
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type

        save_as_image = self.filtered_image
        cv2.imwrite(filename, save_as_image)
        self.filename = filename
    
    # 이미지 초기화
    def reset_action(self):
        self.filtered_image = self.original_image.copy()
        self.display_image(self.filtered_image)

    # 캔버스에 이미지를 띄우는 함수
    def display_image(self, image=None):
        self.canvas.delete("all")
        if image is None:
            image = self.edited_image.copy()
        else:
            image = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        H, W, C = image.shape
        ratio = H / W

        nH = H
        nW = W

        if H > 400 or W > 300:
            if ratio < 1:
                nW = 300
                nH = int(nW * ratio)
            else:
                nH = 400
                nW = int(nH * (W / H))

        self.ratio = H / nH
        self.new_image = cv2.resize(image, (nW, nH))
        self.new_image = ImageTk.PhotoImage(Image.fromarray(self.new_image))

        self.canvas.config(width=nW, height=nH)
        self.canvas.create_image(nW/2, nH/2,  image=self.new_image)

if __name__ == "__main__":
    mainWindow = Tk()
    ImageMaker(mainWindow)
    mainWindow.mainloop()
