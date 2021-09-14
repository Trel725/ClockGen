/*
 * utils.h
 *
 *  Created on: Aug 18, 2021
 *      Author: user
 */

#ifndef INC_UTILS_H_
#define INC_UTILS_H_

#define MAX_RECEIVE_CYCLES SYS_CLOCK_FREQ / 1000
#define CRC32_POLYNOMIAL                        ((uint32_t)0xEDB88320)
#define RCC_CRC_BIT                             ((uint32_t)0x00001000)

void uart_printf(const char * format, ...);
uint32_t crc32_bytes(uint8_t *pData,uint32_t uLen);
uint32_t revbit(uint32_t uData);
inline uint32_t bytes_to_int(uint8_t * bytes);
void uart_interrupt_toggle(int flag);
void tick_timer_toggle(int flag);
void reset_timers_gpio(void);



int_fast16_t nchars;

#endif /* INC_UTILS_H_ */
