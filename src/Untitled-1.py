import requests
import pandas as pd

def Getdata(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            data = requests.get(url, headers=headers)
            data.raise_for_status()
            print("---> Get Data <---")
            return data.text
        except requests.RequestException as re:
            print(f"Network Error: {re}")
            return None

def clean_dataframe(data):
        col = [
            "id",
            "id_info",
            "نماد",
            "نام نماد",
            "?",
            "اولین",
            "پایانی",
            "معامله",
            "تعداد معاملات",
            "حجم معاملات",
            "ارزش معاملات",
            "کمترین بازه روز",
            "بیشترین بازه روز",
            "بازده دیروز",
            "EPS",
            "حجم مبنا",
            "?",
            "?",
            "کد گروه صنعت",
            "قیمت مجاز بیشترین",
            "قیمت مجاز کمترین",
            "تعداد سهام",
            "?",
            "NAV ابطال",
            "موقعیت های باز",
        ]
        try:
            df_main = pd.DataFrame((data.split("@")[2]).split(";"))
            df_split = df_main[0].str.split(",", expand=True)
            print("---> clean code1 <---")
            for item in range(len(col)):
                df_split.rename(columns={item: f"{col[item]}"}, inplace=True)
            print("---> clean code2 <---")
            return df_split
        except Exception as e:
            print(f"NO Data! , Error {e}")

def Clock_Date_namd(data):
        col = ['ساعت معامله', 'تاریخ معامله']
        try:
            df_main = pd.DataFrame((data.split("@")[1]).split(';'))

        except Exception as e:
            print(f"NO Data! , Error {e}")
