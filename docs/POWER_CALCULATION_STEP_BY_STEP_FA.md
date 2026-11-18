# محاسبه توان پمپ و موتور

## بخش فارسی

### روش‌های موجود
۱. راندمان دستی: راندمان پمپ و موتور را جداگانه بر حسب درصد وارد کنید.
۲. منحنی پمپ: ۲ تا ۳۰ نقطه دبی و هد وارد کنید؛ راندمان پمپ و توان محور اختیاری‌اند.
۳. راندمان پیش‌فرض: اگر راندمان خالی باشد، ۱۰۰٪ فرض می‌شود؛ این مقدار ایده‌آل است و عملکرد واقعی نیست.

### روابط
`Ph=ρgQH`
`Pshaft=Ph/ηpump`
`Pelectric=Pshaft/ηmotor`

### مثال
برای Q=50 m³/h، TDH=40 m، چگالی ۱۰۰۰ kg/m³، راندمان پمپ ۷۸٪ و موتور ۹۲٪:
- توان هیدرولیکی ≈ ۵٫۴۵ kW
- توان محور ≈ ۶٫۹۹ kW
- توان برق ورودی ≈ ۷٫۶۰ kW

### محدودیت‌ها
درون‌یابی منحنی خطی و فقط داخل محدوده دبی ورودی است. نقطه کار واقعی از تقاطع منحنی پمپ و سیستم محاسبه نمی‌شود. تلفات VFD، شرایط راه‌اندازی، NPSH و ضربه قوچ لحاظ نمی‌شوند. توان برق ورودی به‌تنهایی انتخاب توان نامی موتور نیست.

## English Section

### Available methods
1. Manual efficiencies: enter pump and motor efficiency separately as percentages.
2. Pump curve: enter 2–30 flow/head points; pump efficiency and shaft power are optional.
3. Default efficiency: a blank efficiency is assumed to be 100%; this is idealized and not actual performance.

### Equations
`Ph=ρgQH`
`Pshaft=Ph/ηpump`
`Pelectric=Pshaft/ηmotor`

### Worked example
For Q=50 m³/h, TDH=40 m, density=1000 kg/m³, pump efficiency=78% and motor efficiency=92%:
- Hydraulic power ≈ 5.45 kW
- Shaft power ≈ 6.99 kW
- Electrical input ≈ 7.60 kW

### Limitations
Curve interpolation is linear and only within the entered flow range. The actual duty point is not solved from pump/system curve intersection. VFD losses, starting conditions, NPSH and water hammer are not included. Electrical input power alone is not a motor nameplate selection.
