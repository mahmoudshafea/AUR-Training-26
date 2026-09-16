import cv2
import matplotlib.pyplot as plt

img = cv2.imread("face.jpeg")

avg_blur = cv2.blur(img, (5, 5))
avg_blur = cv2.cvtColor(avg_blur, cv2.COLOR_BGR2GRAY)
avg_blur_edge = cv2.Canny(avg_blur, 50, 150)

med_blur = cv2.medianBlur(img, 5)
med_blur = cv2.cvtColor(med_blur, cv2.COLOR_BGR2GRAY)
med_blur_edge = cv2.Canny(med_blur, 100, 200)

gaussian_blur = cv2.GaussianBlur(img, (5, 5), 0)
gaussian_blur = cv2.cvtColor(gaussian_blur, cv2.COLOR_BGR2GRAY)
gaussian_blur_edge = cv2.Canny(gaussian_blur, 100, 200)


plt.subplot(2, 4, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("ORIGINAL")
plt.axis("off")

plt.subplot(2, 4, 2)
plt.imshow(avg_blur, cmap="gray")
plt.title("AVERAGE BLUR")
plt.axis("off")

plt.subplot(2, 4, 3)
plt.imshow(avg_blur_edge, cmap="gray")
plt.title("AVERAGE BLUR EDGES")
plt.axis("off")

plt.subplot(2, 4, 4)
plt.imshow(med_blur, cmap="gray")
plt.title("MEDIAN BLUR")
plt.axis("off")

plt.subplot(2, 4, 5)
plt.imshow(med_blur_edge, cmap="gray")
plt.title("MEDIAN BLUR EDGES")
plt.axis("off")

plt.subplot(2, 4, 6)
plt.imshow(gaussian_blur, cmap="gray")
plt.title("GAUSSIAN BLUR")
plt.axis("off")

plt.subplot(2, 4, 7)
plt.imshow(gaussian_blur_edge, cmap="gray")
plt.title("GAUSSIAN BLUR EDGES")
plt.axis("off")

plt.tight_layout()
plt.show()