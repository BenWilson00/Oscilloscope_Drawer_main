#define TRACE_DELAY	1000000000

#define NUM_POINTS 4          

//~

unsigned char points[NUM_POINTS][2] = {{59,25},{59,75},{124,75},{125,25}};

//~


void setup()
{
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  
  TCCR0A = (	1<<COM0A1 | 0<<COM0A0 |		// clear OC0A on compare match (hi-lo PWM)
          		1<<COM0B1 | 0<<COM0B0 |		// clear OC0B on compare match (hi-lo PWM)
          		1<<WGM01  | 1<<WGM00);		// set PWM lines at 0xFF

  TCCR0B = (	0<<FOC0A | 0<<FOC0B |		// no force compare match
          		0<<WGM02 |			        // set PWM lines at 0xFF
          		0<<CS02	 | 0<<CS01 |		// use system clock (no divider)
          		1<<CS00 );

  TIMSK0 = (	0<<OCIE0B | 0<<TOIE0 |
		          0<<OCIE0A );  

}

void loop()
{
  unsigned char t;
  {
    for(t = 0; t < NUM_POINTS; t++)		// run through the points in x & y
    {

      analogWrite(X, points[t][0]);
      analogWrite(Y, points[t][1]);
    	delayMicroseconds(TRACE_DELAY);
      delayMicroseconds(TRACE_DELAY);// wait TRACE_DELAY microseconds
      
    }
  }
}

