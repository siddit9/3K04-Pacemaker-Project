/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: pacemaker.c
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

#include "pacemaker.h"
#include "pacemaker_private.h"

/* Named constants for Chart: '<Root>/Chart' */
#define pacemaker_IN_ECHO_PARAM        ((uint8_T)1U)
#define pacemaker_IN_INITIAL           ((uint8_T)2U)
#define pacemaker_IN_SET_PARAM         ((uint8_T)3U)
#define pacemaker_IN_STANDBY           ((uint8_T)4U)

/* Named constants for Chart: '<Root>/Chart1' */
#define pacemaker_IN_BLUE_ON           ((uint8_T)1U)
#define pacemaker_IN_GREEN_ON          ((uint8_T)2U)
#define pacemaker_IN_OFF               ((uint8_T)3U)
#define pacemaker_IN_RED_ON            ((uint8_T)4U)

/* Block signals (default storage) */
B_pacemaker_T pacemaker_B;

/* Block states (default storage) */
DW_pacemaker_T pacemaker_DW;

/* Real-time model */
RT_MODEL_pacemaker_T pacemaker_M_;
RT_MODEL_pacemaker_T *const pacemaker_M = &pacemaker_M_;

/* Forward declaration for local functions */
static void pacemaker_SystemCore_release_g(const freedomk64f_SCIRead_pacemaker_T
  *obj);
static void pacemaker_SystemCore_delete_g(const freedomk64f_SCIRead_pacemaker_T *
  obj);
static void matlabCodegenHandle_matlabCod_g(freedomk64f_SCIRead_pacemaker_T *obj);
static void pacemaker_SystemCore_release_gd(const
  freedomk64f_DigitalWrite_pace_T *obj);
static void pacemaker_SystemCore_delete_gd(const freedomk64f_DigitalWrite_pace_T
  *obj);
static void matlabCodegenHandle_matlabCo_gd(freedomk64f_DigitalWrite_pace_T *obj);
static void pacemaker_SystemCore_setup_g(freedomk64f_SCIRead_pacemaker_T *obj);
static void pacemaker_SystemCore_release_g(const freedomk64f_SCIRead_pacemaker_T
  *obj)
{
  if ((obj->isInitialized == 1) && obj->isSetupComplete) {
    MW_SCI_Close(obj->MW_SCIHANDLE);
  }
}

static void pacemaker_SystemCore_delete_g(const freedomk64f_SCIRead_pacemaker_T *
  obj)
{
  pacemaker_SystemCore_release_g(obj);
}

static void matlabCodegenHandle_matlabCod_g(freedomk64f_SCIRead_pacemaker_T *obj)
{
  if (!obj->matlabCodegenIsDeleted) {
    obj->matlabCodegenIsDeleted = true;
    pacemaker_SystemCore_delete_g(obj);
  }
}

static void pacemaker_SystemCore_release_gd(const
  freedomk64f_DigitalWrite_pace_T *obj)
{
  if ((obj->isInitialized == 1) && obj->isSetupComplete) {
    MW_digitalIO_close(obj->MW_DIGITALIO_HANDLE);
  }
}

static void pacemaker_SystemCore_delete_gd(const freedomk64f_DigitalWrite_pace_T
  *obj)
{
  pacemaker_SystemCore_release_gd(obj);
}

static void matlabCodegenHandle_matlabCo_gd(freedomk64f_DigitalWrite_pace_T *obj)
{
  if (!obj->matlabCodegenIsDeleted) {
    obj->matlabCodegenIsDeleted = true;
    pacemaker_SystemCore_delete_gd(obj);
  }
}

static void pacemaker_SystemCore_setup_g(freedomk64f_SCIRead_pacemaker_T *obj)
{
  uint32_T SCIModuleLoc;
  MW_SCI_StopBits_Type StopBitsValue;
  MW_SCI_Parity_Type ParityValue;
  obj->isSetupComplete = false;
  obj->isInitialized = 1;
  pacemaker_B.TxPinLoc = MW_UNDEFINED_VALUE;
  SCIModuleLoc = 0;
  obj->MW_SCIHANDLE = MW_SCI_Open(&SCIModuleLoc, false, 10U,
    pacemaker_B.TxPinLoc);
  MW_SCI_SetBaudrate(obj->MW_SCIHANDLE, 115200U);
  StopBitsValue = MW_SCI_STOPBITS_1;
  ParityValue = MW_SCI_PARITY_NONE;
  MW_SCI_SetFrameFormat(obj->MW_SCIHANDLE, 8, ParityValue, StopBitsValue);
  obj->isSetupComplete = true;
}

/* Model step function */
void pacemaker_step(void)
{
  uint8_T RxData[11];
  uint8_T RxDataLocChar[11];
  uint8_T status;
  int32_T rtb_blue_out;
  int32_T rtb_green_out;
  int32_T rtb_red_out;

  /* MATLABSystem: '<Root>/Serial Receive' */
  if (pacemaker_DW.obj.SampleTime != pacemaker_P.SerialReceive_SampleTime) {
    pacemaker_DW.obj.SampleTime = pacemaker_P.SerialReceive_SampleTime;
  }

  status = MW_SCI_Receive(pacemaker_DW.obj.MW_SCIHANDLE, RxDataLocChar, 11U);
  memcpy((void *)&RxData[0], (void *)&RxDataLocChar[0], (uint32_T)((size_t)11 *
          sizeof(uint8_T)));

  /* Chart: '<Root>/Chart' incorporates:
   *  MATLABSystem: '<Root>/Serial Receive'
   */
  switch (pacemaker_DW.is_c3_pacemaker) {
   case pacemaker_IN_ECHO_PARAM:
    pacemaker_DW.is_c3_pacemaker = pacemaker_IN_STANDBY;
    break;

   case pacemaker_IN_INITIAL:
    pacemaker_DW.is_c3_pacemaker = pacemaker_IN_STANDBY;
    break;

   case pacemaker_IN_SET_PARAM:
    pacemaker_DW.is_c3_pacemaker = pacemaker_IN_STANDBY;
    break;

   default:
    /* case IN_STANDBY: */
    if ((status == 0) && (RxData[0] == 1)) {
      switch (RxData[1]) {
       case 2:
        pacemaker_DW.is_c3_pacemaker = pacemaker_IN_SET_PARAM;
        pacemaker_B.red_enable = RxData[2];
        pacemaker_B.green_enable = RxData[3];
        pacemaker_B.blue_enable = RxData[4];
        memcpy((void *)&pacemaker_B.off_time_e, (void *)&RxData[5], (uint32_T)
               ((size_t)1 * sizeof(real32_T)));
        memcpy((void *)&pacemaker_B.switch_time_n, (void *)&RxData[9], (uint32_T)
               ((size_t)1 * sizeof(uint16_T)));
        break;

       case 1:
        pacemaker_DW.is_c3_pacemaker = pacemaker_IN_ECHO_PARAM;
        send_params();
        break;
      }
    }
    break;
  }

  /* End of Chart: '<Root>/Chart' */

  /* Chart: '<Root>/Chart1' */
  if (pacemaker_DW.temporalCounter_i1 < MAX_uint32_T) {
    pacemaker_DW.temporalCounter_i1++;
  }

  if (pacemaker_DW.is_active_c1_pacemaker == 0U) {
    pacemaker_DW.is_active_c1_pacemaker = 1U;
    pacemaker_DW.is_c1_pacemaker = pacemaker_IN_OFF;
    pacemaker_DW.temporalCounter_i1 = 0U;
    rtb_red_out = 0;
    rtb_green_out = 0;
    rtb_blue_out = 0;
    send_params();
  } else {
    switch (pacemaker_DW.is_c1_pacemaker) {
     case pacemaker_IN_BLUE_ON:
      rtb_red_out = 0;
      rtb_green_out = 0;
      rtb_blue_out = 1;
      if (pacemaker_DW.temporalCounter_i1 >= pacemaker_B.switch_time_n) {
        pacemaker_DW.is_c1_pacemaker = pacemaker_IN_OFF;
        pacemaker_DW.temporalCounter_i1 = 0U;
        rtb_blue_out = 0;
        send_params();
      }
      break;

     case pacemaker_IN_GREEN_ON:
      rtb_red_out = 0;
      rtb_green_out = 1;
      rtb_blue_out = 0;
      if (pacemaker_DW.temporalCounter_i1 >= pacemaker_B.switch_time_n) {
        if (pacemaker_B.blue_enable == 1) {
          pacemaker_DW.is_c1_pacemaker = pacemaker_IN_BLUE_ON;
          pacemaker_DW.temporalCounter_i1 = 0U;
          rtb_green_out = 0;
          rtb_blue_out = 1;
        } else {
          pacemaker_DW.is_c1_pacemaker = pacemaker_IN_OFF;
          pacemaker_DW.temporalCounter_i1 = 0U;
          rtb_green_out = 0;
          send_params();
        }
      }
      break;

     case pacemaker_IN_OFF:
      rtb_red_out = 0;
      rtb_green_out = 0;
      rtb_blue_out = 0;
      if (pacemaker_DW.temporalCounter_i1 >= pacemaker_B.off_time_e * 1000.0F) {
        if (pacemaker_B.red_enable == 1) {
          pacemaker_DW.is_c1_pacemaker = pacemaker_IN_RED_ON;
          pacemaker_DW.temporalCounter_i1 = 0U;
          rtb_red_out = 1;
        } else if (pacemaker_B.green_enable == 1) {
          pacemaker_DW.is_c1_pacemaker = pacemaker_IN_GREEN_ON;
          pacemaker_DW.temporalCounter_i1 = 0U;
          rtb_green_out = 1;
        } else if (pacemaker_B.blue_enable == 1) {
          pacemaker_DW.is_c1_pacemaker = pacemaker_IN_BLUE_ON;
          pacemaker_DW.temporalCounter_i1 = 0U;
          rtb_blue_out = 1;
        } else {
          pacemaker_DW.is_c1_pacemaker = pacemaker_IN_OFF;
          pacemaker_DW.temporalCounter_i1 = 0U;
          send_params();
        }
      }
      break;

     default:
      /* case IN_RED_ON: */
      rtb_red_out = 1;
      rtb_green_out = 0;
      rtb_blue_out = 0;
      if (pacemaker_DW.temporalCounter_i1 >= pacemaker_B.switch_time_n) {
        if (pacemaker_B.green_enable == 1) {
          pacemaker_DW.is_c1_pacemaker = pacemaker_IN_GREEN_ON;
          pacemaker_DW.temporalCounter_i1 = 0U;
          rtb_red_out = 0;
          rtb_green_out = 1;
        } else if (pacemaker_B.blue_enable == 1) {
          pacemaker_DW.is_c1_pacemaker = pacemaker_IN_BLUE_ON;
          pacemaker_DW.temporalCounter_i1 = 0U;
          rtb_red_out = 0;
          rtb_blue_out = 1;
        } else {
          pacemaker_DW.is_c1_pacemaker = pacemaker_IN_OFF;
          pacemaker_DW.temporalCounter_i1 = 0U;
          rtb_red_out = 0;
          send_params();
        }
      }
      break;
    }
  }

  /* End of Chart: '<Root>/Chart1' */

  /* MATLABSystem: '<S4>/Digital Write' */
  MW_digitalIO_write(pacemaker_DW.obj_n.MW_DIGITALIO_HANDLE, rtb_red_out != 0);

  /* MATLABSystem: '<S4>/Digital Write1' */
  MW_digitalIO_write(pacemaker_DW.obj_e.MW_DIGITALIO_HANDLE, rtb_green_out != 0);

  /* MATLABSystem: '<S4>/Digital Write2' */
  MW_digitalIO_write(pacemaker_DW.obj_g.MW_DIGITALIO_HANDLE, rtb_blue_out != 0);
}

/* Model initialize function */
void pacemaker_initialize(void)
{
  {
    freedomk64f_DigitalWrite_pace_T *obj;

    /* Chart: '<Root>/Chart' */
    pacemaker_DW.is_c3_pacemaker = pacemaker_IN_INITIAL;
    pacemaker_B.off_time_e = 0.5F;
    pacemaker_B.switch_time_n = 200U;

    /* SystemInitialize for S-Function (sfun_private_function_caller) generated from: '<Root>/Function-Call Subsystem' incorporates:
     *  SubSystem: '<Root>/Function-Call Subsystem'
     */
    send_params_Init();

    /* End of SystemInitialize for S-Function (sfun_private_function_caller) generated from: '<Root>/Function-Call Subsystem' */

    /* Start for MATLABSystem: '<Root>/Serial Receive' */
    pacemaker_DW.obj.isInitialized = 0;
    pacemaker_DW.obj.matlabCodegenIsDeleted = false;
    pacemaker_DW.obj.SampleTime = pacemaker_P.SerialReceive_SampleTime;
    pacemaker_SystemCore_setup_g(&pacemaker_DW.obj);

    /* Start for MATLABSystem: '<S4>/Digital Write' */
    pacemaker_DW.obj_n.matlabCodegenIsDeleted = true;
    pacemaker_DW.obj_n.isInitialized = 0;
    pacemaker_DW.obj_n.matlabCodegenIsDeleted = false;
    obj = &pacemaker_DW.obj_n;
    pacemaker_DW.obj_n.isSetupComplete = false;
    pacemaker_DW.obj_n.isInitialized = 1;
    obj->MW_DIGITALIO_HANDLE = MW_digitalIO_open(42U, 1);
    pacemaker_DW.obj_n.isSetupComplete = true;

    /* Start for MATLABSystem: '<S4>/Digital Write1' */
    pacemaker_DW.obj_e.matlabCodegenIsDeleted = true;
    pacemaker_DW.obj_e.isInitialized = 0;
    pacemaker_DW.obj_e.matlabCodegenIsDeleted = false;
    obj = &pacemaker_DW.obj_e;
    pacemaker_DW.obj_e.isSetupComplete = false;
    pacemaker_DW.obj_e.isInitialized = 1;
    obj->MW_DIGITALIO_HANDLE = MW_digitalIO_open(43U, 1);
    pacemaker_DW.obj_e.isSetupComplete = true;

    /* Start for MATLABSystem: '<S4>/Digital Write2' */
    pacemaker_DW.obj_g.matlabCodegenIsDeleted = true;
    pacemaker_DW.obj_g.isInitialized = 0;
    pacemaker_DW.obj_g.matlabCodegenIsDeleted = false;
    obj = &pacemaker_DW.obj_g;
    pacemaker_DW.obj_g.isSetupComplete = false;
    pacemaker_DW.obj_g.isInitialized = 1;
    obj->MW_DIGITALIO_HANDLE = MW_digitalIO_open(44U, 1);
    pacemaker_DW.obj_g.isSetupComplete = true;
  }
}

/* Model terminate function */
void pacemaker_terminate(void)
{
  /* Terminate for MATLABSystem: '<Root>/Serial Receive' */
  matlabCodegenHandle_matlabCod_g(&pacemaker_DW.obj);

  /* Terminate for S-Function (sfun_private_function_caller) generated from: '<Root>/Function-Call Subsystem' incorporates:
   *  SubSystem: '<Root>/Function-Call Subsystem'
   */
  send_params_Term();

  /* End of Terminate for S-Function (sfun_private_function_caller) generated from: '<Root>/Function-Call Subsystem' */

  /* Terminate for MATLABSystem: '<S4>/Digital Write' */
  matlabCodegenHandle_matlabCo_gd(&pacemaker_DW.obj_n);

  /* Terminate for MATLABSystem: '<S4>/Digital Write1' */
  matlabCodegenHandle_matlabCo_gd(&pacemaker_DW.obj_e);

  /* Terminate for MATLABSystem: '<S4>/Digital Write2' */
  matlabCodegenHandle_matlabCo_gd(&pacemaker_DW.obj_g);
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
