#include "FastLED.h"
CRGB LEDs[20];

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  FastLED.addLeds<WS2812B, 15, GRB>(LEDs,20);
  for(int x=0; x<8; x++)
  {
    LEDs[x+8]= CRGB::Red;
    FastLED.show();
  }

}
void loop() {
  while (!Serial.available());
  int serial = Serial.readString().toInt();
  Serial.print(serial);
  for(int x=0; x<8; x++)
  {
    LEDs[x+8]= CRGB::Red;
    FastLED.show();
  }
  if (serial==0) {
    for (int iter=0; iter<4; iter++) {
      for(int x=0; x<5; x++)
      {
        LEDs[7-x] = CRGB(255,120,0);
        FastLED.show();
        delay(40 * (5-x));
      } 
      delay(150);
      for(int x=0; x<5; x++)
      {
        LEDs[7-x] = CRGB::Black;
        FastLED.show();
      } 
      FastLED.show();
      delay(100);
    }
  } else if (serial==1) {
    for (int iter=0; iter<4; iter++) {
      for(int x=0; x<5; x++)
      {
        LEDs[x+16] = CRGB(255,120,0);
        FastLED.show();
        delay(40 * (5-x));
      } 
      delay(150);
      for(int x=0; x<5; x++) {
        LEDs[x+16] = CRGB::Black;
        FastLED.show();
      } 
      FastLED.show();
      delay(100);
    }
  }
}
