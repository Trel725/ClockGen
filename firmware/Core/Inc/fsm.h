/*
 * fsm.h
 *
 *  Created on: Aug 18, 2021
 *      Author: user
 */

#ifndef INC_FSM_H_
#define INC_FSM_H_

enum FSM_STATE{
	IDLE,
	PROGRAM_RECEIVING,
	WAITING_FOR_START,
	PROGRAM_EXECUTING
};

void fsm(void);


#endif /* INC_FSM_H_ */
