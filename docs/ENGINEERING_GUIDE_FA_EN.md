# راهنمای مهندسی محاسبه‌گر TDH پمپ

## بخش فارسی

این برنامه TDH یک مسیر پایا را بین دو مرز سیستم محاسبه می‌کند.

### معادله
`TDH=Δz+Δ(P/ρg)+Δ(V²/2g)+hf+hm+hequipment`

### مثال
پمپ ۵۰ m³/h آب را به مقصدی با اختلاف ارتفاع ۲۵ m منتقل می‌کند. افت لوله، اتصالات و فیلتر نیز به هد تبدیل و با اختلاف ارتفاع جمع می‌شوند. اگر TDH نهایی ۴۰ m، چگالی ۱۰۰۰ kg/m³، راندمان پمپ ۷۸٪ و موتور ۹۲٪ باشد، توان هیدرولیکی ۵٫۴۵ kW، توان محور ۶٫۹۹ kW و توان برق ورودی ۷٫۶۰ kW خواهد بود.

### کاربردها
انتقال بین دو مخزن، مسیر منفرد پمپ، تخمین TDH با افت تجهیزات معلوم و تخمین توان در نقطه کاری مشخص.

### محدودیت‌ها
یک دبی و یک قطر مرجع در هر محاسبه استفاده می‌شود. چند قطر، شبکه شاخه‌دار، مسیر موازی و پمپ‌های سری/موازی خودکار حل نمی‌شوند. تقاطع منحنی پمپ و سیستم، NPSH، کاویتاسیون، ضربه قوچ، تلفات VFD و راه‌اندازی موتور بررسی نمی‌شوند. راندمان ۱۰۰٪ فرض ایده‌آل است.

## English Section

This application calculates TDH for one steady-flow path between two system boundaries.

### Equation
`TDH=Δz+Δ(P/ρg)+Δ(V²/2g)+hf+hm+hequipment`

### Worked example
A pump transfers 50 m³/h to a destination 25 m higher. Pipe, fitting and filter losses are converted to head and added to the elevation term. If final TDH is 40 m, density is 1000 kg/m³, pump efficiency is 78% and motor efficiency is 92%, hydraulic power is 5.45 kW, shaft power 6.99 kW and electrical input 7.60 kW.

### Suitable applications
Tank-to-tank transfer, a single pump route, TDH estimation with known equipment losses, and power estimation at a defined duty point.

### Limitations
Each calculation uses one flow rate and one reference diameter. Multiple diameters, branched networks, parallel paths and series/parallel pumps are not solved automatically. Pump/system curve intersection, NPSH, cavitation, water hammer, VFD losses and motor starting are not evaluated. 100% efficiency is an idealized assumption.
