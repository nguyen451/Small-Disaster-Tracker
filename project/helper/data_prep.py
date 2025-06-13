import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import re
import unicodedata

def transform(csvfilename : str):
    df = pd.read_csv(csvfilename)
    
    clean(df)

    field_edit(df)

    df.to_csv("proper_data.csv")

    return df

def clean(df) -> None:
    df.drop_duplicates(inplace=True)
    df.drop(columns=["disaster_level"], inplace=True) # "kv_anhhuong", 
    df.dropna(subset=["name"], inplace=True)
    df["name"] = df["name"].str.strip()


    for col in ["type", "level"]:
        df[col] = df[col].astype("category")

    df["time_start"] = pd.to_datetime(df["time_start"]).dt.date
    df["name"] = df["name"].str.strip()


def field_edit(df) -> None:
    provinces_and_east_Sea = [
    "An Giang", "Ba Ria - Vung Tau", "Bac Lieu", "Bac Giang", "Bac Kan",
    "Bac Ninh", "Ben Tre", "Binh Duong", "Binh Đinh", "Binh Phuoc",
    "Binh Thuan", "Ca Mau", "Cao Bang", "Can Tho", "Đa Nang",
    "Đak Lak", "Đak Nong", "Đien Bien", "Đong Nai", "Đong Thap",
    "Gia Lai", "Ha Giang", "Ha Nam", "Ha Noi", "Ha Tinh",
    "Hai Duong", "Hai Phong", "Hau Giang", "Hoa Binh", "Hung Yen",
    "Khanh Hoa", "Kien Giang", "Kon Tum", "Lai Chau", "Lang Son",
    "Lao Cai", "Lam Đong", "Long An", "Nam Dinh", "Nghe An",
    "Ninh Binh", "Ninh Thuan", "Phu Tho", "Phu Yen", "Quang Binh",
    "Quang Nam", "Quang Ngai", "Quang Ninh", "Quang Tri", "Soc Trang",
    "Son La", "Tay Ninh", "Thai Binh", "Thai Nguyen", "Thanh Hoa",
    "Thua Thien Hue", "Tien Giang", "TP. Ho Chi Minh", "Tra Vinh", "Tuyen Quang",
    "Vinh Long", "Vinh Phuc", "Yen Bai", "Bien Đong"
    ]

    df["province"] = df.apply(lambda x : extract_province2(x["kv_anhhuong"]), axis=1)
    filtered = [prov in provinces_and_east_Sea for prov in df["province"]]
    filtered = df[filtered]
    filtered.drop(columns=["kv_anhhuong"], inplace=True)


def remove_accents(text : str) -> str:
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])


def normalize_text(text : str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    text = remove_accents(text)
    text = text.title()
    return text


def extract_province2(kv_anhhuong) -> str:
    mat = re.search(r"tỉnh\s*(.*)", kv_anhhuong, re.IGNORECASE)
    if mat:
        return normalize_text(mat.group(1))
    
    mat = re.search(r"Tp\.*\s*(.*)", kv_anhhuong, re.IGNORECASE)
    if mat:
        return normalize_text(mat.group(1))
    
    mat = re.search(r"Thành Phố\s*(.*)", kv_anhhuong, re.IGNORECASE)
    if mat:
        return normalize_text(mat.group(1))
    
    return normalize_text(kv_anhhuong)


if __name__ == "__main__":
    transform("disasters_2.csv")
