import time
import requests
from datetime import datetime, date, timedelta

# ----------------- ตั้งค่าข้อมูลของคุณ -----------------
TOKEN = "YOUR_TOKEN" 
BIRTHDAY = date(2026, 11, 12)       # วันเกิดของคุณ (12 พ.ย. 26)
# -----------------------------------------------------

def get_status_text():
    today = date.today()
    if today == BIRTHDAY:
        return "สุขสันต์วันเกิดให้ฉัน🎉🎂!"
    elif today > BIRTHDAY:
        return "ผ่านวันเกิดของฉันไปแล้วภารกิจจบลงแล้ว! ✨"
    else:
        days_left = (BIRTHDAY - today).days
        return f"อีก {days_left} วันจะเป็นวันเกิดของฉัน🎉🎂!"

def change_discord_status(status_message):
    """ฟังก์ชันส่งคำขอเปลี่ยนสถานะไปยัง Discord พร้อมระบบเช็ค Error"""
    url = "https://discord.com/api/v9/users/@me/settings"
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "custom_status": {
            "text": status_message
        }
    }
    
    try:
        response = requests.patch(url, json=payload, headers=headers)
        
        # --- ส่วนที่อัปเดตระบบเช็คความถูกต้องของ Token ---
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] เปลี่ยนสถานะสำเร็จเป็น: {status_message}")
        elif response.status_code == 401:
            print("\n🚨 ข้อผิดพลาด: Token ไม่ถูกต้อง หรือหมดอายุแล้ว! บอทขออนุญาตปิดตัวลงเพื่อความปลอดภัย")
            exit()  # สั่งให้บอทหยุดรันทันที ไม่ฝืนต่อ
        else:
            print(f"เกิดข้อผิดพลาดจาก Discord API: {response.status_code} - {response.text}")
        # -----------------------------------------------
            
    except Exception as e:
        print(f"ไม่สามารถเชื่อมต่อกับ Discord ได้: {e}")

def seconds_until_0001():
    """คำนวณจำนวนวินาทีจากตอนนี้ ไปจนถึงเวลา 00:01 น. ของวันถัดไป"""
    now = datetime.now()
    tomorrow_0001 = datetime.combine(now.date() + timedelta(days=1), datetime.strptime("00:01", "%H:%M").time())
    seconds_left = (tomorrow_0001 - now).total_seconds()
    return int(seconds_left)

def main():
    print("==============================================")
    print(" บอทนับถอยหลังวันเกิดทำงานแล้ว (โหมดปลอดภัยสูง) ")
    print("==============================================")
    
    # รันครั้งแรกตอนเปิดบอท เพื่อตรวจเช็คความถูกต้องของ Token ทันที
    first_status = get_status_text()
    change_discord_status(first_status)
    
    while True:
        # คำนวณเวลานอนหลับจนกว่าจะถึง 00:01 น. ของวันรุ่งขึ้น
        sleep_duration = seconds_until_0001()
        
        hours = sleep_duration // 3600
        minutes = (sleep_duration % 3600) // 60
        print(f"บอทกำลังเข้าสู่โหมดจำศีล จะตื่นขึ้นมาเปลี่ยนสถานะในอีก {hours} ชั่วโมง {minutes} นาที (เวลา 00:01 น.)")
        
        # หลับยาวจนถึงเที่ยงคืนหนึ่งนาที
        time.sleep(sleep_duration)
        
        # เมื่อถึงเวลา 00:01 น. บอทจะตื่นมาทำส่วนนี้
        new_status = get_status_text()
        change_discord_status(new_status)
        
        # ถ้ารันจนเลยวันเกิดแล้ว สั่งให้บอทหยุดทำงานถาวร
        if date.today() > BIRTHDAY:
            print("ภารกิจเสร็จสิ้น! เลยวันเกิดแล้ว ขอปิดบอทอัตโนมัติครับ")
            break

if __name__ == "__main__":
    main()
