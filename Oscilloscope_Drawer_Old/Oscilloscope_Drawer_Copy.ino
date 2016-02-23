/* ****************************************************************************
Fritzing is here:

http://www.flickr.com/photos/johngineer/6496005491/sizes/z/in/photostream/

in case you can't see the image, the following circuit is on both PWM ports

      	       R
PWM OUT ----/\/\/\-----+------------ OUTPUT
		       |           |
		      === C        |
                       |
                      GND

R = 10k
C = 0.1uF		

Use of a 16Mhz xtal/ceramic resonator is strongly suggested.

**************************************************************************** */

#define TRACE_DELAY	1000  // trace delay in uS.

#define S           1    // Speed of tracing in Volts/second

#define NUM_POINTS	4         
#define X           6    // attach scope channel 1 (X) to pin 6
#define Y           5    // attach scope channel 2 (y) to pin 5

#define R           10
#define C           0.1

#define e           2.718281828459

//~

unsigned char points[NUM_POINTS][2] = {{59,25},{59,75},{124,75},{125,25}};

//~

float pythag(float x, float y)
{
  return pow(pow(x, 2) + pow(y, 2), 0.5);
}

float compensate(float t, int delta_V)
{
  //    Charging: V = S * t / delta_V * (1 - e^(-t/RC))
  // Discharging: V = S * t / delta_V * e^(-t/RC)
  if (delta_V > 0)
  {
    return S * t / delta_V * (1 - pow(e, -t/(R * C)));
  }
  else if (delta_V < 0)
  {
    return S * t / delta_V * (pow(e, -t/(R * C)));
  }

// Check if it works for delta_V == 0
  
}

void setup()
{
  pinMode(X, OUTPUT);
  pinMode(Y, OUTPUT);

  // The following sets the PWM clock to maximum on the Arduino(no CPU clock division)
  
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

float delta_t;

void loop()
{
    {
      for(unsigned char i = 0; i < NUM_POINTS; i++)		// run through the points in x & y
      {
        float delta_t = pythag( (points[i][0] - points[i-1][0] ), ( points[i][1] - points[i-1][1] ) ) / S;
        
        float t = 0;
        
        while(t < delta_t)
        {
          float Vx = compensate(t, (points[i][0] - points[i-1][0])*0.01);
          float Vy = compensate(t, (points[i][1] - points[i-1][1])*0.01);
        
          analogWrite(X, points[i][0]);
          analogWrite(Y, points[i][1]);
  	delayMicroseconds(TRACE_DELAY);		    // wait TRACE_DELAY microseconds
          
          t += TRACE_DELAY *0.005;
        }
      }
    }
}

