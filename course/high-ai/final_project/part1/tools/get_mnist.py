import requests
import os

TARGET_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../resources/mnist")

def download_unzip():
    links = [
        "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
        "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
        "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
        "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"
    ]
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
    for link in links:
        res = requests.get(link)
        target_path = os.path.join(TARGET_FOLDER, os.path.basename(link))
        print(f"downloading {link}")
        with open(target_path, "wb") as file:
            file.write(res.content)
        if os.system(f"gzip {target_path} -d")!=0:
            print("no gzip! unzip failed.")
    print(f"script {__file__} done.")

if __name__=="__main__":
    download_unzip()