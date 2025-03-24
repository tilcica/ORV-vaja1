import numpy as np
import cv2
import time

subRegionsPerRow = 20
colorCloseness = 0.05
numOfRequiredSkinPixels = 5

def doloci_barvo_koze(slika, spodnjaMeja = np.array([0, 0, 0]), zgornjaMeja = np.array([0, 0, 0])):
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            color = slika[y, x]
            spodnjaMeja[:] = np.clip(color - color * colorCloseness, 0, 255)
            zgornjaMeja[:] = np.clip(color + color * colorCloseness, 0, 255)

    cv2.setMouseCallback("ORV vaja 1", mouse_callback)
    return (spodnjaMeja,zgornjaMeja)

def zmanjsaj_sliko(slika,sirina,visina):
    pomanjsana_slika = cv2.resize(slika, (sirina, visina))
    return cv2.flip(pomanjsana_slika, 1)

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze):
    pass

def prestej_piksle_z_barvo_koze(slika, barva_koze):
    pass

def main():
    cap = cv2.VideoCapture(0)
    window_name = "ORV vaja 1"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    spodnjaMeja = np.array([0, 0, 0])
    zgornjaMeja = np.array([255, 255, 255])
    prev_time = time.time()
    while True:
        success, img = cap.read()

        img = zmanjsaj_sliko(img, 260, 300)
        spodnjaMeja, zgornjaMeja = doloci_barvo_koze(img, spodnjaMeja, zgornjaMeja)

        subBoxes = obdelaj_sliko_s_skatlami(img, 260//subRegionsPerRow, 300//subRegionsPerRow, (spodnjaMeja, zgornjaMeja))
        for i in subBoxes:
            topLeft = i[0]
            bottomRight = i[1]
            numOfSkinPixels = i[2]
            if numOfSkinPixels > numOfRequiredSkinPixels:
                cv2.rectangle(img, topLeft, bottomRight, (0, 255, 0), 1)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(img, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow(window_name, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()