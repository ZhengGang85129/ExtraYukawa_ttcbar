#include "TH2D.h"
#include "TFile.h"


TFile *f1 = TFile::Open("file:///eos/user/t/tihsu/share/muonID_SF/2018UL/muonIdSF_2018UL.root ");
TH2D *h1 = (TH2D*) f1->Get("muIDSF");
TFile *f2 = TFile::Open("file:///afs/cern.ch/user/m/melu/public/output.root");
TH2D *h2 = (TH2D*) f2->Get("EleIDDataEff");



float ID_SF(float l1_pt, float l2_pt, float l1_eta, float l2_eta){
    if(l1_pt>200) l1_pt=199;
    if(l2_pt>200) l2_pt=199;
    float sf_l1=h1->GetBinContent(h1->FindBin(l1_pt,fabs(l1_eta)));
    float sf_l2=h2->GetBinContent(h2->FindBin(l2_pt,fabs(l2_eta)));
    return sf_l1*sf_l2;
}

