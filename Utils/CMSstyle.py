from ROOT import *

def Canvas():
    H_ref = 600; 
    W_ref = 600; 
    W = W_ref
    H  = H_ref

    #T = 0.08*H_ref
    #B = 0.16*H_ref 
    #L = 0.16*W_ref
    #R = 0.04*W_ref
    canvas = TCanvas("c","c",W,H)
    canvas.SetFillColor(0)
    #canvas.SetBorderMode(0)
    #canvas.SetFrameFillStyle(0)
    #canvas.SetFrameBorderMode(0)
    #canvas.SetLeftMargin( L/W )
    #canvas.SetRightMargin( R/W )
    #canvas.SetTopMargin( T/H )
    #canvas.SetBottomMargin( B/H )
    #canvas.SetTickx(0)
    #canvas.SetTicky(0)
    canvas.SetGrid()
    canvas.SetFixedAspectRatio()
    return canvas
def Pad():
    pad = TPad()
    return pad
def SetAxisandLabels(histo):
    
    X = histo.GetXaxis()
    
    X.SetAxisColor(1)
    X.SetNdivisions(510)
    X.SetTickLength(0.03)

    X.SetLabelColor(1)
    X.SetLabelSize(0.04)
    X.SetLabelFont(42)
    X.SetLabelOffset(0.007)
    
    
    
    Y = histo.GetYaxis()

    Y.SetAxisColor(1)
    Y.SetNdivisions(510)
    Y.SetTickLength(0.03)


    Y.SetLabelColor(1)
    Y.SetLabelSize(0.04)
    Y.SetLabelFont(42)
    Y.SetLabelOffset(0.007)
    X.SetNdivisions(510)

def SetStyle(gPad):
    latex = TLatex()
    latex.SetNDC()
    l = gPad.GetLeftMargin()
    t = gPad.GetTopMargin()
    r = gPad.GetRightMargin()
    b = gPad.GetBottomMargin()
    
    
    #CMS text

    cmsText ="CMS"
    cmsTextFont = 60
    cmsTextSize = 0.6
    cmsTextOffset = 0.1

    relPosX = 0.12
    relPosY = 0.035

    # extra
    extraText = ' Preliminary 2017'
    extraOverCmsTextSize =0.76
    extraTextFont = 52

    lumiText ='41.5 fb^{-1}(13 TeV)'
    lumiTextSize = 0.5
    lumiTextOffset = 0.2
    relExtraDY = 1.2

    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    extraTextSize = extraOverCmsTextSize * cmsTextSize
    latex.SetTextFont(42)

    latex.SetTextAlign(31)
    latex.SetTextSize(lumiTextSize * t)
    latex.DrawLatex(1 - r, 1 - t + lumiTextOffset * t, lumiText )

    latex.SetTextFont(cmsTextFont)
    latex.SetTextAlign(11)
    latex.SetTextSize(cmsTextSize * t)
    latex.DrawLatex(l, 1 - t + lumiTextOffset * t, cmsText)
    #posX_ = 0 
    posX_ = l + relPosX * (1 - l - r)
    posY_ = 1 - t + lumiTextOffset * t
    alignX_ = 1
    alignY_ = 1
    align_ = 10 * alignX_ + alignY_

    latex.SetTextFont(extraTextFont)
    latex.SetTextSize(extraTextSize * t)
    latex.SetTextAlign(align_)
    latex.DrawLatex(posX_,posY_,extraText)
    latex.SetTextAlign(31)
    latex.SetTextSize(lumiTextSize * t)
    return gPad


