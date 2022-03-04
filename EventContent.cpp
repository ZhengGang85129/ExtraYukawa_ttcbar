#include "TFile.h"
#include "TTree.h"
void EventContent(char *filename){

    TFile *file = TFile::Open(filename);
    TTree *t = (TTree*) file->Get("Events");
    t->Print();
}
