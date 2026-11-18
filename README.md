# Pump TDH Calculator

## فارسی

### معرفی
این برنامه TDH موردنیاز پمپ را برای یک مسیر جریان پایا بین دو مرز مشخص محاسبه می‌کند و امکان تخمین توان هیدرولیکی، توان محور و توان برق ورودی را فراهم می‌سازد.

### قابلیت‌ها
- محاسبه اختلاف ارتفاع با دو روش
- انتخاب هندسه لوله و محاسبه قطر داخلی اسمی
- محاسبه افت طولی و موضعی
- افزودن افت فشار تجهیزات
- محاسبه هد فشار و هد سرعت مرزی
- محاسبه TDH و توان پمپ و موتور
- ورود مرحله‌ای نقاط منحنی پمپ و درون‌یابی در محدوده داده‌ها

### اجرا
```bash
git clone https://github.com/alizarei-eng/pump-tdh-calculator.git
cd pump-tdh-calculator
python main.py
python -m unittest discover -s tests -v
```

### معادله TDH
`TDH=Δz+Δ(P/ρg)+Δ(V²/2g)+hf+hm+hequipment`

### مثال
برای دبی ۵۰ m³/h، TDH برابر ۴۰ m، چگالی ۱۰۰۰ kg/m³، راندمان پمپ ۷۸٪ و موتور ۹۲٪، توان هیدرولیکی حدود ۵٫۴۵ kW، توان محور ۶٫۹۹ kW و توان برق ورودی ۷٫۶۰ kW است.

### موارد کاربرد
انتقال بین دو مخزن یا یک مسیر خروجی پمپ، تخمین TDH با داشتن ارتفاع و افت‌های مسیر، و تخمین توان در یک نقطه کاری مشخص.

### محدودیت‌ها
هر محاسبه یک دبی و یک قطر مرجع دارد. چند قطر، شبکه شاخه‌دار، مسیر موازی و پمپ‌های سری/موازی خودکار حل نمی‌شوند. تقاطع منحنی پمپ و سیستم، NPSH، کاویتاسیون، ضربه قوچ، تلفات VFD و راه‌اندازی موتور بررسی نمی‌شوند. راندمان ۱۰۰٪ فقط فرض ایده‌آل است.

راهنماهای TDH، هد استاتیکی و توان در پوشه docs قرار دارند.

## English

### Overview
This application calculates pump TDH for one steady-flow path between two defined boundaries. It can also estimate hydraulic power, shaft power and electrical input power.

### Features
- Elevation difference using two input methods
- Pipe geometry selection and nominal internal-diameter calculation
- Major and minor loss calculations
- Equipment pressure-drop inputs
- Boundary pressure-head and velocity-head terms
- TDH and pump/motor power calculations
- Sequential pump-curve point entry and interpolation within the entered range

### Run
```bash
git clone https://github.com/alizarei-eng/pump-tdh-calculator.git
cd pump-tdh-calculator
python main.py
python -m unittest discover -s tests -v
```

### TDH equation
`TDH=Δz+Δ(P/ρg)+Δ(V²/2g)+hf+hm+hequipment`

### Worked example
For a flow rate of 50 m³/h, TDH of 40 m, density of 1000 kg/m³, pump efficiency of 78% and motor efficiency of 92%, hydraulic power is approximately 5.45 kW, shaft power 6.99 kW and electrical input 7.60 kW.

### Suitable applications
Tank-to-tank transfer, a single pump discharge route, TDH estimation with known route losses, and power estimation at a defined duty point.

### Limitations
Each calculation uses one flow rate and one reference diameter. Multiple diameters, branched networks, parallel paths and series/parallel pump systems are not solved automatically. Pump/system curve intersection, NPSH, cavitation, water hammer, VFD losses and motor starting are not evaluated. A 100% efficiency assumption is idealized only.

Detailed TDH, static-head and power guides are available in the docs directory.
