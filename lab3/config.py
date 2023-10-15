M1 = [0,31,28,31,30,31,30,31,31,30,31,30,31]
M2 = [0,31,29,31,30,31,30,31,31,30,31,30,31]
DM = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
DW = {0:'M',1:'Tu',2:'W',3:'Th',4:'F',5:'Sa',6:'Su'}

Init_Time = (
    2023,  # Year
    10,  # Month
    3,  # Day
    -1,  # Week 周几好像随便设，会根据年月日自动生成，0_6为周一_周日
    0,  # Hour
    0,  # Minute
    0,  # Second
    0,  # Millisecond
)

Hour_Set = 12
Minute_Set = 25

Blink_Interval_ms = 500  # deviation: +- 40ms

Alarm_Interval_ms = 800  # deviation: +- 40ms
Alerm_Frequency = 500  # with range 0 to 1024
Alerm_Duty = 100  # with range 0 to 1024
Alarm_Time = 5
