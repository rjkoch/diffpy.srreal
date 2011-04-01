/*****************************************************************************
*
* diffpy.srreal     by DANSE Diffraction group
*                   Simon J. L. Billinge
*                   (c) 2010 Trustees of the Columbia University
*                   in the City of New York.  All rights reserved.
*
* File coded by:    Pavol Juhas
*
* See AUTHORS.txt for a list of people who contributed.
* See LICENSE.txt for license information.
*
******************************************************************************
*
* Bindings to the PDFEnvelope class.  The business methods can be overloaded
* from Python to create custom PDF envelope functions.
*
* $Id$
*
*****************************************************************************/

#include <boost/python.hpp>

#include <diffpy/srreal/PDFEnvelope.hpp>

#include "srreal_converters.hpp"

namespace srrealmodule {
namespace nswrap_PDFEnvelope {

using namespace boost;
using namespace boost::python;
using namespace diffpy::srreal;

// docstrings ----------------------------------------------------------------

const char* doc_PDFEnvelope = "\
FIXME\n\
";

const char* doc_PDFEnvelope_create = "\
FIXME\n\
";

const char* doc_PDFEnvelope_clone = "\
FIXME\n\
";

const char* doc_PDFEnvelope_type = "\
FIXME\n\
";

const char* doc_PDFEnvelope___call__ = "\
FIXME\n\
";

const char* doc_PDFEnvelope__registerThisType = "\
FIXME\n\
";

const char* doc_PDFEnvelope_createByType = "\
FIXME\n\
";

const char* doc_PDFEnvelope_getRegisteredTypes = "\
Set of string identifiers for registered PDFEnvelope classes.\n\
These are allowed arguments for the createByType static method.\n\
";

// wrappers ------------------------------------------------------------------

DECLARE_PYSET_FUNCTION_WRAPPER(PDFEnvelope::getRegisteredTypes,
        getPDFEnvelopeTypes_asset)

// Helper class allows overload of the PDFEnvelope methods from Python.

class PDFEnvelopeWrap :
    public PDFEnvelope,
    public wrapper_srreal<PDFEnvelope>
{
    public:

        // HasClassRegistry methods

        PDFEnvelopePtr create() const
        {
            override f = this->get_pure_virtual_override("create");
            return f();
        }

        PDFEnvelopePtr clone() const
        {
            override f = this->get_pure_virtual_override("clone");
            return f();
        }


        const std::string& type() const
        {
            override f = this->get_pure_virtual_override("type");
            object tp = f();
            mtype = python::extract<std::string>(tp);
            return mtype;
        }

        // own methods

        double operator()(const double& x) const
        {
            override f = this->get_pure_virtual_override("__call__");
            return f(x);
        }

    private:

        mutable std::string mtype;

};  // class PDFEnvelopeWrap

}   // namespace nswrap_PDFEnvelope

// Wrapper definition --------------------------------------------------------

void wrap_PDFEnvelope()
{
    using namespace nswrap_PDFEnvelope;
    using diffpy::Attributes;

    class_<PDFEnvelopeWrap, bases<Attributes>,
        noncopyable>("PDFEnvelope", doc_PDFEnvelope)
        .def("create", &PDFEnvelope::create, doc_PDFEnvelope_create)
        .def("clone", &PDFEnvelope::clone, doc_PDFEnvelope_clone)
        .def("type", &PDFEnvelope::type,
                return_value_policy<copy_const_reference>(),
                doc_PDFEnvelope_type)
        .def("__call__", &PDFEnvelope::operator(),
                doc_PDFEnvelope___call__)
        .def("_registerThisType", &PDFEnvelope::registerThisType,
                doc_PDFEnvelope__registerThisType)
        .def("createByType", &PDFEnvelope::createByType,
                doc_PDFEnvelope_createByType)
        .staticmethod("createByType")
        .def("getRegisteredTypes", getPDFEnvelopeTypes_asset,
                doc_PDFEnvelope_getRegisteredTypes)
        .staticmethod("getRegisteredTypes")
        ;

    register_ptr_to_python<PDFEnvelopePtr>();
}

}   // namespace srrealmodule

// End of file
