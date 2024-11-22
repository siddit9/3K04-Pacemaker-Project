/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: send_params.c
 *
 * Code generated for Simulink model 'pacemaker'.
 *
 * Model version                  : 1.6
 * Simulink Coder version         : 9.3 (R2020a) 18-Nov-2019
 * C/C++ source code generated on : Wed Nov 20 16:53:43 2024
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: ARM Compatible->ARM Cortex
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "send_params.h"

/* Include model header file for global data */
#include "pacemaker.h"
#include "pacemaker_private.h"

/* Forward declaration for local functions */
static void pacemaker_SystemCore_setup(freedomk64f_SCIWrite_pacemake_T *obj);
static void pacemaker_SystemCore_release(const freedomk64f_SCIWrite_pacemake_T
  *obj);
static void pacemaker_SystemCore_delete(const freedomk64f_SCIWrite_pacemake_T
  *obj);
static void matlabCodegenHandle_matlabCodeg(freedomk64f_SCIWrite_pacemake_T *obj);
static void pacemaker_SystemCore_setup(freedomk64f_SCIWrite_pacemake_T *obj)
{
  uint32_T RxPinLoc;
  uint32_T SCIModuleLoc;
  MW_SCI_StopBits_Type StopBitsValue;
  MW_SCI_Parity_Type ParityValue;
  obj->isSetupComplete = false;
  obj->isInitialized = 1;
  RxPinLoc = MW_UNDEFINED_VALUE;
  SCIModuleLoc = 0;
  obj->MW_SCIHANDLE = MW_SCI_Open(&SCIModuleLoc, false, RxPinLoc, 10U);
  MW_SCI_SetBaudrate(obj->MW_SCIHANDLE, 115200U);
  StopBitsValue = MW_SCI_STOPBITS_1;
  ParityValue = MW_SCI_PARITY_NONE;
  MW_SCI_SetFrameFormat(obj->MW_SCIHANDLE, 8, ParityValue, StopBitsValue);
  obj->isSetupComplete = true;
}

static void pacemaker_SystemCore_release(const freedomk64f_SCIWrite_pacemake_T
  *obj)
{
  if ((obj->isInitialized == 1) && obj->isSetupComplete) {
    MW_SCI_Close(obj->MW_SCIHANDLE);
  }
}

static void pacemaker_SystemCore_delete(const freedomk64f_SCIWrite_pacemake_T
  *obj)
{
  pacemaker_SystemCore_release(obj);
}

static void matlabCodegenHandle_matlabCodeg(freedomk64f_SCIWrite_pacemake_T *obj)
{
  if (!obj->matlabCodegenIsDeleted) {
    obj->matlabCodegenIsDeleted = true;
    pacemaker_SystemCore_delete(obj);
  }
}

/* System initialize for Simulink Function: '<Root>/Function-Call Subsystem' */
void send_params_Init(void)
{
  /* Start for MATLABSystem: '<S3>/Serial Transmit' */
  pacemaker_DW.obj_p.isInitialized = 0;
  pacemaker_DW.obj_p.matlabCodegenIsDeleted = false;
  pacemaker_SystemCore_setup(&pacemaker_DW.obj_p);
}

/* Output and update for Simulink Function: '<Root>/Function-Call Subsystem' */
void send_params(void)
{
  uint8_T status;
  uint8_T TxDataLocChar[9];
  uint8_T rtb_TmpSignalConversionAtSerial[9];

  /* SignalConversion generated from: '<S3>/off_time' */
  pacemaker_B.off_time = pacemaker_B.off_time_e;

  /* SignalConversion generated from: '<S3>/switch_time' */
  pacemaker_B.switch_time = pacemaker_B.switch_time_n;

  /* S-Function (any2byte): '<S3>/Byte Pack' */

  /* Pack: <S3>/Byte Pack */
  (void) memcpy(&pacemaker_B.BytePack[0], &pacemaker_B.off_time,
                4);

  /* S-Function (any2byte): '<S3>/Byte Pack1' */

  /* Pack: <S3>/Byte Pack1 */
  (void) memcpy(&pacemaker_B.BytePack1[0], &pacemaker_B.switch_time,
                2);

  /* SignalConversion generated from: '<S3>/Serial Transmit' incorporates:
   *  SignalConversion generated from: '<S3>/blue_enable'
   *  SignalConversion generated from: '<S3>/green_enable'
   *  SignalConversion generated from: '<S3>/red_enable'
   */
  rtb_TmpSignalConversionAtSerial[0] = pacemaker_B.red_enable;
  rtb_TmpSignalConversionAtSerial[1] = pacemaker_B.green_enable;
  rtb_TmpSignalConversionAtSerial[2] = pacemaker_B.blue_enable;
  rtb_TmpSignalConversionAtSerial[3] = pacemaker_B.BytePack[0];
  rtb_TmpSignalConversionAtSerial[4] = pacemaker_B.BytePack[1];
  rtb_TmpSignalConversionAtSerial[5] = pacemaker_B.BytePack[2];
  rtb_TmpSignalConversionAtSerial[6] = pacemaker_B.BytePack[3];
  rtb_TmpSignalConversionAtSerial[7] = pacemaker_B.BytePack1[0];
  rtb_TmpSignalConversionAtSerial[8] = pacemaker_B.BytePack1[1];

  /* MATLABSystem: '<S3>/Serial Transmit' */
  status = 1U;
  while (status != 0) {
    memcpy((void *)&TxDataLocChar[0], (void *)&rtb_TmpSignalConversionAtSerial[0],
           (uint32_T)((size_t)9 * sizeof(uint8_T)));
    status = MW_SCI_Transmit(pacemaker_DW.obj_p.MW_SCIHANDLE, TxDataLocChar, 9U);
  }

  /* End of MATLABSystem: '<S3>/Serial Transmit' */
}

/* Termination for Simulink Function: '<Root>/Function-Call Subsystem' */
void send_params_Term(void)
{
  /* Terminate for MATLABSystem: '<S3>/Serial Transmit' */
  matlabCodegenHandle_matlabCodeg(&pacemaker_DW.obj_p);
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
