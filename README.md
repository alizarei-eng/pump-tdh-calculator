# Pump TDH Calculator | محاسبه‌گر هد کل پمپ

**FA:** ابزار خط فرمان Python برای تخمین خواص سیال، محاسبه هد کل دینامیکی موردنیاز پمپ (TDH) و برآورد توان هیدرولیکی، توان محور و توان الکتریکی ورودی موتور در یک مسیر جریان پایا.

**EN:** A Python command-line tool for screening fluid properties, calculating pump Total Dynamic Head (TDH), and estimating hydraulic, pump-shaft and motor electrical input power for a steady single-flow path.

## Features | قابلیت‌ها
- EC-based screening estimates; EC and operating temperature are independent inputs | تخمین خواص از EC؛ EC و دمای کارکرد مستقل‌اند
- HDPE grade → SDR → OD selection and nominal ID calculation | انتخاب گرید، SDR و OD و محاسبه ID اسمی HDPE
- Automatic pipe roughness lookup | بارگذاری خودکار زبری
- Static head by Δz or start/end elevations | هد استاتیکی با اختلاف ارتفاع یا تراز ابتدا و انتها
- Darcy–Weisbach major loss and K-based fitting loss | افت طولی Darcy و افت موضعی K
- Equipment pressure-drop input | ورود افت فشار واقعی تجهیزات
- Boundary pressure and velocity-head terms | مؤلفه هد فشار و سرعت در مرزها
- Manual efficiencies, staged pump-curve entry, or 100% ideal default | راندمان دستی، ورود مرحله‌ای منحنی یا فرض ۱۰۰٪
- Linear interpolation within pump-curve data range | درون‌یابی خطی فقط داخل محدوده داده‌های منحنی

## Installation and run | نصب و اجرا
```bash
git clone https://github.com/alizarei-eng/pump-tdh-calculator.git
cd pump-tdh-calculator
python main.py
python -m unittest discover -s tests -v
```

## Workflow | مراحل کار
1. Enter EC compensated to 25°C, select fluid profile, and enter actual operating temperature. | ورود EC جبران‌شده، پروفایل سیال و دمای واقعی
2. Select static-head method: direct Δz or elevations z1 and z2. | انتخاب روش هد استاتیکی
3. Select pipe material. For HDPE choose grade, SDR and OD; for other materials enter OD and nominal wall thickness. | انتخاب جنس؛ برای HDPE گرید/SDR/OD و برای سایر مواد OD و ضخامت
4. Enter flow and pipe length. | ورود دبی و طول
5. Add fitting/valve types and quantities. | ورود فیتینگ‌ها و تعداد
6. Add equipment pressure drops at the operating flow. | ورود افت فشار تجهیزات در دبی کاری
7. Enter boundary pressures and boundary velocities where required. | ورود فشار و سرعت مرزی
8. Review TDH components. | بررسی اجزای TDH
9. Optionally calculate pump and motor power. | در صورت نیاز محاسبه توان

## TDH equation | معادله TDH
`TDH = Δz + Δ(P/ρg) + Δ(V²/2g) + hf + hm,fittings + hequipment`

The signs and reference sections matter. For two open reservoirs, boundary gauge pressures are normally zero and free-surface velocities are approximately zero. Static elevation is destination minus origin.

علامت مؤلفه‌ها و تعریف مقاطع ابتدا و انتها مهم است. برای دو مخزن باز، فشار گیج مرزی معمولاً صفر و سرعت سطح آزاد مخازن بزرگ تقریباً صفر است. اختلاف ارتفاع برابر تراز مقصد منهای مبدأ است.

## Power equations | روابط توان
`Ph = ρgQH/1000` kW when Q is in m³/s and H in m.

`Pshaft = Ph/ηpump`; `Pelectric = Pshaft/ηmotor`.

If efficiencies are unknown and left blank, the current program assumes 100%. This is an ideal theoretical assumption, not actual equipment efficiency or a reliable motor-sizing value.

اگر راندمان خالی بماند، برنامه ۱۰۰٪ فرض می‌کند. این فرض ایده‌آل است و نباید به‌عنوان راندمان واقعی یا مبنای قطعی انتخاب موتور تلقی شود.

## Worked end-to-end example | مثال از ابتدا تا انتها
Assume the hydraulic calculation has Q=50 m³/h, TDH=40 m, and density=1000 kg/m³. Choose manual efficiencies ηpump=0.78 and ηmotor=0.92.

`Q = 50/3600 = 0.013889 m³/s`

`Ph = 1000×9.80665×0.013889×40/1000 ≈ 5.45 kW`

`Pshaft = 5.45/0.78 ≈ 6.99 kW`

`Pelectric = 6.99/0.92 ≈ 7.60 kW`

Expected summary:
| Quantity | Approximate result |
|---|---:|
| Hydraulic power | 5.45 kW |
| Pump shaft power | 6.99 kW |
| Electrical input power | 7.60 kW |
| FINAL REQUIRED ELECTRICAL POWER | 7.60 kW |

**تفسیر فارسی:** با دبی ۵۰ مترمکعب بر ساعت، TDH برابر ۴۰ متر، چگالی ۱۰۰۰، راندمان پمپ ۷۸٪ و موتور ۹۲٪، توان هیدرولیکی حدود ۵٫۴۵، توان محور ۶٫۹۹ و توان برق ورودی حدود ۷٫۶۰ کیلووات است. مقدار توان نهایی همان Electrical Input Power است.

## Pump curve input | ورود مرحله‌ای منحنی پمپ
Enter 2–30 points. For each point, flow and head are required; pump efficiency and shaft power are optional. Flow values must be unique. The program sorts points and linearly interpolates only between available points; it does not extrapolate. Motor efficiency is entered separately. Comparing pump head with system TDH at the requested flow is not a full pump/system operating-point solution.

۲ تا ۳۰ نقطه وارد کنید. دبی و هد هر نقطه الزامی و راندمان پمپ و توان محور اختیاری‌اند. دبی‌ها باید یکتا باشند. برنامه نقاط را مرتب و فقط در محدوده داده‌ها درون‌یابی می‌کند؛ برون‌یابی ندارد. راندمان موتور جداگانه وارد می‌شود. مقایسه هد پمپ و TDH در دبی درخواستی، حل کامل نقطه کار واقعی نیست.

## Engineering limitations | محدودیت‌ها
Single steady flow path, one reference pipe diameter for fitting K calculations, approximate EC-based properties and reference roughness. No branched network solver, multiple-pump system solver, automatic pump/system curve intersection, NPSH analysis, VFD losses or water-hammer analysis. Equipment pressure drops must be actual/manufacturer values at the relevant flow.

محاسبه تک‌مسیره و پایاست؛ برای K فیتینگ‌ها یک قطر مرجع استفاده می‌شود؛ خواص EC و زبری تقریبی/مرجع‌اند. شبکه شاخه‌دار، پمپ‌های سری/موازی، تقاطع خودکار منحنی‌ها، NPSH، تلفات VFD و ضربه قوچ در نسخه فعلی وجود ندارند. افت تجهیزات باید در دبی مربوطه از اندازه‌گیری یا سازنده گرفته شود.

See [the bilingual engineering guide](docs/ENGINEERING_GUIDE_FA_EN.md) and the detailed topic guides in `docs/`.

## Suitable applications | موارد کاربرد مناسب
- **EN:** Preliminary or operational TDH estimation for one defined, steady-state flow path between two system boundaries.
- **FA:** تخمین اولیه یا عملیاتی TDH برای یک مسیر جریان پایا و مشخص بین دو مرز سیستم.
- **EN:** Systems where one representative pipe diameter and one flow rate can reasonably represent the pipe route used in the calculation.
- **FA:** سیستم‌هایی که یک قطر مرجع و یک دبی بتواند مسیر لوله مورد محاسبه را به‌طور معقول نمایندگی کند.
- **EN:** Adding static elevation, boundary pressure and velocity-head differences, straight-pipe friction, fitting K losses and measured/manufacturer equipment pressure drops.
- **FA:** ترکیب اختلاف ارتفاع، فشار و هد سرعت مرزی، افت طولی، افت K اتصالات و افت فشار واقعی/سازنده تجهیزات.
- **EN:** Estimating hydraulic, shaft and motor electrical input power at the calculated duty point when credible efficiencies or manufacturer curve data are available.
- **FA:** تخمین توان هیدرولیکی، توان محور و توان برق ورودی موتور در نقطه محاسباتی، در صورت وجود راندمان معتبر یا داده منحنی سازنده.

## Engineering scope and limitations | محدوده مهندسی و محدودیت‌ها
**What one calculation represents | مفهوم یک محاسبه**
- One steady flow rate and one reference pipe internal diameter for the pipe-friction and fitting-loss calculation. | یک دبی پایا و یک قطر داخلی مرجع برای افت طولی و افت اتصالات.
- Fitting K values are all evaluated using the reference pipe velocity. | تمام ضرایب K با سرعت لوله مرجع محاسبه می‌شوند.
- Equipment pressure drops are entered as measured or manufacturer differential pressure at the relevant flow; the selected equipment values are added. | افت فشار تجهیزات به‌صورت اختلاف فشار اندازه‌گیری‌شده یا سازنده در دبی مربوط وارد و با هم جمع می‌شود.
- Boundary pressures and velocities must describe the actual start and end sections of the system. | فشارها و سرعت‌های مرزی باید مقاطع واقعی ابتدا و انتهای سیستم را توصیف کنند.

**Not covered by this tool | موارد خارج از محدوده**
- No automatic solution for multiple pipe diameters/segments, branched networks, parallel paths or flow distribution. | حل خودکار چند قطر/بخش لوله، شبکه شاخه‌دار، مسیرهای موازی یا توزیع دبی وجود ندارد.
- No multiple-pump series/parallel system solver or automatic pump-curve/system-curve intersection. | حل پمپ‌های سری/موازی یا تقاطع خودکار منحنی پمپ و سیستم وجود ندارد.
- Pump-curve data are linearly interpolated only within the entered flow range; no extrapolation or full operating-point solution is performed. | داده منحنی پمپ فقط در محدوده دبی واردشده درون‌یابی خطی می‌شوند؛ برون‌یابی یا حل کامل نقطه کار انجام نمی‌شود.
- No NPSH, cavitation margin, water hammer, transient, VFD-loss or motor-starting analysis. | تحلیل NPSH، حاشیه کاویتاسیون، ضربه قوچ، گذرا، تلفات VFD یا راه‌اندازی موتور وجود ندارد.
- EC-based density/viscosity and reference roughness are estimates; equipment pressure drop must match the operating flow and condition. | چگالی/ویسکوزیته مبتنی بر EC و زبری مرجع تخمینی‌اند؛ افت فشار تجهیز باید با دبی و وضعیت کاری منطبق باشد.
- A 100% efficiency default is an idealized theoretical lower bound, not actual pump or motor performance. | راندمان پیش‌فرض ۱۰۰٪ فرض ایده‌آل و حد پایین نظری است، نه عملکرد واقعی پمپ یا موتور.

**Practical rule | قاعده عملی:** Use this tool for a single-path TDH estimate and preliminary power check. For a route with changing diameters, calculate each segment and fitting group at its own diameter/velocity before assembling the energy balance, or use a network-capable model. For final pump selection, solve the pump/system operating point and verify NPSH, motor loading and transient conditions separately.
