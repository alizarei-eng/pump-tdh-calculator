# Pump TDH Calculator

## فارسی

### معرفی
این برنامه TDH موردنیاز پمپ را برای یک مسیر جریان پایا بین دو مرز مشخص محاسبه می‌کند و سپس امکان تخمین توان هیدرولیکی، توان محور و توان برق ورودی را فراهم می‌سازد.

### قابلیت‌ها
- محاسبه اختلاف ارتفاع با دو روش
- انتخاب هندسه لوله و محاسبه قطر داخلی اسمی
- محاسبه افت طولی و موضعی
- افزودن افت فشار تجهیزات بر اساس داده ورودی
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
فرض کنید دبی ۵۰ m³/h، اختلاف ارتفاع ۲۵ m و افت‌های لوله، اتصالات و تجهیزات معلوم باشند. برنامه تمام مؤلفه‌ها را به هد تبدیل و جمع می‌کند. اگر TDH نهایی ۴۰ m، چگالی ۱۰۰۰ kg/m³، راندمان پمپ ۷۸٪ و موتور ۹۲٪ باشد، توان هیدرولیکی حدود ۵٫۴۵ kW، توان محور ۶٫۹۹ kW و توان برق ورودی ۷٫۶۰ kW است.

### موارد کاربرد
- انتقال بین دو مخزن یا یک مسیر خروجی پمپ
- تخمین TDH با داشتن ارتفاع، فشار مرزی، مشخصات لوله و افت تجهیزات
- تخمین توان در یک نقطه کاری مشخص با داده معتبر راندمان
- مقایسه سناریوهای یک مسیر منفرد

### محدودیت‌ها
برنامه در هر محاسبه یک دبی و یک قطر مرجع دارد و چند قطر را خودکار به هم متصل نمی‌کند. شبکه شاخه‌دار، مسیرهای موازی، پمپ‌های سری و موازی و توزیع دبی حل نمی‌شوند. منحنی سیستم و نقطه تقاطع آن با منحنی پمپ به‌صورت خودکار محاسبه نمی‌شوند. درون‌یابی منحنی پمپ خطی و محدود به بازه داده‌هاست. NPSH، کاویتاسیون، ضربه قوچ، تلفات VFD و شرایط راه‌اندازی موتور بررسی نمی‌شوند. راندمان ۱۰۰٪ فقط فرض ایده‌آل است.

### مستندات تکمیلی
راهنمای TDH، هد استاتیکی و توان در پوشه docs قرار دارند.

---

## English

### Overview
This application calculates the pump TDH for one steady-flow path between two defined boundaries. It can then estimate hydraulic power, shaft power and electrical input power.

### Features
- Static elevation difference using two input methods
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
Assume a flow rate of 50 m³/h, an elevation difference of 25 m, and known pipe, fitting and equipment losses. The program converts the terms to head and sums them. If final TDH is 40 m, density is 1000 kg/m³, pump efficiency is 78% and motor efficiency is 92%, hydraulic power is approximately 5.45 kW, shaft power 6.99 kW and electrical input 7.60 kW.

### Suitable applications
- Transfer between two tanks or a single pump discharge route
- TDH estimates when elevation, boundary pressure, pipe data and equipment losses are known
- Power estimates at a defined duty point with credible efficiency data
- Comparing scenarios for a single flow path

### Limitations
Each calculation uses one flow rate and one reference diameter; multiple diameters are not assembled automatically. Branched networks, parallel paths, flow distribution and series/parallel pump systems are not solved. The system curve and its intersection with the pump curve are not calculated automatically. Pump-curve interpolation is linear and limited to entered data. NPSH, cavitation, water hammer, VFD losses and motor starting conditions are not evaluated. A 100% efficiency assumption is idealized only.

### Additional documentation
Detailed TDH, static-head and power guides are available in the docs directory.
