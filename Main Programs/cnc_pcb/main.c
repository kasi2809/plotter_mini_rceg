#include <msp430.h> 
#include <stdint.h>

//=============================MACROS===============================//

#define UART_TX                 BIT2                    //P1.2
#define UART_RX                 BIT1                    //P1.1

#define STEPPER_X_PULSE         BIT1                    //P2.1(TA1.1)
#define STEPPER_Y_PULSE         BIT4                    //P2.4(TA1.2)
#define STEPPER_X_DIR           BIT2                    //P2.2
#define STEPPER_Y_DIR           BIT5                    //P2.5
#define DC_MOTOR_IN3            BIT0                    //P2.0
#define DC_MOTOR_IN4            BIT3                    //P2.3


#define STEPPER_X_DIR_PXOUT     P2OUT
#define STEPPER_Y_DIR_PXOUT     P2OUT
#define STEPPER_X_PULSE_PXOUT   P2OUT
#define STEPPER_Y_PULSE_PXOUT   P2OUT
#define DC_MOTOR_IN3_PXOUT      P2OUT
#define DC_MOTOR_IN4_PXOUT      P2OUT

#define STEPPER_X_DIR_PXDIR     P2DIR
#define STEPPER_Y_DIR_PXDIR     P2DIR
#define STEPPER_X_PULSE_PXDIR   P2DIR
#define STEPPER_Y_PULSE_PXDIR   P2DIR
#define DC_MOTOR_IN3_PXDIR      P2OUT
#define DC_MOTOR_IN4_PXDIR      P2OUT

#define SPEEDM                  1000
#define DELAYT                  140
#define TIME_TO_SOLDER          2000
//=================================================================//

//=============================Function headers===============================//
void sendString(unsigned char *);
void configPort();
void configUART();
void configTimer1();
void configTimer0();
void delayms(uint16_t);
void moveToXorY(int16_t, unsigned char);
void moveZ();

//============================================================================//

//=============================Global variables===============================//
volatile struct stepperSteps{
    int16_t stepX,stepY, stepForTimer;
    uint8_t currentByte;
    uint8_t currentNibble : 1;            //0 - upper nibble
                                          //1 - lower nibble

    uint8_t currentStep : 1;              //0 - stepX
                                          //1 - stepY

    uint8_t continueReception : 1;        //0 - stop receivind data from BT module
                                          //1 - Continues reception of next data

}s1={0};                                  //Initialize structure with all elements 0

volatile uint16_t timeInms;                        //For generating ms delay
//=============================================================================//
int main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer
	
	//MCLK to run at calibrated 1 MHz frequency
	DCOCTL = 0;
	BCSCTL1 = CALBC1_1MHZ;
	DCOCTL = CALDCO_1MHZ;

	configPort();
	configUART();
	configTimer1();
	configTimer0();

	__bis_SR_register(GIE);     //Enable all maskable interrupts

	while(1){
	    s1 = (struct stepperSteps){0};  //Reset the structure for Current Iteration
	    s1.continueReception = 1;       //To continue receiving from UART. Look at the do..while.. loop for more info

	    IE2 |= UCA0RXIE;                //Enable RX interrupt for
	    sendString("NEXT");
	    do{
	        __bis_SR_register(LPM0_bits);   //Go to sleep and sleep till RXIFG wake you up

	        if(s1.currentStep){
	            if(s1.currentNibble){
	                s1.stepY |= (int16_t)s1.currentByte;    //Lower nibble of stepY is stored in s1.stepY
	                s1.currentNibble = 0;                   //To indicate low nibble is filled
	                s1.currentStep = 0;                     //To indicate stepY is filled
	                s1.continueReception = 0;               //To stop receiving data
	            }else{
	                s1.stepY |= ((int16_t)s1.currentByte) << 8;    //Upper nibble of stepY is stored in s1.stepY
	                s1.currentNibble = 1;                          //To indicate upper nibble is filled
	            }
	        }else{
	            if(s1.currentNibble){
	                    s1.stepX |= (int16_t)s1.currentByte;              //Lower nibble of stepX is stored in s1.stepX
	                    s1.currentNibble = 0;                          //To indicate lower nibble is filled
	                    s1.currentStep = 1;                            //To indicate stepX is filled
	            }else{
	                     s1.stepX |= ((int16_t)s1.currentByte) << 8;      //Upper nibble of stepX is stored in s1.stepX
	                     s1.currentNibble = 1;                         //To indicate upper nibble is filled
	            }
	        }

	    }while(s1.continueReception);
	    IE2 &= ~UCA0RXIE;                                   //Stop generating interrupts for RX


	    moveToXorY(s1.stepX, 'X');
	    moveToXorY(s1.stepY, 'Y');
	    delayms(500);

	    moveZ();

	}
	return 0;
}

//===================================ISR======================================//

#pragma vector = USCIAB0RX_VECTOR
__interrupt void RX_ISR(void){
    if((IFG2 & UCA0RXIFG) && (IE2 & UCA0RXIE)){
        s1.currentByte = UCA0RXBUF;
        __bic_SR_register_on_exit(LPM0_bits);
    }
}

#pragma vector = TIMER1_A0_VECTOR
__interrupt void TIMER1_ISR(void){            //This interrupt is automatically acknowledged
    if(s1.stepForTimer <= 1){
        TA1CTL = MC_0 + TACLR;                //Stops Timer1 and clears the TA1R register
        __bic_SR_register(LPM0_bits);         //Exit LPM0 upon execution of ISR
    }
    s1.stepForTimer--;
}

#pragma vector = TIMER0_A0_VECTOR
__interrupt void TIMER0_ISR(void){
    if(timeInms <= 1){                          //timeInms varies from (ms to 1)
        TA0CTL = TACLR + MC_0;                  //Stop Timer0
        __bic_SR_register(LPM0_bits);
    }
    timeInms--;
}
//============================================================================//


//=============================Function definition===========================//
void sendString(unsigned char *letterPointer){
    while(*letterPointer){                          //Continue as long as you encounter '\0'
        while(!(IFG2 & UCA0TXIFG));                 //Wait till UCA0TXBUF is available
        UCA0TXBUF = *(letterPointer++);             //Send the current letter and point to the next letter of the word
    }
}

void configPort(){
    //Configuring GPIO

    //Look at intial #defines for each pin and verify the below declarations after every update in code
    P2OUT &= ~(STEPPER_X_PULSE + STEPPER_Y_PULSE + STEPPER_X_DIR + STEPPER_Y_DIR + DC_MOTOR_IN3 + DC_MOTOR_IN4);
    P2DIR |= STEPPER_X_PULSE + STEPPER_Y_PULSE + STEPPER_X_DIR + STEPPER_Y_DIR + DC_MOTOR_IN3 + DC_MOTOR_IN4;       //Declared as Outputs

    //Configuring USCIA0
    P1SEL |=  UART_TX + UART_RX;
    P1SEL2 |= UART_TX + UART_RX;

    //Configuring TA1 Outputs
    P2SEL |= STEPPER_X_PULSE + STEPPER_Y_PULSE;

    P1REN |= ~(UART_TX + UART_RX);      //PORT1 Unused pulled-down
    P1OUT &= UART_TX + UART_RX;


    P2REN |= ~(STEPPER_X_PULSE + STEPPER_Y_PULSE + STEPPER_X_DIR + STEPPER_Y_DIR + DC_MOTOR_IN3 + DC_MOTOR_IN4);        //PORT2 Unused pulled-down
    P2OUT &= STEPPER_X_PULSE + STEPPER_Y_PULSE + STEPPER_X_DIR + STEPPER_Y_DIR + DC_MOTOR_IN3 + DC_MOTOR_IN4;

}

void configUART(){
    //9600 bps, No parity, 8-bit, LSB first,  1 Stop Bit

    UCA0CTL1 = UCSWRST + UCSSEL_2;      //Choose BRCLK from SMCL operating @ 1 MHz

    UCA0BR0 = 104;
    UCA0BR1 = 0;
    UCA0MCTL = UCBRS_1;                 //9600-8-N configuration for UART

    UCA0CTL1 &= ~UCSWRST;
}

void configTimer1(){

    TA1CCR0 = SPEEDM;                   //The duration is SPEEDM microseconds

    TA1CCR1 = SPEEDM>>1;                //OUT1 will control STEPPER_X_PULSE
                                        //This is SPEEDM/2 (bitwise right shift by 1 is approx equal to dividing by 2)

    TA1CCR2 = SPEEDM>>1;                //OUT2 will control STEPPER_Y_PULSE
                                        //This is SPEEDM/2 (bitwise right shift by 1 is approx equal to dividing by 2)
}

void configTimer0(){
    TA0CCR0 = 1000;                     //To generate interrupt every 1 ms
}

void delayms(uint16_t ms){            //Capable of producing delay in range of 1 ms to 65.535 s with a resolution of 1 ms
    timeInms = ms;
    TA0CCTL0 |= CCIE;                       //Enable interrupts for Timer0 channel#0
    TA0CTL = TASSEL_2 + TACLR + MC_1;       //Starts Timer0 in UP mode with clock sourced from SMCLK running @ calibrated 1 MHz
    __bis_SR_register(LPM0_bits);           //Go to sleep untill awaken by Timer0 ISR after specified ms of time
    TA0CCTL0 &= ~CCIE;                      //Disable interrupts for Timer0 channel#0
}

void moveToXorY(int16_t steps, unsigned char XorY){
    if(steps == 0){                                             //Check if steps is 0? if steps == 0 -> quit. Else proceed
        return;
    }else{
        TA1CCTL0 |= CCIE;                                       //Enables interrupt for Timer1 channel#0
                                                                //This interrupt regulates the number of pulses sent to the stepper motor driver
        if(XorY == 'x' || XorY == 'X'){

            if(steps < 0){                                      //If steps is negative, convert it into positive and change the stepper motor's
                steps = -steps;                                 //direction of rotation accordingly
                STEPPER_X_DIR_PXOUT |= STEPPER_X_DIR;           //Direction pin 'HIGH'
            }else{
                STEPPER_X_DIR_PXOUT &= ~STEPPER_X_DIR;          //Direction pin 'LOW'
            }

            s1.stepForTimer = steps;
            TA1CCTL1 = OUTMOD_3;                                //Output mode is Set/Reset; makes OUT1 = 0
                                                                //Note: It is important to keep OUT1 = 0 initially, as it will create rising edge during the first
                                                                //call of timerISR
            TA1CTL = TACLR + MC_1 + TASSEL_2;                   //Clear TA1R; Start in Up mode; Source of Timer - SMCLK running @ calibrated 1 MHz
            __bis_SR_register(LPM0_bits);


        }else{
            if(steps < 0){
                steps = -steps;
                STEPPER_Y_DIR_PXOUT |= STEPPER_Y_DIR;           //Direction pin 'HIGH'
            }else{
                STEPPER_Y_DIR_PXOUT &= ~STEPPER_Y_DIR;          //Direction pin 'LOW'
            }

            s1.stepForTimer = steps;
            TA1CCTL2 = OUTMOD_3;                                //Output mode is Set/Reset makes OUT2 = 0
                                                                //Note it is important to keep OUT2 = 0 initially, as it will create rising edge during the first
                                                                //call of timerISR
            TA1CTL = TACLR + MC_1 + TASSEL_2;                   //Clear TA1R; Start in Up mode; Source of Timer - SMCLK running @ calibrated 1 MHz
            __bis_SR_register(LPM0_bits);

        }

        TA1CCTL0 &= ~CCIE;                                  //Disable further Interrupts in channel#0
    }
}

void moveZ(){
    //Z-axis motion
    DC_MOTOR_IN3_PXOUT |= DC_MOTOR_IN3;         //Motor forward: soldering iron moves towards PCB
    DC_MOTOR_IN4_PXOUT &= ~DC_MOTOR_IN4;
    delayms(DELAYT);

    DC_MOTOR_IN3_PXOUT &= ~DC_MOTOR_IN3;        //Motor OFF: soldering iron touches PCB and lets it solder
    DC_MOTOR_IN4_PXOUT &= ~DC_MOTOR_IN4;
    delayms(TIME_TO_SOLDER);

    DC_MOTOR_IN3_PXOUT &= ~DC_MOTOR_IN3;        //Motor backward: soldering iron goes to rest position
    DC_MOTOR_IN4_PXOUT |= DC_MOTOR_IN4;
    delayms(500);

    DC_MOTOR_IN3_PXOUT &= ~DC_MOTOR_IN3;        //Motor OFF: soldering iron stays in rest position
    DC_MOTOR_IN4_PXOUT &= ~DC_MOTOR_IN4;
    delayms(DELAYT);
}
//===========================================================================//
