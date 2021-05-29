

# model = torch.load(
#     "gpu_model.pt", map_location=torch.device("cpu")
# )

# torch.save(model, "cpu_model.pt")




import time
import torch
import cv2



# print(torch.cuda.init())

# device = torch.device('cuda')
# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
# model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5s.pt', force_reload=True)

# model.cpu()
model=model.cuda()

# # Image
img = 'https://ultralytics.com/images/zidane.jpg'
results = model(img)
results.show()
framedata=results.pandas().xyxy[0]
print(framedata)
# cap=cv2.VideoCapture(1)
# ret,img=cap.read()
# while ret:
#     # Inference
#     start=time.time()
#     results = model(img)
#     end=time.time()
#     print("time = ",end-start)
#     # print(results)
#     # results.show()
#     cv2.imshow("img",img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#     framedata=results.pandas().xyxy[0]
#     print(framedata)

#     ret,img=cap.read()