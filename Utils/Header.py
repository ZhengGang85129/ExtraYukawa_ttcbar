Histogram_Definition=dict()
Histogram_Definition['Same_Type']='''
#include "TFile.h"
#include "TH2D.h"
TFile *f1 = TFile::Open("{0}");
TH2D *h1= (TH2D*)f1->Get("{1}");
TH2D *h2 = h1;

'''
Histogram_Definition['Diff_Type']='''
#include "TFile.h"
#include "TH2D.h"
TFile *f1 = TFile::Open("{0}");
TFile *f2 = TFile::Open("{1}");
TH2D *h1= (TH2D*)f1->Get("{2}");
TH2D *h2 = (TH2D*)f2->Get("{3}");
'''

