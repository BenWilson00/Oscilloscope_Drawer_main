

#define TRACE_DELAY	1000

#define X               5     // attach scope channel 1 (X) to pin 6
#define Y               6     // attach scope channel 2 (y) to pin 5

#define POINTS_LENGTH 4

#define I_LENGTH 1

//~

unsigned char points[][2] = {{210, 210}, {20, 210}, {20, 20}, {210, 20}};
  
//~


void setup()
{
  pinMode(X, OUTPUT);
  pinMode(Y, OUTPUT);

  
  TCCR0A = (	1<<COM0A1 | 0<<COM0A0 |		// clear OC0A on compare match (hi-lo PWM)
		1<<COM0B1 | 0<<COM0B0 |		// clear OC0B on compare match (hi-lo PWM)
		1<<WGM01  | 1<<WGM00);		// set PWM lines at 0xFF

  TCCR0B = (	0<<FOC0A | 0<<FOC0B |		// no force compare match
		0<<WGM02 |			// set PWM lines at 0xFF
		0<<CS02	 | 0<<CS01 |		// use system clock (no divider)
		1<<CS00 );

  TIMSK0 = (	0<<OCIE0B | 0<<TOIE0 |
		0<<OCIE0A );  

}
void loop()
{
   while (true) {
    for (unsigned char t = 0; t < POINTS_LENGTH; t++)		// run through the points in x & y
      {
        analogWrite(X, points[t][0]);

        analogWrite(Y, points[t][1]);
        
        delay(TRACE_DELAY);// wait TRACE_DELAY microseconds
      }
     }
}

