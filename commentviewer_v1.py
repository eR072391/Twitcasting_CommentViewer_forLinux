import tkinter as tk
import requests
from playsound import playsound
import os #読み上げよう音声ファイル削除用
import json
# sudo apt install unifont 絵文字表示用
# sudo apt install python3-tk
# pip3 install playsound


class Model:    #アプリケーションのデータを扱う。アプリケーションのデータを保存し、それを更新するためのロジックを定義する。
    def __init__(self):
        self.username = None
        self.movie_id = None
        self.name = None
        self.ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjFhZDM2YzM5MzcxNjJhOGFkMTg0ZGQ3MjhiYmI0MDQ5ZDg5MmUxZDVjOTAzMGY1MDdmN2ZmYjUwODNhY2U5YTViOWI0YjMzN2JiMzVkYjU0In0.eyJhdWQiOiIxNjA1MTgwMDgzODIzODc0MDQ4LjQzZDliNTM0OTMzMzFjNDRlMmRiM2UzNDMyODZmZWUzNTFkMDBmYjNjNzQ3NGZjZDdmZjUxNTEwOGE0MjQ0MTciLCJqdGkiOiIxYWQzNmMzOTM3MTYyYThhZDE4NGRkNzI4YmJiNDA0OWQ4OTJlMWQ1YzkwMzBmNTA3ZjdmZmI1MDgzYWNlOWE1YjliNGIzMzdiYjM1ZGI1NCIsImlhdCI6MTY3MjE0MDIxNCwibmJmIjoxNjcyMTQwMjE0LCJleHAiOjE2ODc2OTIyMTQsInN1YiI6IjE2MDUxODAwODM4MjM4NzQwNDgiLCJzY29wZXMiOlsicmVhZCIsIndyaXRlIl19.MdCFhbAwGac_nCs_d0k5GgPZ6ydJKpt6dzzn2SwtFk93KBuSj7yDX7_bpiN-oI2GpEFclRaXNF3Xtmfpvq2eB4s_jtV59yw0PTjpI8TObwgE9sxnIjxubtwYGLRw_dp1siAKJaAIY3XT1Xn4zcRSeGztVZjFa8YbqUrweTGsbvVkaOy2zWkXbH2QLlq6zeUMwDPfEhnMl7173CiNxZFVKnBJ-HdJgIb6FL5EjVCAdPEzoE_W3Md2aKtPu7uGzM9GVoLGefTxSBIA7DOpus2k1sj24F3_lSMn2JlyBbq6nubmSDRx9CyginAZ827Tbc9NoAxXZrOlQFuEuhoTv6ZZ2w"
        
        self.comment = None
        
        self.new_id = None
        self.old_id = None
        
        self.name = None


class View:     #アプリケーションのユーザーインターフェースを表すクラス。Modelからデータを取得し、それを表示するためのロジックを定義する。
    def __init__(self, model):
        self.model = model
    
    def save_user_name(self):
        self.model.user_name = self.user_name_entry.get()
        self.window.destroy()
        
    def user_name(self):
        self.window = tk.Tk()
        self.window.title("Twicas Comment Viewer")
        label = tk.Label(self.window, text="ツイキャスのユーザー名を入力してください")
        label.pack()
        
        # ユーザー名を入力するためのエントリーウィジェットを作成
        self.user_name_entry = tk.Entry(self.window)
        self.user_name_entry.pack()
        
        button = tk.Button(self.window, text="確定",command=self.save_user_name)
        button.pack()
        
        self.window.mainloop()
        

    
    def show_comments(self):
        window = tk.Tk()
        window.geometry("700x800")
        window.title("コメント")
        
        label1 = tk.Label(window, text="コメント一覧")
        label1.pack()
        textbox = tk.Text(window)
        textbox.pack()
        
        def get_comments():
            print("debug1")
            url = f"https://apiv2.twitcasting.tv/movies/{self.model.movie_id}/comments?offset=0&limit=1"
            
            ACCESS_TOKEN = self.model.ACCESS_TOKEN
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "X-Api-Version": "2.0"
            }
            
            response = requests.get(url, headers=headers)
            response_data = response.json()
            
            #print(len(response_data['comments']))
            #print(response_data)
            
            counts = response_data['all_count']     # コメント総数を取得
            self.model.count_comments = int(counts)   
            
            comments = response_data['comments']
            self.model.new_id = comments[0]['id']
            self.model.name = comments[0]['from_user']['name']
            self.model.comment = comments[0]['message']
            
            #print("new",self.model.new_id)
            #print("old",self.model.old_id)
            
            if self.model.new_id != self.model.old_id:
                text = f"{self.model.name}:{self.model.comment}\n"
                textbox.insert(0., text)
                self.model.old_id = self.model.new_id
                
                # VOICEBOX の API エンドポイント
                VOICEBOX_API_URL = "https://api.su-shiki.com/v2/voicevox/audio/?key=Z24_8-8-8-r_X0i"

                # 読み上げる文字列
                text = self.model.name + "さん　" + self.model.comment

                VOICEBOX_API_URL = VOICEBOX_API_URL + "&text=" + text

                # VOICEBOX の API を叩いて音声データを取得
                responseData = requests.get(VOICEBOX_API_URL).content

                # 音声データを保存
                with open("voice.wav", "wb") as f:
                    f.write(responseData)
                    
                playsound("voice.wav")
                os.remove("voice.wav")
            
            window.after(3000,get_comments)
        
        def send_comment():
            print(Str_input_Comment.get())
            url2 = f"https://apiv2.twitcasting.tv/movies/{self.model.movie_id}/comments"
            
            ACCESS_TOKEN = self.model.ACCESS_TOKEN
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "X-Api-Version": "2.0",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            comment_data = {
                "comment": Str_input_Comment.get(),
                "sns": "none"
            }
            
            response = requests.post(url2, headers=headers,data=json.dumps(comment_data))
            response_data = response.json()
            print(response_data)
            
        #コメント入力を格納
        Str_input_Comment = tk.StringVar()
        
        label2 = tk.Label(window, text="コメント入力")
        label2.pack()
        input_comment = tk.Entry(window, textvariable=Str_input_Comment, width=50)
        input_comment.pack()
        
        button = tk.Button(window, text="送信", command=send_comment)
        button.pack()
        
        
        get_comments()
        window.mainloop()
    
    def show_error_user_not_found(self):
        window = tk.Tk()
        window.title("Twicas Comment Viewer")
        label = tk.Label(window, text="ユーザー名が存在しません。再入力してください。")
        label.pack()
        
        button = tk.Button(window, text="OK",command=self.user_name)
        button.pack()
        
        window.mainloop()

class Controller:   #アプリケーションのロジックを定義するクラス。ModelとViewを使用して、アプリケーションを制御します。
    def __init__(self,view,model):
        self.view = view
        self.model = model
    
    
    
    def get_movie_id(self): # movie_idを取得する
        while True:
            url = f"https://apiv2.twitcasting.tv/users/{self.model.user_name}"
            print("Debug user name",self.model.user_name)
            
            ACCESS_TOKEN = self.model.ACCESS_TOKEN
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "X-Api-Version": "2.0"
            }
            
            response = requests.get(url, headers=headers)
            response_data = response.json()
            
            if 'error' in response_data:    #ユーザーが見つからない場合のエラー処理
                self.view.show_error_user_not_found()
            
            break
        
        name = response_data['user']['name']
        movie_id = response_data['user']['last_movie_id']
        self.model.name = name
        self.model.movie_id = movie_id
        
        
        self.view.show_comments()
        
    def get_user_name(self):    #ユーザー名を取得する
        self.view.user_name()
        
        self.get_movie_id()

def main():
    model = Model()
    view = View(model)
    controller = Controller(view, model)
    
    controller.get_user_name()

if __name__ == '__main__':
    main()