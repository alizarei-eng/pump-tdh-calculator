# Pump TDH Calculator

## فارسی

### معرفی
این برنامه TDH موردنیاز پمپ را برای یک مسیر جریان پایا بین دو مرز مشخص محاسبه می‌کند. پس از محاسبه TDH غیرمنفی، محاسبه توان هیدرولیکی، توان محور و توان برق ورودی به‌صورت خودکار اجرا می‌شود؛ بنابراین برای دریافت نتیجه اولیه نیازی به اطلاعات پلاک یا منحنی پمپ نیست.

### قابلیت‌ها
- محاسبه اختلاف ارتفاع با دو روش
- انتخاب هندسه لوله و محاسبه قطر داخلی اسمی
- محاسبه افت طولی و موضعی
- افزودن افت فشار تجهیزات
- محاسبه هد فشار و هد سرعت مرزی
- محاسبه خودکار توان پس از محاسبه TDH
- ورود اختیاری راندمان پمپ و موتور
- ورود اختیاری ۲ تا ۳۰ نقطه منحنی پمپ و درون‌یابی در محدوده داده‌ها

### اجرا
```bash
git clone https://github.com/alizarei-eng/pump-tdh-calculator.git
cd pump-tdh-calculator
python main.py
python -m unittest discover -s tests -v
```

### معادله TDH
`TDH=Δz+Δ(P/ρg)+Δ(V²/2g)+hf+hm+hequipment`

### منطق محاسبه توان
پس از نمایش TDH، برنامه به‌طور خودکار وارد بخش توان می‌شود:
- روش ۱: ورود جداگانه راندمان پمپ و موتور. برای هر مقدار خالی، راندمان ۱۰۰٪ فرض می‌شود.
- روش ۲: ورود ۲ تا ۳۰ نقطه منحنی پمپ. دبی و هد الزامی و راندمان پمپ و توان محور اختیاری‌اند.
- روش ۳: فرض راندمان ۱۰۰٪ برای پمپ و موتور.
- با فشردن Enter در انتخاب روش، روش ۳ به‌صورت پیش‌فرض اجرا می‌شود؛ بنابراین کاربر بدون داشتن اطلاعات پمپ نیز نتیجه اولیه توان را دریافت می‌کند.

راندمان ۱۰۰٪ یک فرض ایده‌آل و حد پایین نظری توان است، نه راندمان واقعی تجهیز. توان برق واقعی معمولاً بیشتر است. اگر راندمان واقعی در دسترس باشد، ورود آن تخمین را به شرایط واقعی نزدیک‌تر می‌کند.

### مثال
برای دبی ۵۰ m³/h، TDH برابر ۴۰ m، چگالی ۱۰۰۰ kg/m³، راندمان پمپ ۷۸٪ و موتور ۹۲٪، توان هیدرولیکی حدود ۵٫۴۵ kW، توان محور ۶٫۹۹ kW و توان برق ورودی ۷٫۶۰ kW است.

### موارد کاربرد
انتقال بین دو مخزن یا یک مسیر خروجی پمپ، تخمین TDH با داشتن ارتفاع و افت‌های مسیر، و تخمین توان در یک نقطه کاری مشخص.

### محدودیت‌ها
هر محاسبه یک دبی و یک قطر مرجع دارد. چند قطر، شبکه شاخه‌دار، مسیر موازی و پمپ‌های سری/موازی خودکار حل نمی‌شوند. تقاطع منحنی پمپ و سیستم، NPSH، کاویتاسیون، ضربه قوچ، تلفات VFD و راه‌اندازی موتور بررسی نمی‌شوند. مقایسه هد منحنی پمپ با TDH به‌تنهایی نقطه کار واقعی را حل نمی‌کند. توان برق محاسبه‌شده با راندمان‌های فرضی ۱۰۰٪، مقدار واقعی مصرف نیست و به‌تنهایی مبنای انتخاب توان نامی موتور قرار نمی‌گیرد.

راهنماهای TDH، هد استاتیکی و توان در پوشه docs قرار دارند.

## English

### Overview
This application calculates pump TDH for one steady-flow path between two defined boundaries. After a non-negative TDH is calculated, hydraulic, shaft and electrical input power are calculated automatically. Pump nameplate or curve data is not required for the initial power estimate.

### Features
- Elevation difference using two input methods
- Pipe geometry selection and nominal internal-diameter calculation
- Major and minor loss calculations
- Equipment pressure-drop inputs
- Boundary pressure-head and velocity-head terms
- Automatic power calculation after TDH
- Optional pump and motor efficiency inputs
- Optional entry of 2–30 pump-curve points with interpolation within the supplied range

### Run
```bash
git clone https://github.com/alizarei-eng/pump-tdh-calculator.git
cd pump-tdh-calculator
python main.py
python -m unittest discover -s tests -v
```

### TDH equation
`TDH=Δz+Δ(P/ρg)+Δ(V²/2g)+hf+hm+hequipment`

### Power-calculation workflow
After displaying TDH, the application enters the power section automatically:
- Method 1: enter pump and motor efficiencies separately. Each blank value defaults to 100%.
- Method 2: enter 2–30 pump-curve points. Flow and head are required; pump efficiency and shaft power are optional.
- Method 3: assume 100% efficiency for both pump and motor.
- Pressing Enter at the method prompt selects Method 3 by default, so an initial power estimate is produced even when pump data is unavailable.

A 100% efficiency assumption is idealized and represents a theoretical lower bound, not actual equipment efficiency. Actual electrical input will normally be higher. Entering known efficiencies improves the estimate.

### Worked example
For a flow rate of 50 m³/h, TDH of 40 m, density of 1000 kg/m³, pump efficiency of 78% and motor efficiency of 92%, hydraulic power is approximately 5.45 kW, shaft power 6.99 kW and electrical input 7.60 kW.

### Suitable applications
Tank-to-tank transfer, a single pump discharge route, TDH estimation with known route losses, and power estimation at a defined duty point.

### Limitations
Each calculation uses one flow rate and one reference diameter. Multiple diameters, branched networks, parallel paths and series/parallel pump systems are not solved automatically. Pump/system curve intersection, NPSH, cavitation, water hammer, VFD losses and motor starting are not evaluated. Comparing pump-curve head with system TDH alone does not solve the actual operating point. Power calculated with assumed 100% efficiencies is not actual consumption and must not be used alone for motor nameplate selection.

Detailed TDH, static-head and power guides are available in the docs directory.
