/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: pacemaker.h
 *
 * Code generated for Simulink model 'pacemaker'.
 *
 * Model version                  : 1.6
 * Simulink Coder version         : 9.3 (R2020a) 18-Nov-2019
 * C/C++ source code generated on : Wed Nov 20 14:55:39 2024
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: ARM Compatible->ARM Cortex
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#ifndef RTW_HEADER_pacemaker_h_
#define RTW_HEADER_pacemaker_h_
#include <string.h>
#include <stddef.h>
#ifndef pacemaker_COMMON_INCLUDES_
# define pacemaker_COMMON_INCLUDES_
#include "rtwtypes.h"
#include "MW_SCI.h"
#include "MW_digitalIO.h"
#endif                                 /* pacemaker_COMMON_INCLUDES_ */

#include "pacemaker_types.h"

/* Child system includes */
#include "send_params_private.h"
#include "send_params.h"

/* Macros for accessing real-time model data structure */
#ifndef rtmGetErrorStatus
# define rtmGetErrorStatus(rtm)        ((rtm)->errorStatus)
#endif

#ifndef rtmSetErrorStatus
# define rtmSetErrorStatus(rtm, val)   ((rtm)->errorStatus = (val))
#endif

/* Block signals (default storage) */
typedef struct {
  uint32_T TxPinLoc;
  real32_T off_time;
  real32_T off_time_e;                 /* '<Root>/Chart' */
  uint16_T switch_time;
  uint16_T switch_time_n;              /* '<Root>/Chart' */
  uint8_T BytePack[4];                 /* '<S3>/Byte Pack' */
  uint8_T BytePack1[2];                /* '<S3>/Byte Pack1' */
  uint8_T red_enable;                  /* '<Root>/Chart' */
  uint8_T green_enable;                /* '<Root>/Chart' */
  uint8_T blue_enable;                 /* '<Root>/Chart' */
} B_pacemaker_T;

/* Block states (default storage) for system '<Root>' */
typedef struct {
  freedomk64f_SCIRead_pacemaker_T obj; /* '<Root>/Serial Receive' */
  freedomk64f_SCIWrite_pacemake_T obj_p;/* '<S3>/Serial Transmit' */
  freedomk64f_DigitalWrite_pace_T obj_n;/* '<S4>/Digital Write' */
  freedomk64f_DigitalWrite_pace_T obj_e;/* '<S4>/Digital Write1' */
  freedomk64f_DigitalWrite_pace_T obj_g;/* '<S4>/Digital Write2' */
  uint32_T temporalCounter_i1;         /* '<Root>/Chart1' */
  uint8_T is_active_c1_pacemaker;      /* '<Root>/Chart1' */
  uint8_T is_c1_pacemaker;             /* '<Root>/Chart1' */
  uint8_T is_c3_pacemaker;             /* '<Root>/Chart' */
} DW_pacemaker_T;

/* Parameters (default storage) */
struct P_pacemaker_T_ {
  real_T SerialReceive_SampleTime;     /* Expression: -1
                                        * Referenced by: '<Root>/Serial Receive'
                                        */
};

/* Real-time Model Data Structure */
struct tag_RTM_pacemaker_T {
  const char_T *errorStatus;
};

/* Block parameters (default storage) */
extern P_pacemaker_T pacemaker_P;

/* Block signals (default storage) */
extern B_pacemaker_T pacemaker_B;

/* Block states (default storage) */
extern DW_pacemaker_T pacemaker_DW;

/* Model entry point functions */
extern void pacemaker_initialize(void);
extern void pacemaker_step(void);
extern void pacemaker_terminate(void);

/* Real-time Model object */
extern RT_MODEL_pacemaker_T *const pacemaker_M;

/*-
 * The generated code includes comments that allow you to trace directly
 * back to the appropriate location in the model.  The basic format
 * is <system>/block_name, where system is the system number (uniquely
 * assigned by Simulink) and block_name is the name of the block.
 *
 * Use the MATLAB hilite_system command to trace the generated code back
 * to the model.  For example,
 *
 * hilite_system('<S3>')    - opens system 3
 * hilite_system('<S3>/Kp') - opens and selects block Kp which resides in S3
 *
 * Here is the system hierarchy for this model
 *
 * '<Root>' : 'pacemaker'
 * '<S1>'   : 'pacemaker/Chart'
 * '<S2>'   : 'pacemaker/Chart1'
 * '<S3>'   : 'pacemaker/Function-Call Subsystem'
 * '<S4>'   : 'pacemaker/Subsystem'
 */
#endif                                 /* RTW_HEADER_pacemaker_h_ */

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
