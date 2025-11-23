"""Generate a synthetic Thai booking dataset (JSONL) with varied templates.
Produces records of the shape used by your schema:
{ "input": "<text>", "output": { ... } }
"""
import json
import random
from datetime import datetime, timedelta
import argparse


LOCATIONS = ["สุขุมวิท","บางซื่อ","ดอนเมือง","สีลม","สาทร","พระราม9","สุขุมวิท26","ลาดพร้าว","ชิดลม"]
PURPOSES = ["ไปอบรม","ไปประชุม","ไปดูงาน","ไปสัมมนา","เที่ยว","เยี่ยมลูกค้า"]
ROOM_TYPES = [("เดี่ยว",1),("คู่",2),("เตียงเดี่ยว",1),("เตียงคู่",2)]


TEMPLATES = [
"จองโรงแรม{loc} {date_range} {purpose} ห้อง{room_type} {num_rooms} ห้อง {extra}",
"{loc} {date_range} {purpose} {num_rooms} ห้อง {room_type} {extra}",
"ต้องการจองที่พักแถว{loc} วันที่ {date_short} ไป{purpose} ห้อง{room_type} {extra}",
"{loc} {num_rooms} ห้อง {room_type} {num_guests} คน ไม่สูบบุหรี่ ไม่มีอาหารเช้า {date_range} {purpose}",
]


EXTRAS = [
"สูบบุหรี่ มีอาหารเช้า",
"ไม่สูบบุหรี่ ไม่มีอาหารเช้า",
"สูบบุหรี่ ไม่มีอาหารเช้า",
"ไม่สูบบุหรี่ มีอาหารเช้า",
"รวมอาหารเช้า",
]




def random_date_pair(start_days=1, max_span=5):
start = datetime(2025,12,1) + timedelta(days=random.randint(0,25))
span = random.randint(1,4)
end = start + timedelta(days=span)
return start, end




def make_date_strings(start,end):
# formats used in Thai sentences
# e.g. "5-8 ธ.ค." or "11 ธ.ค. ถึง 14 ธ.ค." or "11-14 ธ.ค."
if start.month==end.month:
return f"{start.day}-{end.day} {start.strftime('%b')}." # month abbrev
else:
return f"{start.day} {start.strftime('%b')}. ถึง {end.day} {end.strftime('%b')}."




def build_output(loc,purpose,start,end,room_type,num_rooms,num_guests,smoking,breakfast,raw_text):
return {
"location": loc,
"purpose": purpose,
"check_in": start.strftime("%Y-%m-%d"),
"check_out": end.strftime("%Y-%m-%d"),
"room_type": room_type,
generate(args.n, args.out)