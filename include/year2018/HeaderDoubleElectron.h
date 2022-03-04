#include "TH2D.h"
#include "TFile.h"


TFile *f = TFile::Open("file:///afs/cern.ch/user/m/melu/public/output.root");
TH2D *h = (TH2D*) f->Get("EleIDDataEff");


float ID_SF(float l1_pt, float l2_pt, float l1_eta, float l2_eta){
    if(l1_pt>500) l1_pt=499;
    if(l2_pt>500) l2_pt=499;
    float sf_l1=h->GetBinContent(h->FindBin(l1_pt,fabs(l1_eta)));
    float sf_l2=h->GetBinContent(h->FindBin(l2_pt,fabs(l2_eta)));
    return sf_l1*sf_l2;
}



