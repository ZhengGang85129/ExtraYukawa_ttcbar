#include <stdexcept>
#include "IDScaleFactor.h"





float IDScaleFact(const char *channel="", TH2D*h1=NULL,TH2D*h2=NULL,float l1pt=0,float l2pt=0, float l1eta=0, float l2eta=0){
    
    if(strcmp(channel,"DoubleElectron") ==0 ||strcmp(channel,"DoubleMuon")==0 ){
        return ID_sf_singlelepton(h1,l1pt,l1eta)*ID_sf_singlelepton(h1,l2pt,l2eta);
    }  
    else if (strcmp(channel,"ElectronMuon") ==0){
        return ID_sf_singlelepton(h1,l1pt,l1eta)*ID_sf_singlelepton(h2,l2pt,l2eta);
    }
    else{
       throw std::invalid_argument( "received negative value" ); 
    }

}


float ID_sf_singlelepton(TH2D *h, float pt, float eta){

    if( pt > 200)
        pt = 199;
    return h->GetBinContent(h->FindBin(pt,eta));

}

