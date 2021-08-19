/*
 * extramain.h
 *
 *  Created on: Aug 18, 2021
 *      Author: user
 */

#ifndef INC_EXTRAMAIN_H_
#define INC_EXTRAMAIN_H_

#include "fsm.h"

// hardware handles
CRC_HandleTypeDef hcrc;
TIM_HandleTypeDef htim1;
TIM_HandleTypeDef htim2;
TIM_HandleTypeDef htim3;
TIM_HandleTypeDef htim4;
TIM_HandleTypeDef htim5;
TIM_HandleTypeDef htim6;
TIM_HandleTypeDef htim8;
TIM_HandleTypeDef htim10;
TIM_HandleTypeDef htim11;
TIM_HandleTypeDef htim13;
TIM_HandleTypeDef htim14;
UART_HandleTypeDef huart2;

// function prototypes

// constants
#define UART_RECEIVE_BUF_SIZE 1024
#define END_RECEIVE_CHAR '\r'
#define UART_SEND_BUF_SIZE 1024
#define MAX_PROGRAMM_SIZE 4096
#define START_OF_PROGRAM_BYTE 0x11
#define END_OF_PROGRAMM_BYTE 0xA0

#define TICK_TIMER TIM6

//buffers
uint8_t uartrecbuffer[UART_RECEIVE_BUF_SIZE];
uint8_t uartsendbuffer[UART_SEND_BUF_SIZE];
uint_fast32_t programm_buffer[MAX_PROGRAMM_SIZE];

//state flags
enum FSM_STATE fsm_state;
int_fast8_t uart_receive_end;
uint_fast32_t current_us;

//variables
uint_fast16_t uartrecbufftop;
uint_fast16_t progbuftop;
int ret; // function returns


#endif /* INC_EXTRAMAIN_H_ */
