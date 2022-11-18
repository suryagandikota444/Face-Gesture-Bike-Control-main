#include "FastLED.h"
CRGB LEDs[20];

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  FastLED.addLeds<WS2812B, 2, GRB>(LEDs,20);
  for(int x=0; x<8; x++)
  {
    LEDs[x+6]= CRGB::Red;
    FastLED.show();
  }

}
void loop() {
  while (!Serial.available());
  int x = Serial.readString().toInt();
  Serial.print(x);
  if (x==0) {
    for(int x=0; x<5; x++)
      {
        LEDs[4-x] = CRGB(89, 255, 0);
        FastLED.show();
        delay(20 * (5-x));
      } 
      delay(100);
      for(int x=0; x<5; x++)
      {
        LEDs[4-x] = CRGB::Black;
        FastLED.show();
      } 
      FastLED.show();
      delay(100);
  } else if (x==1) {
    for(int x=0; x<5; x++)
      {
        LEDs[x+15] = CRGB(89, 255, 0);
        FastLED.show();
        delay(20 * (5-x));
      } 
      delay(100);
      for(int x=0; x<5; x++) {
        LEDs[x+15] = CRGB::Black;
        FastLED.show();
        //delay(20 * (5-x));
      } 
      FastLED.show();
      delay(100);
  }
}
