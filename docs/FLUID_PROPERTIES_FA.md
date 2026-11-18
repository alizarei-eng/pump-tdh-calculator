# تخمین خواص سیال بر اساس EC

## بخش فارسی

### ورودی و مدل
EC بر حسب mS/cm باید از قبل به ۲۵°C جبران شده باشد. دمای واقعی کارکرد آب جداگانه وارد می‌شود. ضریب تبدیل داخلی TDS برابر ۰٫۶۵ است و از کاربر دریافت نمی‌شود:
`TDS (mg/L) ≈ EC (µS/cm) × 0.65`
چگالی و ویسکوزیته با همبستگی‌های تقریبی مبتنی بر داده آب شیرین تخمین زده می‌شوند.

### پروفایل ترکیب
پروفایل عمومی غلظت یون‌های منفرد را از EC استنتاج نمی‌کند. پروفایل آب دریای طبیعی نسبت‌های یونی مرجع را فرض می‌کند و جایگزین آنالیز شیمیایی نیست.

### کاربردها و محدودیت‌ها
برای تخمین اولیه آب شیرین، لب‌شور و آب دریای طبیعی مناسب است. EC به‌تنهایی TDS دقیق یا غلظت یون‌ها را مشخص نمی‌کند. نسبت‌های آب دریای طبیعی برای آب چاه یا کنسانتره RO معتبر فرض نمی‌شوند. شورابه غلیظ و ترکیب یونی غیرمعمول به داده معتبر نیاز دارند. این ماژول برای پیش‌بینی رسوب، خوردگی یا طراحی غشا نیست.

## English Section

### Inputs and model
EC in mS/cm must already be compensated to 25°C. Actual operating water temperature is entered separately. The internal TDS conversion factor is 0.65 and is not a user input:
`TDS (mg/L) ≈ EC (µS/cm) × 0.65`
Density and viscosity are estimated using approximate correlations based on freshwater data.

### Composition profiles
The generic profile does not infer individual ion concentrations from EC. The natural-seawater profile assumes reference ionic ratios and is not a substitute for chemical analysis.

### Applications and limitations
Suitable for preliminary estimates for fresh water, brackish water and natural seawater. EC alone does not determine exact TDS or individual ion concentrations. Natural-seawater ratios must not be assumed valid for groundwater or RO concentrate. Concentrated brines and unusual ionic compositions require validated data. This module is not intended for scale prediction, corrosion or membrane design.
