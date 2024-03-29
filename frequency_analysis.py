import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def read_img(img_path):
    # 简单高通滤波：中值滤波 - 原图像
    img = cv2.imread(img_path, 0)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # plt.imshow(img)
    # plt.show()
    blurred_img = cv2.medianBlur(img, 5)
    # plt.imshow(blurred_img.astype(np.int32))
    # plt.show()
    img = blurred_img - img
    # plt.imshow(img.astype(np.int32))
    # plt.show()

    # 傅里叶变换
    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    dftshift = np.fft.fftshift(dft)
    magnitude = cv2.magnitude(dftshift[:, :, 0], dftshift[:, :, 1])
    amplitude = 20 * np.log(magnitude)

    # # 巴特沃斯高通滤波
    # w = np.shape(amplitude)[0]
    # h = np.shape(amplitude)[1]
    # w_center = np.floor(w / 2)
    # h_center = np.floor(h / 2)
    # n = 2
    # d0 = 30
    # hpf_result = np.empty((w, h), dtype=np.float32)
    # for i in range(w):
    #     for j in range(h):
    #         d = np.sqrt((i - w_center) ** 2 + (j - h_center) ** 2)
    #         H = 1 / (1 + (d0 / d) ** (2 * n))
    #         hpf_result[i, j] = H * amplitude[i, j]

    # normalization = (hpf_result - np.min(hpf_result)) / (np.max(hpf_result) - np.min(hpf_result))
    # plt.subplot(121), plt.imshow(img, cmap='gray')
    # plt.title('original'), plt.axis('off')
    # plt.subplot(122), plt.imshow(amplitude, cmap='gray')
    # plt.title('dft'), plt.axis('off')
    # plt.show()
    return amplitude


if __name__ == '__main__':
    # fake_img_path = r'.\images\1_fake\n02381460_1000_fake.png'
    # real_img_path = r'.\images\0_real\n02381460_1000_real.png'
    # f_array = [read_img(fake_img_path)]
    # r_array = [read_img(real_img_path)]

    fake_path = os.walk(r".\images\1_fake")
    real_path = os.walk(r".\images\0_real")
    f_array = []
    r_array = []
    for path, dir_list, file_list in fake_path:
        for file_name in file_list:
            file_path = os.path.join(path, file_name)
            print(file_path)
            f_array.append(read_img(file_path))
    for path, dir_list, file_list in real_path:
        for file_name in file_list:
            file_path = os.path.join(path, file_name)
            print(file_path)
            r_array.append(read_img(file_path))

    f_ave = np.mean(np.array(f_array), axis=0)
    r_ave = np.mean(np.array(r_array), axis=0)
    im_color_f = cv2.applyColorMap(f_ave.astype(np.uint8), cv2.COLORMAP_JET)
    im_color_r = cv2.applyColorMap(r_ave.astype(np.uint8), cv2.COLORMAP_JET)
    plt.subplot(121), plt.imshow(im_color_r, cmap='gray')
    plt.title('real'), plt.axis('off')
    plt.subplot(122), plt.imshow(im_color_f, cmap='gray')
    plt.title('fake'), plt.axis('off')
    plt.show()
