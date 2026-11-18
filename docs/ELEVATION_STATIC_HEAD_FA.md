# Elevation and Static Head | اختلاف ارتفاع و هد استاتیکی

## Purpose | هدف
**EN:** This module calculates the elevation contribution to the pump energy balance. It is one component of TDH, not a complete TDH calculation by itself.

**FA:** این ماژول مؤلفه اختلاف ارتفاع را در تراز انرژی پمپ محاسبه می‌کند. این فقط یکی از اجزای TDH است و به‌تنهایی محاسبه کامل TDH نیست.

## Input methods | روش‌های ورود
1. **Direct elevation difference | اختلاف ارتفاع مستقیم:** enter Δz in metres. Positive means the destination is higher; negative means it is lower.
2. **Start and end elevations | تراز ابتدا و انتها:** enter z1 and z2 relative to the same common vertical datum.

`Δz=z2-z1`

Example: z1=10 m and z2=35 m gives Δz=+25 m. Reversing the direction gives -25 m.

مثال: تراز ابتدا ۱۰ و تراز مقصد ۳۵ متر باشد، اختلاف ارتفاع +۲۵ متر است. با معکوس شدن جهت، مقدار -۲۵ متر می‌شود.

## Suitable applications | موارد کاربرد
- **EN:** Transfers between tanks, reservoirs or process equipment where boundary elevations are known.
- **FA:** انتقال بین مخازن، حوضچه‌ها یا تجهیزات فرایندی که تراز مرزهای آن‌ها مشخص است.
- **EN:** Comparing uphill and downhill routes and supplying the static-head term to the TDH calculation.
- **FA:** مقایسه مسیرهای سربالایی و سرازیری و تأمین مؤلفه هد استاتیکی برای محاسبه TDH.

## Limitations | محدودیت‌ها
- Both elevations must use the same vertical datum. | هر دو تراز باید نسبت به یک مبنای ارتفاعی مشترک باشند.
- This module does not calculate pipe friction, fittings, equipment pressure drop, boundary pressure/velocity terms or pump power. | این ماژول افت لوله، اتصالات، افت تجهیزات، مؤلفه فشار/سرعت مرزی یا توان پمپ را محاسبه نمی‌کند.
- Elevation alone is not pump TDH. All other energy terms and losses must be included. | اختلاف ارتفاع به‌تنهایی TDH پمپ نیست؛ تمام مؤلفه‌های انرژی و افت‌ها باید لحاظ شوند.

In the current application, the result is passed into the complete single-path TDH calculation.
در برنامه فعلی، نتیجه این ماژول به محاسبه کامل TDH تک‌مسیره وارد می‌شود.

## Tests | آزمون‌ها
```bash
python -m unittest discover -s tests -v
```
