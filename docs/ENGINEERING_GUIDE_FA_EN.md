# Engineering Guide | راهنمای مهندسی
## Pump TDH Calculator | محاسبه‌گر هد کل پمپ

## 1. Scope | دامنه
**EN:** The program estimates the total head required to move a fluid between two defined system boundaries. It adds static elevation, pressure-head difference, velocity-head difference, pipe friction, fitting losses and equipment pressure losses. It supports optional pump-power estimation.

**FA:** برنامه هد کل لازم برای انتقال سیال بین دو مرز مشخص را تخمین می‌زند. اختلاف ارتفاع، هد فشار، هد سرعت، افت اصطکاکی لوله، افت فیتینگ‌ها و افت تجهیزات با هم ترکیب می‌شوند. محاسبه توان پمپ نیز اختیاری است.

## 2. Fluid inputs | ورودی سیال
EC is entered in mS/cm and must already be compensated to 25°C. The actual operating water temperature is entered separately and used for density/viscosity estimates. The internal default TDS factor is approximate (0.65); the user does not enter a conversion factor. Generic profile does not infer individual ions. Natural-seawater profile assumes standard seawater ratios and is not a substitute for laboratory analysis.

EC بر حسب mS/cm وارد می‌شود و باید از قبل تا ۲۵°C جبران شده باشد. دمای واقعی کارکرد جداگانه وارد می‌شود و برای تخمین چگالی و ویسکوزیته کاربرد دارد. ضریب داخلی TDS تقریبی و برابر ۰٫۶۵ است؛ کاربر آن را وارد نمی‌کند. پروفایل عمومی یون‌های منفرد را حدس نمی‌زند. پروفایل آب دریا نسبت‌های استاندارد را فرض می‌کند و جایگزین آزمایش نیست.

## 3. Static elevation | هد استاتیکی
Two input methods are available:
1. Direct elevation difference Δz.
2. Start and end elevations z1 and z2 measured from one common datum.

`Δz = z2 - z1`.

A positive result means the destination is higher. A negative result means it is lower. Example: z1=10 m and z2=35 m gives Δz=+25 m.

دو روش ورود وجود دارد: اختلاف ارتفاع مستقیم یا تراز ابتدا و انتها نسبت به یک مبنای مشترک. مقدار مثبت یعنی مقصد بالاتر است. مثال: تراز ۱۰ تا ۳۵ متر، هد استاتیکی مثبت ۲۵ متر دارد.

## 4. Pipe geometry and roughness | هندسه و زبری لوله
For HDPE, choose grade PE80/PE100, SDR and catalogue OD. The program obtains nominal wall thickness and calculates `ID=OD−2e`. For other materials, enter OD and nominal wall thickness; ID is derived. Absolute roughness is loaded from the material database for listed materials.

برای HDPE گرید، SDR و OD انتخاب می‌شود؛ ضخامت اسمی از بانک خوانده و ID محاسبه می‌شود. برای سایر مواد OD و ضخامت اسمی وارد می‌شود. زبری مطلق مواد فهرست‌شده خودکار از بانک بارگذاری می‌شود.

## 5. System losses | افت‌های سیستم
Darcy–Weisbach major loss:
`hf = f(L/D)(V²/2g)`.

Fitting minor loss:
`hm = ΣK(V²/2g)`.

Equipment loss from pressure drop:
`hequipment = ΔPequipment/(ρg)`.

For equipment such as bag filters, cartridge filters, sand filters and RO units, enter the actual measured or manufacturer pressure drop at the operating flow. Do not assign a generic K where the program expects pressure-drop data.

برای تجهیزاتی مانند فیلتر کیسه‌ای، کارتریجی، شنی و RO، افت فشار اندازه‌گیری‌شده یا اعلام‌شده سازنده را در دبی کاری وارد کنید. برای تجهیزی که افت فشار واقعی آن لازم است، K عمومی فرض نکنید.

## 6. Boundary energy terms | مؤلفه‌های مرزی انرژی
`Δ(P/ρg)` is based on the pressure difference between the selected start and end boundaries. For open tanks at atmospheric pressure, gauge pressure is zero at both free surfaces. The velocity-head term is based on the velocities at the two boundary sections; large reservoir free-surface velocities are often approximated as zero.

هد فشار از اختلاف فشار دو مرز به دست می‌آید. برای مخازن باز به اتمسفر، فشار گیج سطح آزاد هر دو صفر است. هد سرعت نیز از سرعت دو مقطع مرزی محاسبه می‌شود؛ سرعت سطح آزاد مخزن بزرگ معمولاً نزدیک صفر فرض می‌شود.

## 7. Total Dynamic Head | هد کل دینامیکی
`TDH = Δz + Δ(P/ρg) + Δ(V²/2g) + hf + hm + hequipment`.

Check signs and boundary definitions carefully. A negative TDH should trigger a review of flow direction, elevations, pressures and reference sections rather than being blindly accepted.

علامت مؤلفه‌ها و تعریف مقاطع را کنترل کنید. TDH منفی باید باعث بازبینی جهت جریان، ارتفاع‌ها، فشارها و مرزهای سیستم شود.

## 8. Power calculation | محاسبه توان
Hydraulic power:
`Ph(kW)=ρgQH/1000`, with Q in m³/s and H in m.

Pump shaft power:
`Pshaft=Ph/ηpump`.

Motor electrical input:
`Pelectric=Pshaft/ηmotor`.

ηpump and ηmotor are decimal efficiencies in the equations (e.g. 78%=0.78). The CLI accepts percentages. If left blank, 100% is assumed and must be identified as an ideal assumption. VFD losses are not separately included.

راندمان‌ها در فرمول به‌صورت عدد اعشاری هستند؛ مثلاً ۷۸٪ برابر ۰٫۷۸ است. برنامه درصد دریافت می‌کند. ورودی خالی به معنی فرض ۱۰۰٪ است و باید فرض ایده‌آل تلقی شود. تلفات VFD جداگانه محاسبه نمی‌شود.

## 9. Worked power example | مثال عددی توان
Given Q=50 m³/h, TDH=40 m, density=1000 kg/m³, pump efficiency=78%, motor efficiency=92%:
- Q=50/3600=0.013889 m³/s
- Ph=1000×9.80665×0.013889×40/1000≈5.45 kW
- Pshaft=5.45/0.78≈6.99 kW
- Pelectric=6.99/0.92≈7.60 kW

خروجی نهایی: توان هیدرولیکی ۵٫۴۵، توان محور ۶٫۹۹ و توان الکتریکی ورودی حدود ۷٫۶۰ کیلووات. مقدار FINAL REQUIRED ELECTRICAL POWER همان توان الکتریکی ورودی موتور است.

## 10. Pump curve workflow | ورود منحنی پمپ
Enter the number of points (2–30). For each point, enter flow and head; efficiency and shaft power are optional. Flow values must be unique. Points are sorted by flow and linearly interpolated only within the entered range. No extrapolation is performed. Motor efficiency is entered separately.

تعداد نقاط (۲ تا ۳۰) را وارد کنید. برای هر نقطه دبی و هد الزامی و راندمان و توان محور اختیاری است. دبی‌ها تکراری نباشند. نقاط بر اساس دبی مرتب و فقط در محدوده داده‌ها درون‌یابی می‌شوند. برون‌یابی وجود ندارد و راندمان موتور جداگانه وارد می‌شود.

The comparison of interpolated pump head with calculated system TDH at the requested flow is only a pointwise check. The actual operating point requires the intersection of the pump curve and the system curve; this version does not solve that intersection automatically.

مقایسه هد پمپ در دبی موردنظر با TDH سیستم صرفاً کنترل نقطه‌ای است. نقطه کار واقعی از تقاطع منحنی پمپ و منحنی سیستم به دست می‌آید و نسخه فعلی این تقاطع را خودکار حل نمی‌کند.

## 11. Worked example: reading the result | تفسیر خروجی
If the report shows TDH=40 m and the power calculation above, 7.60 kW is the estimated electrical input at the specified duty point. It is not, by itself, the final motor nameplate selection. Check the manufacturer's shaft-power curve over the full operating range, starting conditions, service factor, motor efficiency at load, VFD losses and supplier recommendations.

اگر گزارش TDH=40 متر و توان برق ۷٫۶۰ کیلووات را نشان دهد، این عدد توان ورودی تخمینی در نقطه کاری بررسی‌شده است؛ به‌تنهایی انتخاب قطعی توان نامی موتور نیست. منحنی توان محور در کل محدوده، راه‌اندازی، ضریب سرویس، راندمان موتور در بار، تلفات VFD و توصیه سازنده را کنترل کنید.

## 12. Limitations | محدودیت‌ها
Single steady-state flow path and one reference diameter for fitting losses. No branched network, multiple-pump solver, automatic pump/system intersection, NPSH, water hammer or VFD loss model. Fluid properties and some pipe data are approximate references. Validate equipment pressure drops and actual fluid properties for final engineering.

محاسبه تک‌مسیره و پایاست و برای افت فیتینگ‌ها یک قطر مرجع دارد. شبکه شاخه‌دار، حل پمپ‌های متعدد، تقاطع خودکار منحنی‌ها، NPSH، ضربه قوچ و مدل تلفات VFD وجود ندارد. خواص سیال و برخی داده‌های لوله تقریبی‌اند. برای طراحی نهایی خواص واقعی سیال و افت تجهیزات را تأیید کنید.

## 13. Tests | آزمون‌ها
```bash
python -m unittest discover -s tests -v
```
