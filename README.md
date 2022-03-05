# LINE_Notify_Weather_With_Lambda
This is a system to notify the weather in Shibuya-ku at A.M.9:00 every day through LINE App.

The conposition of this system is very simple. ↓↓

LINE Notify API ← AWS Lambda (scraping web site of weather forecast) ←  Cloud Watch Events (A.M.9:00 every day) <br>
     ↓<br>
  LINE App<br>
  ・ Weather: ☀️<br>
  ・ Temperature: 10℃/20℃<br>
  ・ Rain-Prob: 20%<br>
