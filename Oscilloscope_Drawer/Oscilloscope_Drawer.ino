#define LOOP_TIME 5000.0
#define ITS_PER_FRAME 20

#define _RT2 0.707
#define APPROX_FACTOR 1.041

//~
#define FRAME_N 1
unsigned char points[FRAME_N][64][2] = {{{0, 0}, {36, 215}, {35, 128}, {0, 0}, {36, 157}, {57, 163}, {66, 140}, {68, 124}, {0, 0}, {99, 144}, {109, 147}, {106, 164}, {95, 155}, {103, 133}, {112, 133}, {0, 0}, {134, 198}, {130, 132}, {137, 129}, {0, 0}, {153, 199}, {153, 127}, {161, 123}, {0, 0}, {188, 144}, {195, 121}, {208, 136}, {196, 154}, {186, 139}, {0, 0}, {103, 53}, {97, 38}, {109, 23}, {118, 45}, {103, 50}, {0, 0}, {140, 17}, {141, 52}, {157, 53}, {0, 0}, {178, 79}, {173, 22}, {184, 17}, {0, 0}, {209, 48}, {212, 19}, {199, 20}, {196, 39}, {209, 49}, {209, 79}, {0, 0}, {213, 29}, {226, 14}, {0, 0}, {36, 30}, {72, 37}, {72, 56}, {0, 0}, {33, 30}, {32, 62}, {0, 0}, {32, 32}, {53, 31}, {52, 59}}};
unsigned char lengths[FRAME_N] = {64};
//~

int fast_pythag(int x, int y) {
  x = max(x, -x);
  y = max(y, -y);
  
  // max(x, y) -- approximation 1 - good for |x-y| is large
  // (x + y) * 1/sqrt(2) -- approximation 2 - good for x==y
  // take min of two for closest approximation

  return (int) ( APPROX_FACTOR * min(_RT2*(x + y), max(x, y)) );
}

void setup()
{

  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);

  // using the 8-bit timers, 0 and 2

  // Both outputs on compare match, fast PWM changing at OCR, using system clock without divisor
  TCCR0A =  0b10100011;
  TCCR0B =  0b00000001;

  // Raise no interrupts.
  TIMSK0 =  0b00000000;

  OCR0A = 127;
  OCR0B = 127;
}

void loop()
{
  unsigned char i, curr_x, curr_y, next_x, next_y;
  int j, k, frame_len, n_jumps;
  float v, adj_v, l, len;
  bool block = false;
  
  for (i = 0; i < FRAME_N; i++) // iterate through frames
  {

    // Calculate total travel distance in this frame's loop
    frame_len = 0;
    
    for (j = 0; j < lengths[i]; j++) {
      frame_len += fast_pythag(points[i][j][0], points[i][j][1]);
    }

    // Calculate velocity by dividing total distance by total time
    v = frame_len / LOOP_TIME;

    for (k = 0; k < ITS_PER_FRAME; k++) // frame persist loop
    {
      for (j = 0; j < lengths[i]; j++) // iterate through frame values
      {

        adj_v = v * analogRead(A0) / 200.0 + 0.1;
        
        // get current and next x and y values
        curr_x = points[i][j][0];
        curr_y = points[i][j][1];

        if (j != lengths[i] - 1) { next_x = points[i][j+1][0]; next_y = points[i][j+1][1]; }
        else { next_x = points[i][0][0]; next_y = points[i][0][1]; }

//      if there is no jump, calculate jumps to next point

        if (curr_x != 0 and next_x != 0) {
  
          len = fast_pythag(next_x - curr_x, next_y - curr_y);
    
          for (l = 0.0; l < len - adj_v; l += adj_v) {
            analogWrite(5, curr_x + l * (next_x - curr_x) / len );
            analogWrite(6, curr_y + l * (next_y - curr_y) / len );
          }
        }
      }
    }
  }
}
