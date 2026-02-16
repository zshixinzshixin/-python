// 代码功能：Arduino主程序，控制3个步进电机的运动
/*
特点：
三电机独立控制：支持三个步进电机的单独控制
串口通信协议：采用17字节固定长度的通信协议
定时器脉冲生成：使用三个定时器（Timer1、Timer3、Timer4）生成精确的脉冲信号
电机3特殊控制：电机3支持自动往返运动模式 
*/
#define motor1_pulse_pin 11
#define motor2_pulse_pin 5
#define motor3_pulse_pin 6

#define motor1_dir_pin 21
#define motor2_dir_pin 22
#define motor3_dir_pin 23

#define motor1_ena_pin 27
#define motor2_ena_pin 28
#define motor3_ena_pin 29

 
const int ProtocolLength=17;  //协议长度
byte SerialBuffer [ProtocolLength];  //串口数据缓存

int motorMode[3] = {0,0,0};
int motorSpeed[3] = {0,0,0};
long int motor3Max = 0;

long int motor3count = 0;
int motor3Dir = LOW;

int motorDiv = 800;
float step_size = 0.45;

int a=0;
unsigned long currentMillis = 0;  //单片机时间
unsigned long previousMillis = 0;  //单片机上次计数时间
long serial_count=0;  //串口计数


void setup() {
  // put your setup code here, to run once:
  Timer1_init();
  Timer3_init();
  Timer4_init();

//脉冲引脚
  pinMode(motor1_pulse_pin, OUTPUT);
  pinMode(motor2_pulse_pin, OUTPUT);
  pinMode(motor3_pulse_pin, OUTPUT);

//使能引脚
  pinMode(motor1_ena_pin, OUTPUT);
  pinMode(motor2_ena_pin, OUTPUT);
  pinMode(motor3_ena_pin, OUTPUT);

  digitalWrite(motor1_ena_pin,HIGH);
  digitalWrite(motor2_ena_pin,HIGH);
  digitalWrite(motor3_ena_pin,HIGH);

 //方向引脚
  pinMode(motor1_dir_pin, OUTPUT);
  pinMode(motor2_dir_pin, OUTPUT);
  pinMode(motor3_dir_pin, OUTPUT);
  pinMode(13, OUTPUT);
  
  Serial.begin(9600);
}

void loop() {
  
  if(Serial.available())
  {
    delay(20);
    if(Serial.available()==ProtocolLength){     //判断串口数据长度，若长度正确进行读取
    Serial.readBytes(SerialBuffer,ProtocolLength); //读取串口数据，放在buffer中
    }
    
    while (Serial.available()){
      Serial.print("Length=");
      Serial.println(Serial.available());//返回串口数据长度，调试用
      Serial.read();      //清空串口缓存
      }
    //若接受数据长度与协议不一致，清空串口缓存

    //串口数据解析
    motorSpeed[0] = 0;
    motorSpeed[1] = 0;
    motorSpeed[2] = 0;
    motor3Max = 0;
    
    for (a=0;a<3;a++)
    {
      motorSpeed[0] = 10*motorSpeed[0]+SerialBuffer[a+1]-48;
      motorSpeed[1] = 10*motorSpeed[1]+SerialBuffer[a+5]-48;
      motorSpeed[2] = 10*motorSpeed[2]+SerialBuffer[a+9]-48;
      motor3Max = 10*motor3Max+SerialBuffer[a+12]-48;
      }
    for (a=0;a<3;a++)
    {
      motorSpeed[a] = 6*motorSpeed[a];
      motorMode[a] = SerialBuffer[4*a]-48;
      }
      motor3Max = 2*motorDiv*motor3Max;
      //=================================================


        //Motor1
        if(motorMode[0]==4)
        {
          TCCR1B=0X0A;
          OCR1A=2000000/2/motorSpeed[0]*step_size;
          digitalWrite(motor1_dir_pin,LOW);
        }
        else if(motorMode[0]==5)
        {
          TCCR1B=0X0A;
          OCR1A=2000000/2/motorSpeed[0]*step_size;
          digitalWrite(motor1_dir_pin,HIGH);
          }
        else
        {
          TCCR1B=0X00;
        }
        //=======================================


        if(motorMode[1]==4)
        {
          TCCR3B=0X0A;
          OCR3A=2000000/2/motorSpeed[1]*step_size;
          digitalWrite(motor2_dir_pin,LOW);
          }
        else if(motorMode[1]==5)
        {
          TCCR3B=0X0A;
          OCR3A=2000000/2/motorSpeed[1]*step_size;
          digitalWrite(motor2_dir_pin,HIGH);
          }
        else
        {
          TCCR3B=0X00;
        }


        if(motorMode[2])
        {
          TCCR4B=0X0A;
          OCR4A=2000000/2/motorSpeed[2]*step_size;
          digitalWrite(motor3_dir_pin,motor3Dir);
          }
        else
        { 
          TCCR4B=0X00;
        }
  


//调试代码==============================
      currentMillis = millis();
    if (currentMillis - previousMillis >= 500) 
  {
    previousMillis = currentMillis;
    serial_count++;
    Serial.print(0.5*serial_count);
    Serial.print(",");
    Serial.print(motorSpeed[0]);
    Serial.print(",");
    Serial.print(motorSpeed[1]);
    Serial.print(",");
        Serial.print(motorSpeed[2]);
    Serial.print(",");
    Serial.print(motor3Max);
    Serial.print(",");
        Serial.print(motor3count);
    Serial.print(",");
    Serial.println(motor3Dir);

     }
  }
 //================================    
  // put your main code here, to run repeatedly:  
}



void Timer1_init(void)
{
  TCCR1A=0X50;  //普通模式
  TCCR1B=0X00;  //8分频（2Mhz时钟频率）1A 和1B 两个寄存器共同控制模式和分频系数，详见手册
  OCR1A=29999;  //（20hz PWM频率,注意这个值的上限65535）
  //OCR1B=999;    //通电10ms后开始读iic
  }

  
void Timer3_init(void)
{
  TCCR3A=0X50;  //普通模式
  TCCR3B=0X00;  //8分频（2Mhz时钟频率）1A 和1B 两个寄存器共同控制模式和分频系数，详见手册
  OCR3A=19999;  //（20hz PWM频率,注意这个值的上限255）
  //OCR1B=999;    //通电10ms后开始读iic
  }

  void Timer4_init(void)
{
  TCCR4A=0X50;  //普通模式
  TCCR4B=0X00;  //8分频（2Mhz时钟频率）1A 和1B 两个寄存器共同控制模式和分频系数，详见手册
  OCR4A=19999;  //（20hz PWM频率,注意这个值的上限255）
  //OCR1B=999;    //通电10ms后开始读iic

  TIMSK4 |=(1 << OCIE4A);  //开启比较中断
  }

  ISR(TIMER4_COMPA_vect) //定时器更新中断
{
  motor3count+=1;
  if (motor3count>=motor3Max)
  {
    motor3count=0;
    if (motor3Dir == LOW) {
      motor3Dir = HIGH;
    } else {
      motor3Dir = LOW;
    }
    digitalWrite(3,motor3Dir);
    digitalWrite(13,motor3Dir);
    }  
  
}


