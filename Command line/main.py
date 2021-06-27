import requests
from bs4 import BeautifulSoup

header = {
            "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
}

def insta_download():
    img_count = 0

    while True :
        img_count+=1

        url = input("Enter instagram image url (no private post) : ")

        response = requests.get(url, headers= header)

        if response.ok == False:
            print("Server error! Please try again !")
            continue

        soup = BeautifulSoup(response.text,'html.parser')
        img_url = None


        for tag in soup.find_all("meta",property="og:image"):
            if tag.get("property",None) == 'og:image':
                img_url = tag.get('content',None)

        if img_url == None:
            print("Image is not obtained")
            continue

        try:
            img_response = requests.get(img_url, headers=header)

            with open(f"img{img_count}.jpg","wb") as f:
                f.write(img_response.content)

            print(f"Your image (img{img_count}) is downloaded successfully ! ")

        except Exception as e:
            print(e)
            print("image download failed !")

        choice = input("Continue (Y/N) : ")
        if choice == 'N':
            break

def main():
    insta_download()


if __name__ == '__main__':
    main()
