#ifndef __IDSCALEFACTOR_H__
#define __IDSCALEFACTOR_H__
#include "TH2D.h"
#include "TFile.h"

float IDScaleFact(const char *, TH2D*,TH2D*,float ,float , float , float );
float ID_sf_singlelepton(TH2D*,float,float);

#endif
