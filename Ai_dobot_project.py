import numpy as np
import cv2
import cv2.aruco as aruco
import os
import re
marker_size = 0.025
qwe=0
camera_matrix = np.load("calibration_matrix.npy")
dist_coeffs = np.load("distortion_coefficients.npy")
# ArUco 마커 ID와 상품 정보 매칭 딕셔너리
aruco2product = {
    0: "Snacks",
    21: "Ramen",
    2: "Malatang",
    3: "Sundae Soup",
    4: "Mara Rose Steamed Chicken",
    5: "Pho",
    6: "bread",
    7: "robot",
    8: "dubai chocolate",
    9: "car"
}

aruco2price = {
    0: "2,000 won",
    21: "800 won",
    2: "10,000 won",
    3: "10,000 won",
    4: "24,800 won",
    5: "10,000 won",
    6: "1,500 won",
    7: "5,000,000 won",
    8: "4,000 won",
    9: "30,000,000,000 won",
}

aruco2weight = {
    0: "0.125kg",
    21: "0.065kg",
    2: "0.500kg",
    3: "0.400kg",
    4: "0.600kg",
    5: "0.300kg",
    6: "0.060kg",
    7: "8.000kg",
    8: "0.050kg",
    9: "2000kg"
}

aruco2date = {
    0: "2025-08-01",
    21: "2026-08-31",
    2: "2024-09-01",
    3: "2024-08-30",
    4: "2024-08-29",
    5: "2024-08-28",
    6: "2024-08-23",
    7: "2025-09-01",
    8: "2025-07-01",
    9: "2034-08-01"
}

aruco2img = {
    0: "image00.png",
    21: "image01.png",
    2: "image02.png",
    3: "image03.png",
    4: "image04.png",
    5: "image05.png",
    6: "image06.png",
    7: "image07.png",
    8: "image08.png",
    9: "image09.png"
}

# 카메라 초기화
cap = cv2.VideoCapture(1)

# ArUco 딕셔너리와 파라미터 설정
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
parameters = aruco.DetectorParameters_create()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # ArUco 마커 검출
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, dist_coeffs)
        for i in range(len(ids)):
            id = ids[i][0]
            rvec_str = np.array2string(rvecs[i][0], precision=2, separator=',')
            tvec_str = np.array2string(tvecs[i][0], precision=2, separator=',')
            if id in aruco2product:
                # ArUco 마커 주변에 사각형 그리기
                aruco.drawDetectedMarkers(frame, corners)
            if (tvec_str[7] == '-'): # 좌표값 -
                s = re.findall(r'\d+', tvec_str)
                s = s[3]
                s = float(s)
                s/=100.0
                #run_point(move, [270-s*912, 5, 5, 115])
                s=265-s*912
                
            elif (tvec_str[7] == '.'or ' '): #좌표값 +
                s = re.findall(r'\d+', tvec_str)
                s = s[3]
                s = float(s)
                s/=100.0
                #run_point(move, [270+s*912, 5, 5, 115])
                s=265+s*912
            

            if (tvec_str[1] == '-'): #좌표값 -
                n = re.findall(r'\d+', tvec_str)
                n = n[1]
                if n =='1':
                    n=float(n)
                    n*=10.0
                n=float(n)
                n/=100.0*-1
                #run_point(move, [245, n*954+40, 5, 115])
                n=n*954+40
                
            elif (tvec_str[1] == '0'or' '): #좌표값 +
                n = re.findall(r'\d+', tvec_str)
                n = n[1]
                if n =='1':
                    n=float(n)
                    n*=10.0
                n=float(n)
                n/=100.0
                #run_point(move, [245, n*954+40, 5, 115])
                n=n*954+40
                
            #run_point(move, [s, n, -40, 115])
            
            
            
            if qwe==ids[i][0]:
                run_point(move, [s, n, -10, 115])
                
                sleep(0.5)
                run_point(move, [s, n, -56, 115])
                gripper_DO(dashboard, gripper_port, 1)
                run_point(move, [s, n, -10, 115])
                run_point(move, [290, 260, -10, 115])
                run_point(move, [290, 260, -55, 115])
                gripper_DO(dashboard, gripper_port, 0)
                run_point(move, [290, 260, -10, 115])
                qwe+=1
            s=0
            n=0
            qwe+=1
            if qwe==30:
                qwe=0                
                # 상품 정보 표시
            product_name = aruco2product[id]
            price = aruco2price[id]
            weight = aruco2weight[id]
            expiry_date = aruco2date[id]
            img_path = aruco2img[id]

                # 상품 이미지 읽기
            product_img = cv2.imread(img_path)
            if product_img is not None:
                product_img = cv2.resize(product_img, (200, 200))
                frame[0:200, 0:200] = product_img

                # 텍스트 표시
            cv2.putText(frame, f"Name: {product_name}", (10, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Price: {price}", (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Weight: {weight}", (10, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Expiry: {expiry_date}", (10, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # 화면에 결과 보여주기
    cv2.imshow('ArUco Marker', frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 카메라 및 윈도우 종료
cap.release()
cv2.destroyAllWindows()