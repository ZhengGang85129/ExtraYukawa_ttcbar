### ttc_bar
```
Analysis for ttcbar.
The structure of the code is simply derived from [TTC_plots](https://github.com/menglu21/TTC_plots.git)
```
## Steps to produce Trigger Scale Factors for three channels.
```
#step1: 

$ mkdir ExtraYukawa_ttcbar
$ cd ExtraYukawa_ttcbar
% git clone https://github.com/ZhengGang85129/ExtraYukawa_ttcbar.git

#step2: Initialization
- Build necessary paths to Data and MC directory.

$ python3 WorkFlow/main.py --mode Init --channels DoubleElectron DoubleMuon ElectronMuon --year 2017
$ sh ./script/script.sh

#step3: Build Directory
- Build Output Directory

$ python3 WorkFlow/main.py --mode BuildDir --year2017 --task TriggerSF --DirOut /eos/user/y/yourname/

#step4: Trigger Efficiency Calculation

At the moment, the analysis code haven't include multi-thread calculation, thus you need to calculate channel by channel, type by type(MC/Data).
ex: for DoubleElectron and MC samples(TTTo2L).
$ python3 WorkFlow/main.py --mode TrigEff_Calc --year2017 --channel DoubleElectron --Type MC

After the program is done, you can see your /eos/user/y/yourname/ExtraYukawa/TriggerSF/files/DoubleElectron directory, see what's the change.

#step5: Trigger Efficiency Plot

At the moment, you have to collect the trigger efficiency results of both types (MC/Data) from above actions for one channel, otherwise, you can't implement this step.
For DoubleElectron:

$ python3 WorkFlow/main.py --mode TrigEff_Plot --year2017 --channel DoubleElectron

#step6: Trigger ScaleFactor 

$ python3 WorkFlow/main.py --mode TrigSF_Calc --year2017 --channel DoubleElectron

After the program is done, you can see trigSF plots and files in your /eos/user/y/yourname/ExtraYukawa/TriggerSF/DoubleElectron/files/ and /eos/user/y/yourname/ExtraYukawa/TriggerSF/DoubleElectron/plots/
```
