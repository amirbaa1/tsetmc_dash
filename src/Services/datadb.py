import requests
import pandas as pd
import numpy as np
from datetime import datetime
from requests.exceptions import RequestException
import os


class Database:
    @staticmethod
    def Getdata(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            data = requests.get(url, headers=headers)
            data.raise_for_status()
            print("---> Get Data <---")
            return data.text
        except RequestException as re:
            print(f"Network Error: {re}")
            return None

    @staticmethod
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
            # "NAV ابطال",
            # "موقعیت های باز",
        ]
        try:
            df_main = pd.DataFrame((data.split("@")[2]).split(";"))
            df_split = df_main[0].str.split(",", expand=True)
            print("---> clean code1 <---")
            for item in range(len(col)):
                df_split.rename(columns={item: f"{col[item]}"}, inplace=True)
            # df_split = df_split.drop(columns=["NAV ابطال","موقعیت های باز"],axis=0)
            print("---> clean code2 <---")
            return df_split
        except Exception as e:
            print(f"NO Data! , Error {e}")

    @staticmethod
    def Clock_Date_namd(data, df):
        try:
            df_main_clock = pd.DataFrame((data.split("@")[1]).split(","))
            colok = df_main_clock.loc[0]
            date_time_str = colok[0].strip()
            if date_time_str:
                date, time = date_time_str.split()

                df["ساعت معامله"] = time
                df["تاریخ معامله"] = date

                print(f"---> Add Time and Date in namad : {time} <---")
                # df.insert(8, "تاریخ معامله'", df.pop("تاریخ معامله'"))
                # df.insert(9, "ساعت معامله'", df.pop("ساعت معامله'"))

                return df
            else:
                print(f"NO Date and Time!")
        except Exception as e:
            print(f"NO Date and Time! , Error {e}")

    @staticmethod
    def clean_namd(df):
        df_split_values = df["نام نماد"].str.split("-")
        df["نام نماد"] = df_split_values.str[0]
        df["مقدار"] = df_split_values.str[1]
        df["تاریخ"] = df_split_values.str[2]
        df.insert(4, "نام نماد", df.pop("نام نماد"))
        df.insert(6, "مقدار", df.pop("مقدار"))
        df.insert(8, "تاریخ", df.pop("تاریخ"))
        print("---> clean namd <---")
        df = df[df["نام نماد"].apply(
            lambda x: "اختيار" in x)].reset_index(drop=True)
        print("---> split ektiar <---")
        return df

    @staticmethod
    def split_buy_sell(df):
        df["وضعیت"] = np.where(
            df["نام نماد"].str.contains("اختيارخ"), "خرید", "فروش")
        df.insert(5, "وضعیت", df.pop("وضعیت"))
        print("---> split buy_sell <---")

        df["دسته"] = df["نام نماد"].str.extract(r"\s(.+)$")
        df.insert(4, "دسته", df.pop("دسته"))
        print("---> split nmad <---")
        return df

    @staticmethod
    def clean_time(time):
        try:
            if len(time) == 8 and "/" not in time:
                year = int(time[:4])
                month = int(time[4:6])
                day = int(time[6:])
                print("---> clean time <---")
                return f"{year}/{month:02d}/{day:02d}"
            else:
                return time
        except Exception as e:
            print("Error clena_time : ", e)

        # def clena_time2(time):
        #     try:
        #         time_split = time.split('/')

        except Exception as e:
            print(e)

    @staticmethod
    def apply_time(df):
        df["تاریخ"] = df["تاریخ"].apply(lambda time: Database.clean_time(time))
        return df

    @staticmethod
    def SaveToExcel(df):
        try:
            # df.to_excel(r"../tsetmc/df_ektiar.xlsx") macOS
            # df.to_excel(r"E:\code\data_vizi\tsetmc_dash\tsetmc\App\Data\df_ektiar.xlsx") # win

            directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(directory, "..", "Data", "df_ektiar.xlsx")
            if not os.path.exists(file_path):
                df.to_excel(os.path.join(directory, "..", "Data", "df_ektiar.xlsx"), index=False)
                print(f"*---> {datetime.now()}: Data Save to excel successfully in file new <---*")

            else: 
                df_old = pd.read_excel(file_path)

                    # Print the data for debugging
                    # print(df)
                    # print("===")
                    # print(df_old)
                    # print("===")

                df.to_excel(os.path.join(directory, "..", "Data", "df_new.xlsx"), index=False)

                df_new = pd.read_excel(os.path.join(directory, "..", "Data", "df_new.xlsx"))
                df_concat = pd.concat([df_old, df_new],ignore_index=True)

                df_concat.to_excel(file_path, index=False)


                print(f"*---> {datetime.now()}: Data Save to excel successfully <---*")
        except Exception as e:
            print(f"no save Error!! Error Details: {e}")
            print(f"old :{df_old.columns} ", len(df_old.columns))
            print(f"new :{df.columns} ", len(df.columns))

    @staticmethod
    def Database_Tsetmc():
        url = "https://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx"
        data = Database.Getdata(url=url)
        if data:
            clean = Database.clean_dataframe(data)
            add_time_date = Database.Clock_Date_namd(data, clean)
            clean_status = Database.clean_namd(add_time_date)
            clean_status = Database.split_buy_sell(clean_status)
            clean_time = Database.apply_time(clean_status)

            if clean_status is not None:
                Database.SaveToExcel(clean_time)
# Database.Database_Tsetmc()

# x = Getdata("https://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx")
# clean = clean_dataframe(x)
# SaveToExcel(clean_namd(clean))

# if __name__ == "__main__":
#     url = "https://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx"
#     data = Getdata(url=url)
#     if data:
#         clean = clean_dataframe(data)
#         if clean is not None:
#             SaveToExcel(clean_namd(clean))
