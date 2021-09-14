/*
 * utils.c
 *
 *  Created on: Aug 18, 2021
 *      Author: user
 */

#include "main.h"
#include <stdio.h>
#include <stdarg.h>

/*
 * @brief stop all timers, set all gpio to 0
 */
void reset_timers_gpio(void){
	TIM1->CR1 = 0;
	TIM2->CR1 = 0;
	TIM3->CR1 = 0;
	TIM4->CR1 = 0;
	TIM5->CR1 = 0;
	TIM8->CR1 = 0;
	TIM10->CR1 = 0;
	TIM11->CR1 = 0;
	TIM12->CR1 = 0;
	TIM13->CR1 = 0;
	TIM14->CR1 = 0;

	GPIOA->ODR = 0;
	GPIOB->ODR = 0;
	GPIOC->ODR = 0;

}

/**
 * @brief converts 4 bytes to int
 */
inline uint32_t bytes_to_int(uint8_t * bytes){
	return bytes[0] + (bytes[1] << 8) + (bytes[2] << 16) + (bytes[3] << 24);
}

/**
 * @brief enables/disables TICK_TIMER interrupts
 */
void tick_timer_toggle(int flag){
	if(flag){
		//enable tick timer, enable its interrupt
		TICK_TIMER->CR1 |= TIM_CR1_CEN;
		TICK_TIMER->DIER |= TIM_DIER_UIE;
		return;
	}
	//disable timer, interrupts, reset it
	TICK_TIMER->CR1 &= ~TIM_CR1_CEN;
	TICK_TIMER->DIER  &= ~ TIM_DIER_UIE;
	TICK_TIMER->CNT = 0;
}

/**
 * @brief enables/disables UART interrupts
 */
void uart_interrupt_toggle(int flag) {
	if (flag) {
		UART_MAIN_HANDLE.Instance->CR1 |= USART_CR1_RXNEIE;
		return;
	}
	UART_MAIN_HANDLE.Instance->CR1 &= ~USART_CR1_RXNEIE;
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
