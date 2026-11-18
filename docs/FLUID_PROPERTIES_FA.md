# EC-Based Fluid Properties | تخمین خواص سیال بر اساس EC

## 1. Inputs | ورودی‌ها
- **EN:** EC in mS/cm, already temperature-compensated to 25°C. The program does not apply a second temperature correction.
- **FA:** EC بر حسب mS/cm که از قبل به دمای مرجع ۲۵ درجه جبران شده باشد. برنامه دوباره اصلاح دمایی انجام نمی‌دهد.
- **EN:** Actual operating water temperature in °C, entered independently and used for the property estimate.
- **FA:** دمای واقعی کارکرد آب بر حسب درجه سانتی‌گراد که مستقل وارد و برای تخمین خواص استفاده می‌شود.
- **EN:** Composition profile: generic water or natural-seawater ionic-ratio assumption.
- **FA:** پروفایل ترکیب: آب عمومی یا فرض نسبت‌های یونی آب دریای طبیعی.

## 2. Calculation model | مدل محاسبه
The internal TDS conversion factor is fixed at 0.65 in the current implementation:
`TDS (mg/L) ≈ EC (µS/cm) × 0.65`

ضریب تبدیل داخلی TDS برابر ۰٫۶۵ است و در نسخه فعلی ورودی کاربر نیست:
`TDS (mg/L) ≈ EC (µS/cm) × 0.65`

Density and dynamic viscosity are estimated using screening corrections to freshwater temperature data; kinematic viscosity is `ν=μ/ρ`. These are engineering screening correlations, not a universal electrolyte equation of state.

چگالی و ویسکوزیته دینامیکی با اصلاح‌های تقریبی روی داده آب شیرین در دمای مربوط تخمین زده می‌شوند؛ ویسکوزیته سینماتیکی از رابطه `ν=μ/ρ` به دست می‌آید. این روابط همبستگی غربالگری‌اند، نه معادله حالت عمومی برای همه الکترولیت‌ها.

## 3. Composition profile | پروفایل ترکیب
**Generic | عمومی:** EC is used to estimate TDS and screening properties only. Individual sodium, calcium, magnesium, chloride, sulfate, iron or alkalinity values are not inferred.

در حالت عمومی، EC فقط برای تخمین TDS و خواص غربالگری استفاده می‌شود. غلظت سدیم، کلسیم، منیزیم، کلرید، سولفات، آهن یا قلیائیت از EC به‌تنهایی استخراج نمی‌شود.

**Natural seawater | آب دریای طبیعی:** The program scales a standard natural-seawater ionic composition in proportion to estimated TDS. This is an assumption for natural seawater, not a chemical analysis.

در حالت آب دریای طبیعی، برنامه ترکیب یونی مرجع آب دریا را متناسب با TDS تخمینی مقیاس می‌کند. این صرفاً یک فرض برای آب دریای طبیعی است و آنالیز شیمیایی واقعی نیست.

## 4. Suitable use | موارد استفاده مناسب
- **EN:** Preliminary hydraulic estimates for ordinary fresh, brackish or natural seawater when laboratory density and viscosity are unavailable.
- **FA:** تخمین اولیه هیدرولیکی برای آب شیرین، لب‌شور یا آب دریای طبیعی در شرایطی که چگالی و ویسکوزیته آزمایشگاهی موجود نیست.
- **EN:** Sensitivity comparisons to understand how approximate density and viscosity affect Reynolds number, friction and pressure loss.
- **FA:** مقایسه حساسیت برای درک اثر تقریبی چگالی و ویسکوزیته بر Reynolds، اصطکاک و افت فشار.

## 5. Limitations | محدودیت‌ها
- EC alone cannot uniquely determine TDS factor or individual ion concentrations; factor 0.65 is not universal. | EC به‌تنهایی ضریب واقعی TDS یا غلظت یون‌های منفرد را مشخص نمی‌کند؛ ضریب ۰٫۶۵ عمومی و قطعی نیست.
- Natural-seawater ion ratios must not be used for groundwater, industrial water, produced water or RO concentrate unless laboratory analysis validates the assumption. | نسبت‌های آب دریای طبیعی را برای آب چاه، آب صنعتی، آب تولیدی یا کنسانتره RO به‌کار نبرید مگر آزمایش آن را تأیید کند.
- Concentrated brines, high salinity, unusual ionic composition, high pressure or temperatures outside the implemented freshwater table require validated property data. | شورابه غلیظ، شوری بالا، ترکیب یونی غیرمعمول، فشار بالا یا دماهای خارج از جدول آب شیرین به داده خواص معتبر نیاز دارند.
- The current temperature table supports 0–100°C; the EC value must already be referenced to 25°C. | جدول دمایی فعلی ۰ تا ۱۰۰ درجه را پشتیبانی می‌کند؛ EC باید از قبل به ۲۵ درجه مرجع شده باشد.
- This module is not for scaling prediction, chemical dosing, corrosion, membrane design or water-quality compliance. | این ماژول برای پیش‌بینی رسوب، تزریق مواد شیمیایی، خوردگی، طراحی غشا یا انطباق کیفیت آب نیست.

For final design, use laboratory-measured density, viscosity, TDS and ion analysis or a validated electrolyte model for the actual fluid and operating temperature.
برای طراحی نهایی از چگالی، ویسکوزیته، TDS و آنالیز یونی آزمایشگاهی یا مدل معتبر الکترولیتی متناسب با سیال واقعی و دمای کار استفاده کنید.
