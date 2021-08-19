/*
 * utils.h
 *
 *  Created on: Aug 18, 2021
 *      Author: user
 */

#ifndef INC_UTILS_H_
#define INC_UTILS_H_

int receive_program(void);
void uart_interrupt_toggle(int flag);
void uart_printf(const char * format, ...);

uint32_t crc32_bytes(uint8_t *pData,uint32_t uLen);
uint32_t revbit(uint32_t uData);


#define MAX_RECEIVE_CYCLES SYS_CLOCK_FREQ / 1000
#define CRC32_POLYNOMIAL                        ((uint32_t)0xEDB88320)
#define RCC_CRC_BIT                             ((uint32_t)0x00001000)

unsigned int crc32b(unsigned char *message, int len);


int_fast16_t nchars;

#endif /* INC_UTILS_H_ */
