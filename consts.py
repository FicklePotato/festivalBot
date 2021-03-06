# -*- coding: utf-8 -*-
ROOT_OUT_PATH = r"media"
DUMP_TIME = 10
MAX_TIMES = 3
MISSION_SCORE = {'1': 1, '10': 2, '11': 2, '12': 2, '13': 2, '14': 2, '15': 2, '16': 2, '17': 2, '18': 3, '19': 3, '2': 1, '20': 3, '21': 3, '22': 3, '23': 3, '24': 3, '25': 3, '26': 3, '27': 3, '28': 3, '29': 3, '3': 1, '30': 3, '31': 3, '32': 3, '33': 3, '34': 3, '35': 3, '36': 3, '37': 3, '38': 3, '39': 4, '4': 1, '40': 4, '41': 4, '42': 4, '43': 4, '44': 4, '45': 4, '46': 4, '47': 4, '48': 4, '49': 4, '5': 2, '50': 4, '51': 4, '52': 4, '53': 4, '54': 5, '55': 5, '56': 5, '57': 5, '58': 5, '59': 5, '6': 2, '60': 5, '61': 5, '62': 5, '63': 6, '64': 8, '7': 2, '8': 2, '9': 2}
TITLE_LOC = 1
MISSION_LOC = 0
JSON_PATH = r"groups.json"
ADMIN_IDS = [409589602, 596310448]
HELP_MSG = """
כללי המשחק:
- אם אין תיעוד לכך שהמשימה בוצעה בתמונה או סרטון, לא ניתן לקבל ניקוד על המשימה.
- בתיאור של כל תמונה/סרטון יש לכתוב את מספר המשימה. משימה שלא יהיה כתוב בתיאורה את מספר המשימה, לא תיחשב!
- כל משימה ניתן לבצע פעם אחת בלבד.
כדאי לדעת:
- אם יש שאלות, מוזמנים לשלוח לנו אותן אל המייל הבא: YearotChallenge@gmail.com
- מומלץ להוריד למכשיריכם את רשימת המשימות, כדי שלא תצטרכו חיבור אינטרנטי על מנת להתבונן בהן בהמשך.
- המשימות רשומות בלשון רבים, אך חלקן יכולות להתבצע על ידי אדם אחד מהקבוצה (כתלות במשימה).
- כדי לקבל את סכום הנקודות שצברתם עד כה, יש לשלוח את ההודעה "/score" (כותבים את הסלאש לפני המילה). כדי לקבל שוב את הוראות המשחק יש לשלוח את ההודעה "/help" (כנ"ל).
לרשימת המשימות היכנסו לקישור הבא: https://tinyurl.com/y8ly78ca
"""

START_MSG = """
ברוכים הבאים ליערות מנשה צ'לנג'! 
הצ'לנג' הוא תחרות נושאת פרסים (מקום ראשון – כרטיסים לפסטיבל שנה הבאה! מקום שני – חולצות של הפסטיבל!) אליה נרשמים עם החברים (עד 4 בקבוצה), מבצעים כמה שיותר משימות באופן הכי טוב שאפשר, נהנים מהחוויה, ואולי זוכים בפרס הגדול!
כדאי לקרוא את ההוראות שלהלן, חבל לפספס נקודות כי לא שמתם לב...
{0}
שיהיה בהצלחה!!
""".format(HELP_MSG)
