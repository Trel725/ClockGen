/*
 * exec.c
 *
 *  Created on: Aug 19, 2021
 *      Author: user
 */

#include "main.h"

void start_execution(void){
	uart_printf("Starting program execution...");
	uart_interrupt_toggle(0);
	progbuftop=0;
	tick_timer_toggle(1);
}

inline void exec_irq_handler(void) {
	uint32_t volatile * addr;
	uint32_t value;
	/*
	 * progbuf structure: u32 time, u32 addr, u32 value
	 * uC must write value by addr at specified time
	 */
	if (progbuffer[progbuftop] == current_us) {
		progbuftop++;
		while (1) {
			addr = (uint32_t volatile*) progbuffer[progbuftop++];
			if (addr == END_OF_COMMAND)
				break;
			value = progbuffer[progbuftop++];
			*addr = value;
		}
		return;
	}
	if(progbuffer[progbuftop] == TICK_TIMER_MAX){
		stop_exec_handler();
	}
}

void stop_exec_handler(void){
	tick_timer_toggle(0);
	reset_timers_gpio();
	progbuftop = 0;
	current_us = 0;
	fsm_state = IDLE;
	uart_interrupt_toggle(1);
}
