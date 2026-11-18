# محاسبه هد کل دینامیکی پمپ (TDH)

## بخش فارسی

### هدف و معادله انرژی
این برنامه هد موردنیاز پمپ را برای یک مسیر جریان پایا بین دو مرز سیستم تخمین می‌زند.

`TDH=Δz+Δ(P/ρg)+Δ(V²/2g)+hf+hm+hequipment`

اجزای معادله شامل اختلاف ارتفاع، اختلاف هد فشار، اختلاف هد سرعت، افت طولی لوله، افت اتصالات و افت فشار تجهیزات است.

### هندسه لوله
برای HDPE گرید، SDR و OD انتخاب می‌شود و ID از ضخامت اسمی بانک محاسبه می‌شود. برای سایر مواد OD و ضخامت دیواره وارد می‌شود. زبری مرجع از بانک جنس خوانده می‌شود.

### تجهیزات و اتصالات
ضرایب K تقریبی‌اند و با سرعت قطر مرجع محاسبه می‌شوند. افت تجهیزات بر حسب bar وارد و با چگالی سیال به هد تبدیل می‌شود. مقدار افت باید مربوط به دبی محاسباتی باشد.

### منحنی پمپ
۲ تا ۳۰ نقطه وارد می‌شود. دبی و هد الزامی و راندمان پمپ و توان محور اختیاری‌اند. درون‌یابی خطی فقط در محدوده دبی‌های واردشده انجام می‌شود و برون‌یابی وجود ندارد. مقایسه هد پمپ و TDH به‌تنهایی نقطه کار واقعی نیست؛ نقطه کار از تقاطع منحنی پمپ و منحنی سیستم به دست می‌آید.

### کاربردها و محدودیت‌ها
برای انتقال بین مخازن و مسیر منفرد پمپ مناسب است. چند قطر و چند مسیر خودکار مدل نمی‌شوند. شبکه شاخه‌دار، تقسیم دبی، NPSH، کاویتاسیون، ضربه قوچ و تحلیل گذرا پشتیبانی نمی‌شوند.

## English Section

### Purpose and energy equation
This application estimates pump head for one steady-flow path between two system boundaries.

`TDH=Δz+Δ(P/ρg)+Δ(V²/2g)+hf+hm+hequipment`

The terms represent elevation difference, pressure-head difference, velocity-head difference, straight-pipe loss, fitting loss and equipment pressure drop.

### Pipe geometry
For HDPE, select grade, SDR and OD; ID is calculated from nominal database wall thickness. For other materials, enter OD and wall thickness. Reference roughness is loaded from the material database.

### Equipment and fittings
K coefficients are approximate and use the reference-diameter velocity. Equipment pressure drop is entered in bar and converted to head using fluid density. The entered drop must correspond to the calculation flow.

### Pump curve
Enter 2–30 points. Flow and head are required; pump efficiency and shaft power are optional. Linear interpolation is limited to the entered flow range, with no extrapolation. Comparing pump head with TDH alone does not determine the actual duty point; that requires the intersection of pump and system curves.

### Applications and limitations
Suitable for tank-to-tank transfer and a single pump route. Multiple diameters and paths are not assembled automatically. Branched networks, flow distribution, NPSH, cavitation, water hammer and transient analysis are not supported.
