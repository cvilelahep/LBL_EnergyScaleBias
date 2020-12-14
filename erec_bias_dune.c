#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdbool.h>

#include <globes/globes.h>   /* GLoBES library */

enum projection {dcp_th13, sinsqth23_dmsq32};

int main(int argc, char ** argv){

  enum projection this_projection;
  bool this_profile;
  double this_e_shift;

  double delta_cp_override = -1000;
  
  if (argc >= 4){

    if (strcmp(argv[1], "dcp_th13") == 0) this_projection = dcp_th13;
    else if (strcmp(argv[1], "sinsqth23_dmsq32") == 0) this_projection = sinsqth23_dmsq32;
    else {
      printf("PROJECTION must be dcp_th13 or sinsqth23_dmsq32\n");
      return -1;
    }

    if (!strcmp(argv[2], "0")) this_profile = false;
    else if (!strcmp(argv[2], "1")) this_profile = true;
    else {
      printf("PROFILE must be 0 or 1");
      return -1;
    }

    this_e_shift = atof(argv[3]);

    if (argc >=5) delta_cp_override = atof(argv[4]);
    
  } else {
    printf("Usage: erec_bias_dune PROJECTION PROFILE E_SHIFT [deltacp]\n");
    printf("PROJECTION: dcp_th13 or sinsqth23_dmsq32\n");
    printf("PROFILE: 1 to profile over other oscillation parameters, 0 to fix at true value\n");
    printf("E_SHIFT: fractional energy bias\n");
    printf("deltacp: value of deltacp, optional\n");
    return -1;
  }

  printf("Projection");
  if (this_projection == dcp_th13) printf(" dcp_th13\n");
  else if (this_projection == sinsqth23_dmsq32) printf(" sinsqth23_dmsq32\n");
  printf("Profile %s\n", argv[2]);
  printf("Energy scale shift %f\n", this_e_shift);
  printf("Energy scale shift %f\n", this_e_shift);
  printf("--------------------------------------------------------------------------------\n");
  
  glbInit("erec_bias_dune");
  glbInitExperiment("DUNE_GLoBES.glb", &glb_experiment_list[0],&glb_num_of_exps); 

  /* Define "true" oscillation parameters */
  // nu-fit 5.0 (July 2020) w/SK NO
  double theta12 = 0.5836;
  double theta13 = 0.1496;
  double theta23 = 0.8587;
  //double deltacp = 3.438; // nu-fit 5.0
  double deltacp = 1.396; // Missing energy paper
  double sdm = 7.42e-5;
  double ldm = 2.517e-3;

  if (delta_cp_override > -999) deltacp = delta_cp_override;
  
  // Contour grid
  /* Scan the th13-delta plane */
  double th13_lower  = 0.1387;
  double th13_upper  = 0.1650;
  double th13_steps  = 50;

  double delta_lower = 0;
  double delta_upper = 6.2832;
  double delta_steps = 50;

  double th23_lower  = 0.6331;
  double th23_upper  = 0.9377;
  double th23_steps  = 50;

  double ldm_lower = 2.35e-3;
  double ldm_upper = 2.55e-3;
  double ldm_steps = 50;
  
  /* Define "true" oscillation parameter vector */
  glb_params true_values = glbAllocParams();
  glbDefineParams(true_values,theta12,theta13,theta23,deltacp,sdm,ldm);
  glbSetDensityParams(true_values,1.0,GLB_ALL);
 
  /* Define initial guess for the fit values */ 
  glb_params test_values = glbAllocParams();
  glbDefineParams(test_values,theta12,theta13,theta23,deltacp,sdm,ldm);  
  glbSetDensityParams(test_values,1.0,GLB_ALL);

  glb_params input_errors = glbAllocParams();
  glbDefineParams(input_errors, theta12*0.1, 0, 0, 0, sdm*0.1, 0);
  glbSetDensityParams(input_errors,0.05,GLB_ALL);
  glbSetInputErrors(input_errors);
  glbSetCentralValues(true_values);

  /* Define projection onto th13 and delta, marginalizing over
   * th23 and dm31. The solar parameters can be kept fixed to speed
   * up the calculation without introducing large errors. */
  glb_projection globes_projection = glbAllocProjection();

  if (!this_profile) {
    // theta12, theta13,theta23,
    // delta, dms, dma
    glbDefineProjection(globes_projection,
			GLB_FIXED,GLB_FIXED,GLB_FIXED,
                        GLB_FIXED,GLB_FIXED,GLB_FIXED);
  } else if (this_projection == dcp_th13) {
    glbDefineProjection(globes_projection,
			GLB_FIXED,GLB_FIXED,GLB_FREE,
			GLB_FIXED,GLB_FIXED,GLB_FREE);
  } else if (this_projection == sinsqth23_dmsq32) {
    glbDefineProjection(globes_projection,
			GLB_FIXED,GLB_FREE,GLB_FIXED,
			GLB_FREE,GLB_FIXED,GLB_FIXED);
  }

  //                                             NOT SURE WHAT THIS DOES, but doesn't seem to affect contours. CHECK!
  glbSetDensityProjectionFlag(globes_projection, GLB_FIXED, GLB_ALL);
  glbSetProjection(globes_projection);  
  
  /* Compute simulated data */
  glbSetOscillationParameters(true_values);
  glbSetRates();

  // Apply energy scale shift. For now, just take the total rate histograms and shift them.
  double emin, emax;
  glbGetEminEmax(0, &emin, &emax);
  int n_bins = glbGetNumberOfBins(0);
  double signal_fit_rates_N[n_bins];
  
  for (int irule = 0; irule < 4; irule++){
    double * rate = glbGetRuleRatePtr(0, irule);
    glbShiftEnergyScale(this_e_shift, rate ,signal_fit_rates_N, n_bins, emin, emax);
    for (int i = 0; i < n_bins; i++) rate[i] = signal_fit_rates_N[i];
  }

  // Do the scan
  int xvar, yvar;
  double xmin, xmax, xsteps,
    ymin, ymax, ysteps;

  if (this_projection == dcp_th13) {
    xvar = GLB_THETA_13;
    yvar = GLB_DELTA_CP;

    xmin = th13_lower;
    xmax = th13_upper;
    xsteps = th13_steps;

    ymin = delta_lower;
    ymax = delta_upper;
    ysteps = delta_steps;

    printf("TRUEVALUES %f %f\n", theta13, deltacp);
  } else if (this_projection == sinsqth23_dmsq32) {
    xvar = GLB_THETA_23;
    yvar = GLB_DM_31;

    xmin = th23_lower;
    xmax = th23_upper;
    xsteps = th23_steps;

    ymin = ldm_lower;
    ymax = ldm_upper;
    ysteps = ldm_steps;

    printf("TRUEVALUES %f %f\n", theta23, ldm);
  }
  
  double this_x, this_y;
  double res;
  for(this_x=xmin; this_x<xmax; this_x+=(xmax-xmin)/xsteps)
    {
      for(this_y=ymin; this_y<ymax; this_y+=(ymax-ymin)/ysteps)
	{
	  /* Set vector of test=fit values */
	  glbSetOscParams(test_values, this_x, xvar);
	  glbSetOscParams(test_values, this_y, yvar);
	  
	  /* Compute chi^2 assuming the normal mass hierarchy in the fit */
	  res = glbChiNP(test_values, NULL, GLB_ALL);

	  printf("CONTOURPOINT %f %f %f\n", this_x, this_y, res);
    }

  }
  
  /* Destroy parameter and projection vector(s) */
  glbFreeParams(true_values);
  glbFreeParams(test_values);
  glbFreeParams(input_errors);
  glbFreeProjection(globes_projection);

  return 0;
}
