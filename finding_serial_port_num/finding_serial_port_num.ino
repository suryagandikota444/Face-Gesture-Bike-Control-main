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
  int serial = Serial.readString().toInt();
  Serial.print(serial);
  if (serial==0) {
    for (int iter=0; iter<5; iter++) {
      for(int x=0; x<5; x++)
      {
        LEDs[4-x] = CRGB(89, 255, 0);
        FastLED.show();
        delay(40 * (5-x));
      } 
      delay(150);
      for(int x=0; x<5; x++)
      {
        LEDs[4-x] = CRGB::Black;
        FastLED.show();
      } 
      FastLED.show();
      delay(100);
    }
  } else if (serial==1) {
    for (int iter=0; iter<5; iter++) {
      for(int x=0; x<5; x++)
      {
        LEDs[x+15] = CRGB(89, 255, 0);
        FastLED.show();
        delay(40 * (5-x));
      } 
      delay(150);
      for(int x=0; x<5; x++) {
        LEDs[x+15] = CRGB::Black;
        FastLED.show();
      } 
      FastLED.show();
      delay(100);
    }
  }
}
