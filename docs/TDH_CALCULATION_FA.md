# Pump Total Dynamic Head (TDH) | محاسبه هد کل دینامیکی پمپ

## 1. Purpose and energy equation | هدف و معادله انرژی
**EN:** The application estimates the head a pump must add between two defined system boundaries for one steady-state flow path.

**FA:** برنامه هد موردنیاز پمپ را بین دو مرز مشخص سیستم و برای یک مسیر جریان پایا تخمین می‌زند.

`TDH = Δz + Δ(P/ρg) + Δ(V²/2g) + hf + hm,fittings + hequipment`

- Δz: destination elevation minus source elevation. | اختلاف تراز مقصد منهای مبدأ.
- Δ(P/ρg): pressure-head difference at the two boundaries. | اختلاف هد فشار در دو مرز.
- Δ(V²/2g): boundary velocity-head difference. | اختلاف هد سرعت دو مرز.
- hf: Darcy–Weisbach straight-pipe friction. | افت طولی Darcy–Weisbach.
- hm: fitting and valve loss from K values. | افت اتصالات و شیرها با ضرایب K.
- hequipment: measured/manufacturer equipment pressure drop converted to fluid head. | افت فشار واقعی/سازنده تجهیزات تبدیل‌شده به هد سیال.

## 2. Pipe geometry | هندسه لوله
For HDPE, select grade → SDR → OD. Nominal wall thickness is read from the database and nominal ID is calculated as `ID=OD−2e`. For other listed materials, enter OD and nominal wall thickness; the program calculates ID. Reference roughness is loaded from the material database.

برای HDPE گرید ← SDR ← OD انتخاب می‌شود؛ ضخامت اسمی از بانک خوانده و ID اسمی محاسبه می‌شود. برای سایر مواد OD و ضخامت اسمی وارد می‌شود. زبری مرجع از بانک جنس لوله بارگذاری می‌شود.

## 3. Fluid properties | خواص سیال
EC must already be compensated to 25°C and is entered separately from actual operating temperature. TDS, density and viscosity are approximate screening estimates. The generic profile does not infer individual ions; the natural-seawater profile assumes standard natural-seawater ionic ratios.

EC باید از قبل به ۲۵ درجه جبران شده باشد و از دمای واقعی کارکرد جداگانه وارد می‌شود. TDS، چگالی و ویسکوزیته تخمینی‌اند. پروفایل عمومی یون‌های منفرد را استنتاج نمی‌کند؛ پروفایل آب دریا نسبت‌های استاندارد آب دریای طبیعی را فرض می‌کند.

## 4. Equipment and fittings | تجهیزات و اتصالات
Fitting K values are approximate references. In the current implementation, all selected K values use the velocity calculated from the single reference pipe diameter. Equipment pressure drops are entered in bar and converted to head using the estimated fluid density. Enter each equipment drop at the flow rate relevant to the system calculation.

ضرایب K اتصالات تقریبی‌اند. در نسخه فعلی همه Kها با سرعت محاسبه‌شده از یک قطر مرجع اعمال می‌شوند. افت فشار تجهیزات بر حسب bar وارد و با چگالی تخمینی به هد تبدیل می‌شود. افت هر تجهیز باید مربوط به دبی محاسباتی باشد.

## 5. Power calculation | محاسبه توان
`Ph=ρgQH/1000` kW, where Q is m³/s and H is m.
`Pshaft=Ph/ηpump`
`Pelectric=Pshaft/ηmotor`

The CLI accepts efficiencies as percentages. Blank efficiencies default to 100%, an idealized theoretical assumption. Manufacturer shaft-power data can be entered through pump-curve points; if available, the interpolated shaft power is used. The program does not include VFD losses.

برنامه راندمان را به‌صورت درصد دریافت می‌کند. ورودی خالی برابر فرض ۱۰۰٪ است؛ یعنی فرض ایده‌آل نظری. توان محور سازنده را می‌توان در نقاط منحنی وارد کرد و در صورت امکان درون‌یابی می‌شود. تلفات VFD محاسبه نمی‌شود.

## 6. Pump curve | منحنی پمپ
Enter 2–30 points. Flow and head are required; pump efficiency and shaft power are optional. Flow values must be unique. Linear interpolation is performed only within the entered flow range; no extrapolation is made. The motor efficiency is entered separately.

۲ تا ۳۰ نقطه وارد کنید. دبی و هد الزامی و راندمان پمپ و توان محور اختیاری‌اند. دبی‌ها باید یکتا باشند. درون‌یابی خطی فقط داخل محدوده دبی‌های واردشده انجام می‌شود و برون‌یابی وجود ندارد. راندمان موتور جداگانه وارد می‌شود.

Comparing pump head and system TDH at the requested flow is not a full operating-point solution. The operating point requires the intersection of the pump curve and the system curve; the current version does not solve it automatically.

مقایسه هد پمپ با TDH در دبی موردنظر حل نقطه کار واقعی نیست. نقطه کار از تقاطع منحنی پمپ و منحنی سیستم به دست می‌آید و نسخه فعلی آن را خودکار حل نمی‌کند.

## 7. Suitable applications | موارد کاربرد مناسب
- **EN:** One steady flow path with one representative flow and pipe diameter, such as a transfer line between two tanks or a single pump discharge route.
- **FA:** یک مسیر جریان پایا با یک دبی و قطر مرجع؛ مانند خط انتقال بین دو مخزن یا مسیر خروجی یک پمپ.
- **EN:** Preliminary TDH estimation when elevations, boundary pressures, pipe length, fittings and equipment differential pressures are known.
- **FA:** تخمین اولیه TDH زمانی که ارتفاع‌ها، فشارهای مرزی، طول لوله، اتصالات و افت فشار تجهیزات مشخص‌اند.
- **EN:** Preliminary power estimation at a defined duty point when credible efficiency or manufacturer curve data are available.
- **FA:** تخمین اولیه توان در نقطه کاری مشخص، در صورت وجود راندمان معتبر یا داده منحنی سازنده.

## 8. Limitations and decision boundary | محدودیت‌ها و مرز استفاده
- One calculation uses one flow and one reference internal diameter. Multiple diameters/segments are not assembled automatically. | هر محاسبه یک دبی و یک قطر داخلی مرجع دارد؛ چند قطر/بخش خودکار به هم متصل نمی‌شوند.
- All fitting K values use the same reference velocity. Fittings on other diameters must be calculated separately at their local velocities. | همه Kها با سرعت مرجع مشترک محاسبه می‌شوند؛ اتصالات روی قطرهای دیگر باید جداگانه با سرعت محلی محاسبه شوند.
- No branched network, parallel flow paths, flow distribution or multiple-pump series/parallel solver. | شبکه شاخه‌دار، مسیرهای موازی، توزیع دبی یا حل پمپ‌های سری/موازی وجود ندارد.
- No automatic system-curve construction or pump/system intersection. | ساخت خودکار منحنی سیستم یا تقاطع منحنی پمپ و سیستم وجود ندارد.
- No NPSH, cavitation, water hammer, transient, VFD-loss or motor-starting analysis. | تحلیل NPSH، کاویتاسیون، ضربه قوچ، گذرا، تلفات VFD یا راه‌اندازی موتور وجود ندارد.
- EC properties and reference roughness are estimates. Equipment pressure drop must match the relevant flow and equipment condition. | خواص مبتنی بر EC و زبری مرجع تخمینی‌اند. افت تجهیز باید با دبی و وضعیت واقعی آن منطبق باشد.
- 100% efficiency is not actual equipment performance; calculated electrical input is not a motor nameplate selection. | راندمان ۱۰۰٪ عملکرد واقعی نیست؛ توان برق محاسباتی به‌تنهایی انتخاب توان نامی موتور نیست.

For a multi-diameter or branched system, use a network-capable hydraulic model or calculate each segment and local fitting group separately while maintaining continuity and energy balance. Verify NPSH, motor loading and transient conditions for final design.
برای سیستم چندقطری یا شاخه‌دار از مدل هیدرولیکی شبکه استفاده کنید یا هر بخش و گروه اتصالات محلی را جداگانه محاسبه و پیوستگی و تعادل انرژی را کنترل کنید. برای طراحی نهایی NPSH، بار موتور و شرایط گذرا را نیز بررسی کنید.

## 9. Run and test | اجرا و تست
```bash
python main.py
python -m unittest discover -s tests -v
```
