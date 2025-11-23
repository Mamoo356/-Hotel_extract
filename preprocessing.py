# helper functions: normalize text, fix typos, parse dates, and canonicalize outputs
from rapidfuzz import process
import re
from dateparser import parse as dateparse
from pythainlp.tokenize import word_tokenize


# small dictionaries/corrections
LOCATIONS = ["สุขุมวิท","บางซื่อ","ดอนเมือง","สีลม","สาทร","พระราม9","ลาดพร้าว","ชิดลม"]
ROOM_MAP = {"เดี่ยว":"เดี่ยว","ห้องเดี่ยว":"เดี่ยว","คู่":"คู่","เตียงเดี่ยว":"เดี่ยว","เตียงคู่":"คู่"}




def fix_location(text):
# use fuzzy match
choice,score = process.extractOne(text, LOCATIONS)
if score > 60:
return choice
return None




def parse_date_range(text, prefer_year=2025):
# try to find two dates; fallback to single date
# This is a simple heuristic; production code should be more robust
dates = []
# find patterns like 5-8 ธ.ค. or 11 ธ.ค. ถึง 14 ธ.ค.
m = re.search(r"(\d{1,2})\s*-\s*(\d{1,2})\s*([\u0E00-\u0E7Fa-zA-Z\.]+)", text)
if m:
d1 = f"{m.group(1)} {m.group(3)} {prefer_year}"
d2 = f"{m.group(2)} {m.group(3)} {prefer_year}"
a = dateparse(d1, languages=['th'])
b = dateparse(d2, languages=['th'])
if a and b:
return a.date().isoformat(), b.date().isoformat()
# fallback: find two individual dates
matches = re.findall(r"(\d{1,2})\s*(?:ม\.|ธ\.ค\.|ธ.ค\.|ก\.ย\.|ต\.ค\.|พ\.ย\.|พย\.)", text)
if len(matches) >= 2:
# crude fallback
a = dateparse(matches[0] + ' ธ.ค. ' + str(prefer_year), languages=['th'])
b = dateparse(matches[1] + ' ธ.ค. ' + str(prefer_year), languages=['th'])
if a and b:
return a.date().isoformat(), b.date().isoformat()
# final fallback: single date
dt = dateparse(text, languages=['th'])
if dt:
return dt.date().isoformat(), (dt + timedelta(days=1)).date().isoformat()
return None, None




def normalize_room_type(text):
for k in ROOM_MAP:
if k in text:
return ROOM_MAP[k]
return None




def extract_bool(text, token):
# token e.g. 'สูบบุหรี่' or 'อาหารเช้า'
if token in text:
return None