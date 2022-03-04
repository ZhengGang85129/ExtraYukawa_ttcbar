void a() {
TFile *f=TFile::Open("/afs/cern.ch/user/m/melu/public/output.root");
std::cout<< f->GetName()<< std::endl;
std::cout<< f->IsZombie()<< std::endl;
TH2D*h1=(TH2D*)f->Get("EleIDDataEff");
}

