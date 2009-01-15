/***********************************************************************
* $Id$
***********************************************************************/

#include <string>
#include "RefinableObj/RefinableObj.h" // From ObjCryst
#include "bondwidthcalculator.h"

/* BondWidthCalculator */
SrReal::BondWidthCalculator::
BondWidthCalculator() : ObjCryst::RefinableObj() {}

SrReal::BondWidthCalculator::
~BondWidthCalculator() {}

float
SrReal::BondWidthCalculator::
calculate(SrReal::BondPair& bp) 
{

    float sigma;
    sigma = bp.getSC1()->mpScattPow->GetBiso();
    sigma += bp.getSC2()->mpScattPow->GetBiso();

    return sqrt(sigma/(8*M_PI*M_PI));

}

/* JeongBWCalculator */

SrReal::JeongBWCalculator::
JeongBWCalculator()
{
    delta1 = delta2 = qbroad = 0.0;

    ResetParList();

    /* Create the RefinablePar objects for delta1 and delta2 */
    // delta1
    {
    ObjCryst::RefinablePar* tmp = new ObjCryst::RefinablePar("delta1", &delta1, 0.0, 1.0, 
        &SrReal::bwrefpartype, ObjCryst::REFPAR_DERIV_STEP_ABSOLUTE, 
        false, false, true, false, 1.0, 1);
    tmp->AssignClock(mClockMaster);
    AddPar(tmp);
    }

    // delta2
    {
    ObjCryst::RefinablePar* tmp = new ObjCryst::RefinablePar("delta2", &delta2, 0.0, 1.0, 
        &SrReal::bwrefpartype, ObjCryst::REFPAR_DERIV_STEP_ABSOLUTE, 
        false, false, true, false, 1.0, 1);
    tmp->AssignClock(mClockMaster);
    AddPar(tmp);
    }

    // qbroad
    {
    ObjCryst::RefinablePar* tmp = new ObjCryst::RefinablePar("qbroad", &qbroad, 0.0, 1.0, 
        &SrReal::bwrefpartype, ObjCryst::REFPAR_DERIV_STEP_ABSOLUTE, 
        false, false, true, false, 1.0, 1);
    tmp->AssignClock(mClockMaster);
    AddPar(tmp);
    }
}

SrReal::JeongBWCalculator::
~JeongBWCalculator() 
{}

float
SrReal::JeongBWCalculator::
calculate(SrReal::BondPair& bp)
{

    // Only isotropic scattering factors are supported right now.  Only one of
    // delta1 or delta2 should be used. This is not enforced.
    float r, sigma, corr;
    sigma = SrReal::BondWidthCalculator::calculate(bp);
    r = bp.getDistance();
    corr = 1.0 - delta1/r - delta2/(r*r) + pow(qbroad*r, 2);
    if(corr > 0)
    {
        sigma *= sqrt(corr);
    }
    return sigma;
}

float
SrReal::JeongBWCalculator::
getDelta1()
{
    // Called this way in case the parameter is constrained
    return GetPar(&delta1).GetValue();
}

float
SrReal::JeongBWCalculator::
getDelta2()
{
    return GetPar(&delta2).GetValue();
}

float
SrReal::JeongBWCalculator::
getQbroad()
{
    return GetPar(&qbroad).GetValue();
}

void
SrReal::JeongBWCalculator::
setDelta1(float val)
{
    GetPar(&delta1).MutateTo(val);
    return;
}

void
SrReal::JeongBWCalculator::
setDelta2(float val)
{
    GetPar(&delta2).MutateTo(val);
    return;
}

void
SrReal::JeongBWCalculator::
setQbroad(float val)
{
    GetPar(&qbroad).MutateTo(val);
    return;
}

