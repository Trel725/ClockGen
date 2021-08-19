/*
 * extramain.h
 *
 *  Created on: Aug 18, 2021
 *      Author: user
 */

#ifndef INC_EXTRAMAIN_H_
#define INC_EXTRAMAIN_H_

#include "fsm.h"
#include "exec.h"
#include "utils.h"
#include "comm.h"


// hardware
#define TICK_TIMER TIM6
#define UART_MAIN_HANDLE huart2

//hardware handles
UART_HandleTypeDef huart2;

// function prototypes

// constants
#define UART_RECEIVE_BUF_SIZE 1024
#define END_RECEIVE_CHAR '\r'
#define UART_SEND_BUF_SIZE 1024
#define MAX_PROGRAMM_SIZE 16384
#define START_OF_PROGRAM_BYTE 0x11
#define END_OF_PROGRAMM_BYTE 0xA0
#define START_EXEC_BYTE 0xC6
#define END_OF_COMMAND 0xABBCCDDE
#define TICK_TIMER_MAX 0xFFFFFFFF


//buffers
uint8_t uartrecbuffer[UART_RECEIVE_BUF_SIZE];
uint8_t uartsendbuffer[UART_SEND_BUF_SIZE];
uint_fast32_t progbuffer[MAX_PROGRAMM_SIZE];

//state flags
enum FSM_STATE fsm_state;
int_fast8_t uart_receive_end;

//variables
uint_fast16_t uartrecbufftop;
uint_fast16_t progbuftop;
uint_fast32_t current_us;
int ret; // function returns


#endif /* INC_EXTRAMAIN_H_ */
