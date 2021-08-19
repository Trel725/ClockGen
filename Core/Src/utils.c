/*
 * utils.c
 *
 *  Created on: Aug 18, 2021
 *      Author: user
 */

#include "main.h"
#include "utils.h"
#include <stdio.h>
#include <stdarg.h>

/*
 * @brief performs program receiving from host
 * initialized by getting START_OF_PROGRAM_BYTE
 * end by receiving END_OF_PROGRAM_BYTE
 * @ret 0 is success, negative if error
 */
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


/*
 * @brief performs program receiving from host
 * initialized by getting START_OF_PROGRAM_BYTE
 * end when flow have stopped (when counter, reset after each received byte gets > MAX_RECEIVE_CYCLES)
 * @ret 0 is success, negative if error
 */
int receive_program(void) {
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
			if (uartrecbufftop >= UART_RECEIVE_BUF_SIZE) {
				uart_printf(
						"Receiving buffer overflow, program is too big!\r\n");
				uartrecbufftop = 0;
				uart_interrupt_toggle(1);
				return -1;
			}
			counter = 0;
		}
	} while (counter < MAX_RECEIVE_CYCLES);
	// if something went wrong and we did not receive enough bytes,
	// exit earlier to prevent memory smashing+
	if(uartrecbufftop < 5){
		goto EXIT_W_ERROR;
	}
	uint32_t received_crc = uartrecbuffer[uartrecbufftop - 5] + (uartrecbuffer[uartrecbufftop - 4] << 8) + (uartrecbuffer[uartrecbufftop - 3] << 16) + (uartrecbuffer[uartrecbufftop - 2] << 24);
	uint32_t crc = crc32_bytes(uartrecbuffer, uartrecbufftop - 5);
	if (received_crc != crc){
	    EXIT_W_ERROR:
		uart_printf("Control sum mismatch!\r\n");
		uart_interrupt_toggle(1);
		return -1;

	}

	uart_interrupt_toggle(1);
	return 0;
}

/**
 * @brief enables/disables UART interrupts
 */
void uart_interrupt_toggle(int flag) {
	if (flag) {
		huart2.Instance->CR1 |= USART_CR1_RXNEIE;
		return;
	}
	huart2.Instance->CR1 &= ~USART_CR1_RXNEIE;
}

/**
 * @brief printf by uart
 * @retval None
 */
void uart_printf(const char *format, ...) {
	va_list args;
	va_start(args, format);
	nchars = vsnprintf(uartsendbuffer, UART_SEND_BUF_SIZE - 1, format, args);
	HAL_UART_Transmit(&huart2, uartsendbuffer, nchars, HAL_TIMEOUT);
	va_end(args);
}

/**
 * @brief  Calc CRC32 for data in bytes
 * @param  pData Buffer pointer
 * @param  uLen  Buffer Length
 * @retval CRC32 Checksum
 * from https://stackoverflow.com/questions/39646441/how-to-set-stm32-to-generate-standard-crc32
 */
uint32_t crc32_bytes(uint8_t *pData, uint32_t uLen) {
	uint32_t uIndex = 0, uData = 0, i;
	uIndex = uLen >> 2;

	/* Reset CRC generator */
	CRC->CR |= CRC_CR_RESET;

	while (uIndex--) {
#ifdef USED_BIG_ENDIAN
        uData = __REV((uint32_t*)pData);
#else
		((uint8_t*) &uData)[0] = pData[0];
		((uint8_t*) &uData)[1] = pData[1];
		((uint8_t*) &uData)[2] = pData[2];
		((uint8_t*) &uData)[3] = pData[3];
#endif
		pData += 4;
		uData = revbit(uData);
		CRC->DR = uData;
	}
	uData = revbit(CRC->DR);
	uIndex = uLen & 0x03;
	while (uIndex--) {
		uData ^= (uint32_t) *pData++;
		for (i = 0; i < 8; i++)
			if (uData & 0x1)
				uData = (uData >> 1) ^ CRC32_POLYNOMIAL;
			else
				uData >>= 1;
	}
	return uData ^ 0xFFFFFFFF;
}

uint32_t revbit(uint32_t uData) {
	uint32_t uRevData = 0, uIndex = 0;
	uRevData |= ((uData >> uIndex) & 0x01);
	for (uIndex = 1; uIndex < 32; uIndex++) {
		uRevData <<= 1;
		uRevData |= ((uData >> uIndex) & 0x01);
	}
	return uRevData;
}
