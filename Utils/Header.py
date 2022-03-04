Header_DoubleElectron="""

float a (float b){
    return a * a 
}
"""

#float Id_sf(float l1_pt, float l2_pt, float l1_eta, float l2_eta){\nif(l1_pt>200)l1_pt=199;\nif(l2_pt>200)l2_pt=199;\nfloat sf_l1=h1->GetBinContent(h1->FindBin(l1_pt,fabs(l1_eta)));\nfloat sf_l2=h1->GetBinContent(h1->FindBin(l2_pt,fabs(l2_eta)));\nreturn sf_l1*sf_l2;}


Define_Hists={
'DoubleElectron':Header_DoubleElectron
}
