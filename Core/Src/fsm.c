/*
 * fsm.c
 * finite state machine parsing programs
 *  Created on: Aug 18, 2021
 *      Author: user
 */

#include "main.h"

void fsm(void) {
	switch (fsm_state) {
		case IDLE:
			break;
		case PROGRAM_RECEIVING:
			ret = receive_program();
			if (ret < 0) {
				uart_printf("Error receiving program\r\n");
				fsm_state = IDLE;
				break;
			}
			uart_printf("Program successfully received!\r\n");
			fsm_state = WAITING_FOR_START;
			break;
		case WAITING_FOR_START:
			break;
		case PROGRAM_EXECUTING:
			break;
	}
}
