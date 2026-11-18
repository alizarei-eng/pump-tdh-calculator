# محاسبه توان پمپ و موتور

## بخش فارسی

### رفتار برنامه
پس از محاسبه TDH، اگر مقدار TDH غیرمنفی باشد، برنامه بدون پرسش بله/خیر وارد بخش محاسبه توان می‌شود. در نتیجه حتی اگر کاربر هیچ اطلاعاتی از پمپ نداشته باشد، می‌تواند با فشردن Enter در انتخاب روش، محاسبه اولیه را دریافت کند.

### روش‌های ورود اطلاعات
۱. **راندمان دستی:** راندمان پمپ و موتور را جداگانه بر حسب درصد وارد کنید. اگر هرکدام خالی بماند، همان راندمان ۱۰۰٪ فرض می‌شود؛ خالی گذاشتن یکی، محاسبه را متوقف نمی‌کند.

۲. **منحنی پمپ:** ۲ تا ۳۰ نقطه وارد کنید. دبی و هد هر نقطه الزامی است؛ راندمان پمپ و توان محور اختیاری‌اند. برنامه فقط در محدوده دبی نقاط واردشده درون‌یابی خطی انجام می‌دهد و برون‌یابی نمی‌کند. راندمان موتور در این روش جداگانه پرسیده می‌شود و در صورت خالی ماندن، ۱۰۰٪ فرض می‌شود.

۳. **فرض ایده‌آل:** راندمان پمپ و موتور هر دو ۱۰۰٪ در نظر گرفته می‌شوند. این روش، پیش‌فرض برنامه است؛ کافی است در سؤال انتخاب روش Enter بزنید.

### روابط
`Ph=ρgQH`

`Pshaft=Ph/ηpump`

`Pelectric=Pshaft/ηmotor`

در این روابط، Q بر حسب m³/s، هد بر حسب متر و راندمان‌ها به‌صورت عدد اعشاری هستند. هر سه خروجی توان (هیدرولیکی، محور و برق ورودی) هم بر حسب kW و هم بر حسب اسب بخار مکانیکی (hp) نمایش داده می‌شوند. ضریب تبدیل برنامه برابر است با `hp = kW × 1.34102209`.

### تفسیر نتایج
- **توان هیدرولیکی:** توانی که به سیال منتقل می‌شود و از دبی، چگالی و TDH به دست می‌آید.
- **توان محور:** توان مکانیکی موردنیاز در محور پمپ با لحاظ راندمان پمپ.
- **توان برق ورودی:** توان الکتریکی موردنیاز با لحاظ راندمان موتور.

اگر هر دو راندمان ۱۰۰٪ باشند، هر سه مقدار برابر می‌شوند. این برابری فقط نتیجه فرض ایده‌آل است؛ مصرف واقعی معمولاً بیشتر خواهد بود. توان برق تخمینی را نباید بدون بررسی شرایط کاری، ضریب سرویس، شرایط محیطی و الزامات سازنده مبنای انتخاب نهایی موتور قرار داد.

### مثال
برای Q=50 m³/h، TDH=40 m، چگالی ۱۰۰۰ kg/m³، راندمان پمپ ۷۸٪ و موتور ۹۲٪:
- توان هیدرولیکی ≈ ۵٫۴۵ kW
- توان محور ≈ ۶٫۹۹ kW
- توان برق ورودی ≈ ۷٫۶۰ kW

### محدودیت‌ها
درون‌یابی منحنی خطی و فقط داخل محدوده دبی ورودی است. نقطه کار واقعی از تقاطع منحنی پمپ و سیستم محاسبه نمی‌شود. تلفات VFD، شرایط راه‌اندازی، NPSH و ضربه قوچ لحاظ نمی‌شوند. اگر TDH منفی باشد، این محاسبه توان پمپ اجرا نمی‌شود؛ زیرا شرایط مرزی ممکن است نشان‌دهنده جریان رانشی یا نیازمند بازبینی تعریف سیستم باشد. توان برق ورودی به‌تنهایی انتخاب توان نامی موتور نیست.

## English Section

### Application behavior
After TDH is calculated, the application enters the power-calculation section automatically whenever TDH is non-negative. The user can therefore obtain an initial estimate without pump data by pressing Enter at the method-selection prompt.

### Input methods
1. **Manual efficiencies:** enter pump and motor efficiencies separately as percentages. If either value is left blank, that efficiency alone defaults to 100%; leaving one blank does not skip the calculation.

2. **Pump curve:** enter 2–30 points. Flow and head are required for each point; pump efficiency and shaft power are optional. Linear interpolation is performed only within the entered flow range; no extrapolation is made. Motor efficiency is requested separately and defaults to 100% if left blank.

3. **Idealized assumption:** both pump and motor efficiencies are set to 100%. This is the default method; press Enter at the method-selection prompt.

### Equations
`Ph=ρgQH`

`Pshaft=Ph/ηpump`

`Pelectric=Pshaft/ηmotor`

In these equations, Q is in m³/s, head is in metres, and efficiencies are decimal fractions. All three power outputs (hydraulic, shaft and electrical input) are displayed in both kW and mechanical horsepower (hp), using `hp = kW × 1.34102209`.

### Interpreting the results
- **Hydraulic power:** power transferred to the fluid, calculated from flow, density and TDH.
- **Shaft power:** mechanical power required at the pump shaft, accounting for pump efficiency.
- **Electrical input power:** electrical power required, accounting for motor efficiency.

If both efficiencies are 100%, all three values are equal. This is only an idealized assumption; actual consumption will normally be higher. Estimated electrical input must not be used alone for final motor selection without checking duty conditions, service factor, ambient conditions and manufacturer requirements.

### Worked example
For Q=50 m³/h, TDH=40 m, density=1000 kg/m³, pump efficiency=78% and motor efficiency=92%:
- Hydraulic power ≈ 5.45 kW
- Shaft power ≈ 6.99 kW
- Electrical input ≈ 7.60 kW

### Limitations
Curve interpolation is linear and only within the entered flow range. The actual duty point is not solved from pump/system curve intersection. VFD losses, starting conditions, NPSH and water hammer are not included. If TDH is negative, this pump-power calculation is not run because the boundary conditions may indicate a gravity-driven flow or a system definition that needs review. Electrical input power alone is not a motor nameplate selection.
