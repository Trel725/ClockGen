/*
 * comm.c
 * describes communication with host
 *  Created on: Aug 19, 2021
 *      Author: user
 */


#include "main.h"


/*
 * @brief performs program receiving from host
 * initialized by getting START_OF_PROGRAM_BYTE
 * end when flow have stopped (when counter, reset after each received byte gets > MAX_RECEIVE_CYCLES)
 * @ret 0 is success, negative if error
 */
int receive_program(void) {
	//reset uart buffer
	uartrecbufftop = 0;
	//disable interrupt handler
	uart_interrupt_toggle(0);
	// use progbuffer as u8 for now
	uint8_t * buffer = (uint8_t *) progbuffer;
	uint16_t bufftop = 0;
	uint8_t curr_byte;
	// initialzie counter so that we wont get stuck into infinite loop
	int counter = 0;
	do {
		counter++;
		if ( USART2->SR & USART_SR_RXNE) {
			// save the data to the buffer
			curr_byte = (USART2->DR & USART_DR_DR);
			buffer[bufftop] = curr_byte;
			bufftop++;
			// if host tries to send more than we can handle
			if (bufftop >= MAX_PROGRAMM_SIZE*sizeof(uint32_t)) {
				uart_printf(
						"Receiving buffer overflow, program is too big!\r\n");
				bufftop = 0;
				uart_interrupt_toggle(1);
				return -1;
			}
			counter = 0;
		}
	} while (counter < MAX_RECEIVE_CYCLES);
	// if something went wrong and we did not receive enough bytes,
	// exit earlier to prevent memory smashing+
	if(bufftop < 5){
		goto EXIT_W_ERROR;
	}
	uint32_t received_crc = buffer[bufftop - 5] + (buffer[bufftop - 4] << 8) + (buffer[bufftop - 3] << 16) + (buffer[bufftop - 2] << 24);
	uint32_t crc = crc32_bytes(buffer, bufftop - 5);
	if (received_crc != crc){
	    EXIT_W_ERROR:
		uart_printf("Control sum mismatch!\r\n");
		uart_interrupt_toggle(1);
		return -1;

	}

	uart_interrupt_toggle(1);
	return 0;
}


/*
 * @brief performs program receiving from host
 * initialized by getting START_OF_PROGRAM_BYTE
 * end by receiving END_OF_PROGRAM_BYTE
 * @ret 0 is success, negative if error
 */

/*
int receive_program_endbyte(void) {
	uint_fast8_t curr_byte;
	//disable interrupt handler
	uart_interrupt_toggle(0);
	// set receive buffer to 0
	uartrecbufftop = 0;
	// initialzie counter so that we wont get stuck into infinite loop
	int counter = 0;
	do {
		counter++;
		if ( USART2->SR & USART_SR_RXNE) {
			// save the data to the buffer
			curr_byte = (USART2->DR & USART_DR_DR);
			uartrecbuffer[uartrecbufftop] = curr_byte;
			uartrecbufftop++;
			// if host tries to send more than we can handle
			if (uartrecbufftop == UART_RECEIVE_BUF_SIZE) {
				uart_printf(
						"Receiving buffer overflow, program is too big!\r\n");
				uart_interrupt_toggle(1);
				return -1;
			}
		}
		// if receiving is too long probably we missed end of program byte somewhere
		if (counter >= MAX_RECEIVE_CYCLES) {
			uart_printf("Can't find end of program, rejecting...!\r\n");
			uart_interrupt_toggle(1);
			return -1;
		}
	} while (curr_byte != END_OF_PROGRAMM_BYTE);
	// at uartrecbuffer[uartrecbufftop - 1] lies END_OF_PROGRAMM_BYTE
	uint32_t received_crc = uartrecbuffer[uartrecbufftop - 5] + (uartrecbuffer[uartrecbufftop - 4] << 8) + (uartrecbuffer[uartrecbufftop - 3] << 16) + (uartrecbuffer[uartrecbufftop - 2] << 24);
	uint32_t crc = crc32_bytes(uartrecbuffer, uartrecbufftop - 5);
	if (received_crc != crc){
		uart_printf("Control sum mismatch!\r\n");
		uart_interrupt_toggle(1);
		return -1;

	}

	uart_interrupt_toggle(1);
	return 0;
}
*/
