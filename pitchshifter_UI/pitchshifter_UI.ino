#include <Adafruit_GFX.h>    // Core graphics library
#include <MCUFRIEND_kbv.h>   // Hardware-specific library
#include <Fonts/FreeSans9pt7b.h>
#include <TouchScreen.h>

#define BLACK   0x0000
#define GREY    0x8410
#define WHITE   0xFFFF
#define MINPRESSURE 200
#define MAXPRESSURE 1000

//display
MCUFRIEND_kbv tft;

//Touchscreen Calibration
const int XP = 8, XM = A2, YP = A3, YM = 9; //ID=0x9341
const int TS_LEFT = 136, TS_RT = 916, TS_TOP = 945, TS_BOT = 94;
TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);

//buttons
String controls[] = {"Transposition","Window","Delay"};
Adafruit_GFX_Button trans;
Adafruit_GFX_Button wind;
Adafruit_GFX_Button del;
Adafruit_GFX_Button* buttons[] = {&trans, &wind, &del};
int len = sizeof buttons/sizeof buttons[0];

//mapping values
int low_vals[] = {-24,0,0};
int high_vals[] = {24, 1000, 500};

//potentiometer
int pot = A15;
int last_val = 0;

//function that determines point of screen that is pressed
bool Touch_getXY(void);
int pixel_x, pixel_y;

//button functions
bool update_button_list(Adafruit_GFX_Button **pb);
bool update_button(Adafruit_GFX_Button *b, bool down);

//function to write text
void update_text(int x, int y, String control, String color);

void pressed(int i);
void mapPot(int i);
bool almost_equal(float num1, float num2, float tol);


void setup() 
{
    Serial.begin(9600);

    //initialize screen
    uint16_t ID = tft.readID();
    if (ID == 0xD3) ID = 0x9481;
    tft.begin(ID);
    tft.setRotation(0);
    tft.fillScreen(GREY);

    //initialize buttons
    char control1[1] = "";
    char* label1 = control1;

    //Draw GUI
    for(int i = 0; i < len; i++)
    {
        buttons[i]->initButtonUL(&tft,  -10, -5+(40*i), 340, 40, BLACK, GREY, GREY, label1, 2);
        buttons[i]->drawButton(false);
    
        //write options to screen
        update_text(0, 40*i+30, controls[i], "WHITE");
    }
}

void loop()
{
    //check for pressed buttons
    update_button_list(buttons);
    for(int i = 0; i < len; i++)
    {
        if (buttons[i]->justPressed())
        {
            pressed(i);
        }
    }
}

void pressed(int i)
{
    update_text(0, 40*i+30, controls[i], "BLACK");  //make text black
    delay(50);  //debounce

    //check if user clicked away
    bool touched = false;
    while(!touched)
    {
        touched = Touch_getXY();
        mapPot(i);
    }
    update_text(0, 40*i+30, controls[i], "WHITE");
}

void mapPot(int i)
{
    int pot_val;
    int mapped_val;
    pot_val = analogRead(pot);
    if(!almost_equal(last_val,pot_val,2))
    {
        mapped_val = map(pot_val,0,1023,0,255-len);   //map 10bit to 8bit
        Serial.write(i);                              //control id
        Serial.write(mapped_val+len);                 //potentiometer value
        last_val = pot_val;
    }
}

bool almost_equal(float num1, float num2, float tol)
{
    if(abs(num1-num2)<abs(tol))
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool Touch_getXY(void)
{
    TSPoint p = ts.getPoint();
    pinMode(YP, OUTPUT);      //restore shared pins
    pinMode(XM, OUTPUT);
    digitalWrite(YP, HIGH);   //because TFT control pins
    digitalWrite(XM, HIGH);
    bool pressed = (p.z > MINPRESSURE && p.z < MAXPRESSURE);
    if (pressed) {
        pixel_x = map(p.x, TS_LEFT, TS_RT, 0, tft.width()); //.kbv makes sense to me
        pixel_y = map(p.y, TS_TOP, TS_BOT, 0, tft.height());
    }
    return pressed;
}

void update_text(int x, int y, String control, String color)
{
    if (color == "BLACK")
    {
      tft.setTextColor(BLACK,BLACK);
    }
    else
    {
      tft.setTextColor(WHITE,BLACK);
    }
    tft.setFont(&FreeSans9pt7b);
    tft.setTextSize(2);
    tft.setCursor(x,y);
    tft.print(control);
}

bool update_button(Adafruit_GFX_Button *b, bool down)
{
    b->press(down && b->contains(pixel_x, pixel_y));
    if (b->justReleased())
        //b->drawButton(false);
    if (b->justPressed())
        //b->drawButton(false);
    return down;
}


bool update_button_list(Adafruit_GFX_Button **pb)
{
    bool down = Touch_getXY();
    for (int i = 0; i < len; i++) {
        update_button(pb[i], down);
    }
    return down;
}
