from multiprocessing import Manager

manager = Manager()

HistSettings =manager.dict()
HistSettings['DY_l1_pt'] = manager.dict()
HistSettings['DY_l1_pt']['name'] = 'DY_l1_pt'
HistSettings['DY_l1_pt']['nbins'] = 20
HistSettings['DY_l1_pt']['lowedge'] = 0
HistSettings['DY_l1_pt']['highedge'] = 200


HistSettings['DY_l1_eta'] = manager.dict()
HistSettings['DY_l1_eta']['name'] = 'DY_l1_eta'
HistSettings['DY_l1_eta']['nbins'] = 20
HistSettings['DY_l1_eta']['lowedge'] = -3
HistSettings['DY_l1_eta']['highedge'] = 3

HistSettings['DY_l1_phi'] = manager.dict()
HistSettings['DY_l1_phi']['name'] = 'DY_l1_phi'
HistSettings['DY_l1_phi']['nbins'] = 20
HistSettings['DY_l1_phi']['lowedge'] = -4
HistSettings['DY_l1_phi']['highedge'] = 4

HistSettings['DY_l2_pt'] = manager.dict()
HistSettings['DY_l2_pt']['name'] = 'DY_l2_pt'
HistSettings['DY_l2_pt']['nbins'] = 20
HistSettings['DY_l2_pt']['lowedge'] = 0
HistSettings['DY_l2_pt']['highedge'] = 100

HistSettings['DY_l2_eta'] = manager.dict()
HistSettings['DY_l2_eta']['name'] = 'DY_l2_eta'
HistSettings['DY_l2_eta']['nbins'] = 20
HistSettings['DY_l2_eta']['lowedge'] = -3
HistSettings['DY_l2_eta']['highedge'] = 3

HistSettings['DY_l2_phi'] = manager.dict()
HistSettings['DY_l2_phi']['name'] = 'DY_l2_phi'
HistSettings['DY_l2_phi']['nbins'] = 20
HistSettings['DY_l2_phi']['lowedge'] = -4
HistSettings['DY_l2_phi']['highedge'] = 4

HistSettings['DY_z_pt'] = manager.dict()
HistSettings['DY_z_pt']['name'] = 'DY_z_pt'
HistSettings['DY_z_pt']['nbins'] = 50
HistSettings['DY_z_pt']['lowedge'] = 0
HistSettings['DY_z_pt']['highedge'] = 200

HistSettings['DY_z_eta'] = manager.dict()
HistSettings['DY_z_eta']['name'] = 'DY_z_eta'
HistSettings['DY_z_eta']['nbins'] = 20
HistSettings['DY_z_eta']['lowedge'] = -3
HistSettings['DY_z_eta']['highedge'] = 3

HistSettings['DY_z_phi'] = manager.dict()
HistSettings['DY_z_phi']['name'] = 'DY_z_phi'
HistSettings['DY_z_phi']['nbins'] = 20
HistSettings['DY_z_phi']['lowedge'] = -4
HistSettings['DY_z_phi']['highedge'] = 4

HistSettings['DY_z_mass'] = manager.dict()
HistSettings['DY_z_mass']['name'] = 'DY_z_mass'
HistSettings['DY_z_mass']['nbins'] = 60
HistSettings['DY_z_mass']['lowedge'] = 60
HistSettings['DY_z_mass']['highedge'] = 120
