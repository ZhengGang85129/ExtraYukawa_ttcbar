#include "TH2D.h"
#include "TFile.h"


TFile *f = TFile::Open("file:///afs/cern.ch/user/m/melu/public/output.root");
TH2D *h = (TH2D*) f->Get("muIDSF");


float ID_SF(float l1_pt, float l2_pt, float l1_eta, float l2_eta){
    if(l1_pt>200) l1_pt=199;
    if(l2_pt>200) l2_pt=199;
    float sf_l1=h->GetBinContent(h->FindBin(l1_pt,fabs(l1_eta)));
    float sf_l2=h->GetBinContent(h->FindBin(l2_pt,fabs(l2_eta)));
    return sf_l1*sf_l2;
}

