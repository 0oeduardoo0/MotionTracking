#include <Servo.h>
#define MOV_LEFT 'L'
#define MOV_RIGHT 'R'
#define MOV_DOWN 'D'
#define MOV_UP 'U'
#define LED_LEFT 48
#define LED_RIGHT 49
#define LED_DOWN 46
#define LED_UP 47
#define MAX_X 120
#define MAX_Y 140
#define SENS 5

Servo xServo;
Servo yServo;
int anguloX = 60;
int anguloY = 70;
void turnOnLed( int pin );
void turnOffAllLeds();

void setup()
{
  xServo.attach(2);
  yServo.attach(3);
  Serial.begin(9600);

  for( int i = 46; i < 50; i++ )
  {
    pinMode(i, OUTPUT);
  }

}//end setup


void loop()
{

  unsigned char comando = 0;

  if(Serial.available())
  {    
    comando = Serial.read();

    switch( comando ) 
    {
      case MOV_RIGHT:
        anguloX += SENS;
        turnOnLed( LED_RIGHT );
        break;
      case MOV_LEFT:
        anguloX -= SENS;
        turnOnLed( LED_LEFT );
        break;
      case MOV_UP:
        anguloY -= SENS;
        turnOnLed( LED_UP );
        break;
      case MOV_DOWN:
        anguloY += SENS;
        turnOnLed( LED_DOWN );
        break;
    }

    anguloX = constrain( anguloX, 0, MAX_X );
    anguloY = constrain( anguloY, 0, MAX_Y );
  }

  xServo.write( anguloX );
  yServo.write( anguloY );
  delay(10);
  turnOffAllLeds();
}//End loop

void turnOnLed( int pin ) 
{
  digitalWrite( pin, HIGH);
}

void turnOffAllLeds() 
{
  for ( int i = 46; i < 50; i++ )
  {
    digitalWrite( i, LOW );
  }
}
