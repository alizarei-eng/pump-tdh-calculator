# Pump and Motor Power Calculation | محاسبه توان پمپ و موتور

## 1. Purpose | هدف
**EN:** This guide explains the optional power calculation after the system TDH has been calculated. The program can use manual efficiencies, entered pump-curve points, or an idealized 100% default.

**FA:** این راهنما بخش اختیاری محاسبه توان پس از محاسبه TDH را توضیح می‌دهد. برنامه می‌تواند از راندمان دستی، نقاط منحنی پمپ یا فرض ایده‌آل ۱۰۰٪ استفاده کند.

## 2. Three available methods | سه روش موجود
1. **Manual efficiencies | راندمان دستی:** enter pump efficiency and motor efficiency separately as percentages. | راندمان پمپ و موتور را جداگانه و بر حسب درصد وارد کنید.
2. **Pump curve | منحنی پمپ:** enter 2–30 points sequentially. Each point requires flow (m³/h) and head (m); pump efficiency (%) and shaft power (kW) are optional. | ۲ تا ۳۰ نقطه را مرحله‌ای وارد کنید. دبی و هد الزامی و راندمان پمپ و توان محور اختیاری‌اند.
3. **100% default | پیش‌فرض ۱۰۰٪:** the program assumes ideal pump and motor efficiencies. | برنامه راندمان پمپ و موتور را ایده‌آل و برابر ۱۰۰٪ فرض می‌کند.

If an efficiency is left blank, 100% is assumed for that missing value. This is an idealized lower-bound calculation, not measured performance.

اگر راندمان خالی بماند، برای همان ورودی ۱۰۰٪ فرض می‌شود. این محاسبه حد پایین ایده‌آل است، نه عملکرد اندازه‌گیری‌شده.

## 3. Equations | روابط
`Ph=ρgQH`
`Pshaft=Ph/ηpump`
`Pelectric=Pshaft/ηmotor`

Use Q in m³/s, density in kg/m³ and head in metres. The program reports power in kW.

دبی باید بر حسب m³/s، چگالی بر حسب kg/m³ و هد بر حسب متر باشد. برنامه توان را بر حسب kW گزارش می‌کند.

## 4. Worked example | مثال
Given Q=50 m³/h, TDH=40 m, density=1000 kg/m³, pump efficiency=78% and motor efficiency=92%:

- Q=50/3600=0.013889 m³/s
- Hydraulic power ≈ 5.45 kW
- Pump shaft power ≈ 5.45/0.78 = 6.99 kW
- Electrical input ≈ 6.99/0.92 = 7.60 kW

با دبی ۵۰، TDH برابر ۴۰ متر، چگالی ۱۰۰۰، راندمان پمپ ۷۸٪ و موتور ۹۲٪، توان هیدرولیکی حدود ۵٫۴۵، توان محور ۶٫۹۹ و توان برق ورودی ۷٫۶۰ کیلووات است. مقدار FINAL REQUIRED ELECTRICAL POWER همان Electrical input power است.

## 5. Pump curve interpolation | درون‌یابی منحنی پمپ
The program validates unique flow values and interpolates head, efficiency and shaft power independently when at least two valid values are available for the selected quantity. It sorts points by flow and never extrapolates outside the entered flow range. Motor efficiency is still entered separately.

برنامه یکتایی دبی‌ها را کنترل می‌کند و هد، راندمان و توان محور را در صورت وجود حداقل دو مقدار معتبر برای هر کمیت، مستقل درون‌یابی می‌کند. نقاط بر اساس دبی مرتب می‌شوند و خارج از محدوده برون‌یابی وجود ندارد. راندمان موتور جداگانه وارد می‌شود.

## 6. Suitable applications | موارد کاربرد مناسب
- **EN:** Estimating hydraulic, shaft and electrical input power at a known flow and calculated TDH.
- **FA:** تخمین توان هیدرولیکی، محور و برق ورودی در دبی و TDH مشخص.
- **EN:** Using manufacturer pump efficiency and shaft-power data when the curve matches the exact pump, impeller diameter, speed and operating frequency.
- **FA:** استفاده از راندمان و توان محور سازنده، به شرط انطباق منحنی با مدل پمپ، قطر پروانه، دور و فرکانس واقعی.

## 7. Limitations | محدودیت‌ها
- The tool does not determine the actual operating point by intersecting the pump and system curves. | نقطه کار واقعی از تقاطع منحنی پمپ و سیستم تعیین نمی‌شود.
- Linear interpolation is only an estimate between supplied points; it is not a replacement for the complete manufacturer curve. | درون‌یابی خطی فقط تخمین بین نقاط ورودی است و جایگزین منحنی کامل سازنده نیست.
- No extrapolation is performed beyond the curve flow range. | خارج از محدوده دبی منحنی برون‌یابی انجام نمی‌شود.
- 100% default efficiency is idealized and must not be used as actual efficiency or motor sizing data. | راندمان پیش‌فرض ۱۰۰٪ ایده‌آل است و نباید راندمان واقعی یا مبنای انتخاب موتور تلقی شود.
- VFD losses, starting conditions, motor service factor, NPSH, cavitation and water hammer are not included. | تلفات VFD، شرایط راه‌اندازی، ضریب سرویس موتور، NPSH، کاویتاسیون و ضربه قوچ لحاظ نمی‌شوند.
- Electrical input power is not automatically the required motor nameplate rating. Verify shaft-power demand across the full operating range and follow manufacturer recommendations. | توان برق ورودی به‌صورت خودکار توان نامی موتور نیست. توان محور را در کل محدوده کاری بررسی و توصیه سازنده را رعایت کنید.

## 8. Tests | آزمون‌ها
```bash
python -m unittest discover -s tests -v
```
