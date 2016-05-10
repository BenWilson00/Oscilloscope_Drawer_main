/*
 * 	Oscilloscope Christmas Tree
 *
 *  	Created: Dec 10, 2011
 *  
 *	Author: John M. De Cristofaro
 *
 *	License: This code CC-BY-SA 3.0 and is unsupported.
 *		 (see creativecommons.org/licenses for info)
 *
 */

/* ****************************************************************************
Fritzing is here:

http://www.flickr.com/photos/johngineer/6496005491/sizes/z/in/photostream/

in case you can't see the image, the following circuit is on both PWM ports

	       R
PWM OUT ----/\/\/\-----+------------ OUTPUT
		       |
		      === C
                       |
                      GND

R = 10k
C = 0.1uF		

Use of a 16Mhz xtal/ceramic resonator is strongly suggested.

**************************************************************************** */

#define TRACE_DELAY	1000000000  // trace delay in uS. making this longer will
			      // result in a straighter drawing, but slower
			      // refresh rate. making it too short will result
			      // in an angular blob.

#define NUM_POINTS 95         

#define X               5     // attach scope channel 1 (X) to pin 6
#define Y               6     // attach scope channel 2 (y) to pin 5


//~

unsigned char points[NUM_POINTS][2] = {{173,74},{168,83},{163,92},{159,101},{154,110},{149,118},{145,127},{140,136},{136,145},{131,154},{126,163},{122,172},{117,181},{112,189},{108,198},{103,207},{99,216},{94,225},{89,234},{85,243},{80,252},{90,252},{100,252},{110,252},{120,252},{130,252},{140,252},{150,252},{160,252},{170,252},{181,252},{191,252},{201,252},{211,252},{221,252},{231,252},{241,252},{251,252},{261,252},{271,252},{281,252},{291,252},{301,252},{311,252},{321,252},{331,252},{341,252},{351,252},{362,252},{366,243},{370,235},{374,226},{378,218},{382,209},{386,201},{390,192},{394,184},{398,175},{388,174},{378,173},{368,172},{358,171},{349,170},{339,169},{329,168},{319,167},{309,166},{299,165},{289,164},{279,163},{269,162},{260,162},{265,153},{271,144},{277,135},{282,127},{288,118},{294,109},{299,101},{305,92},{311,83},{317,75},{306,74},{296,74},{286,74},{275,74},{265,74},{255,74},{245,74},{234,74},{224,74},{214,74},{203,74},{193,74},{183,74}};

//~


void setup()
{
  pinMode(X, OUTPUT);
  pinMode(Y, OUTPUT);

  // The following sets the PWM clock to maximum on the Arduino(no CPU clock division)
  // DO NOT CHANGE THESE UNLESS YOU KNOW WHAT YOU ARE DOING!
  
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

