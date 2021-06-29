import json
import numpy as np 
from sklearn.svm import SVR
import matplotlib.pyplot as plt 

with open('data.json') as f:
    data = json.load(f)
sd=data["sdviolations"]
noped=data["numberofpedestrians"]

if len(sd)<100:
    print("too little data")
    # exit()
else:
    # print(data["sdviolations"])
    # print(data["numberofpedestrians"])
    # print(data["timestamp"])

    # plt.scatter(sd,noped,color="black",label="org data")
    # plt.xlabel("sd")
    # plt.ylabel("no of ped")
    # plt.title("svm")
    # plt.legend()
    # plt.show()

    sd=np.array(sd).reshape(-1,1)
    noped=np.array(noped).reshape(-1,1)
    noped=noped.ravel()




    print("\n",len(sd)," entries found!\n")
    while True:
        try:
            lastindex=int(input("enter size of data to train on: "))
        except (NameError, ValueError):
            print("invalid format")
            continue
        if lastindex<100:
            print("too small, try again\n")
        elif lastindex>len(sd):
            print("too big, try again\n")
        else:
            break


    # print(len(noped))
    svr_linear=SVR(kernel="linear", C=1e3)
    print("fitting model...")
    # lastindex=-1
    svr_linear.fit(sd[:lastindex],noped[:lastindex])
    print("fitting completed.")

    answer=svr_linear.predict([[0]])
    critical_density=round(answer[0])
    print("critical density = ",critical_density)

    with open('settings.json') as f:
        data = json.load(f)

    data["critical_desity"]=critical_density

    json_object = json.dumps(data,indent=1)

    with open("settings.json", "w") as outfile:
        outfile.write(json_object)

