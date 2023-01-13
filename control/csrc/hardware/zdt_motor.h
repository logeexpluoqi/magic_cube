/*
 * @Author: luoqi 
 * @Date: 2022-12-24 13:32:57 
 * @Last Modified by: luoqi
 * @Last Modified time: 2022-12-24 13:34:43
 */

#ifndef _ZDT_MOTOR_H
#define _ZDT_MOTOR_H

#ifdef __cplusplus
 extern "C" {
#endif

#include <stdint.h>

typedef struct
{
    float p;
    float v;
    int32_t enc_pos;
    int32_t pulse_ref;
    uint16_t enc;
    int acc;
    int dir;

    uint8_t div;
    uint8_t block_flag;
    uint8_t zero_flag;
    uint8_t ena;
    int err;
    int (*send)(char *wdata, int len);
    int (*recv)(char *rdata, int len);
} ZdtMotorObj;


#ifdef __cplusplus
 }
#endif

#endif
