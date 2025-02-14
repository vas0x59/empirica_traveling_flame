// #include "fvCFD.H"

#include "argList.H"
#include "timeSelector.H"
// #include "setWriter.H"
#include "writeFile.H"

#include "surfaceMesh.H"
#include "fieldTypes.H"
//#include "fieldMapper.H"
#include "fvsPatchFields.H"
#include "patchToPatch.H"
//#include "fvPatchField.H"
// #include "inletOutletFvPatchFields.H"
#include "inletOutletFvPatchFields.H"
#include "fixedValueFvPatchFields.H"
#include "Constant.H"
#include "Uniform.H"
#include "volFields.H"

#include "uniformDimensionedFields.H"

using namespace std;
using namespace Foam;

struct Ys_t {
    double Y_fuel_fz;
    // double Y_air_fz;
    double Y_N2_fz;
    double Y_O2_fz;
};


// double Y_air_N2 = 0.767;
// double Y_air_O2 = 0.233;
double Y_liquid_fuel = 0.085;

double fuel_Z_0 = 0.048;

Ys_t calc_Ys(double z, double maxZ) {
    double t = min(1, max(1 - (z / maxZ), 0));
    Ys_t ys;
    ys.Y_fuel_fz = t * Y_liquid_fuel;
    double Y_air_fz = 1 - ys.Y_fuel_fz;
    // ys.Y_N2_fz = Y_air_N2 * Y_air_fz;
    // ys.Y_O2_fz = Y_air_O2 * Y_air_fz;
    return ys;
}

int main(int argc, char *argv[]) {
    // Initialize OpenFOAM
#include "setRootCase.H"
#include "createTime.H"
#include "createMesh.H"


    volScalarField ft_field
            (
                    IOobject
                            (
                                    "ft",
                                    runTime.name(),
                                    mesh,
                                    IOobject::MUST_READ,
                                    IOobject::NO_WRITE
                            ),
                    mesh
                    // dimensionedScalar(dimless, 0)
            );
    volScalarField fu_field
            (
                    IOobject
                            (
                                    "fu",
                                    runTime.name(),
                                    mesh,
                                    IOobject::MUST_READ,
                                    IOobject::NO_WRITE
                            ),
                    mesh
                    // dimensionedScalar(dimless, 0)
            );
    // volScalarField fu_field = mesh().lookupObject<volScalarField>("fu");
    // volScalarField fu_field = mesh().lookupObject<volScalarField>("fu");
    // volScalarField Y_O2_field
    // (
    //     IOobject
    //     (
    //         "O2",
    //         runTime.timeName(),
    //         mesh,
    //         IOobject::MUST_READ,
    //         IOobject::NO_WRITE 
    //     ),
    //     mesh
    // );


    const vectorField &cellCenters = mesh.C();


    scalar maxZ = 0;


    // forAll(cellCenters, cellI)
    // {
    //     scalar z = cellCenters[cellI].z(); 

    //     maxZ = max(maxZ, z);
    // }

    maxZ = fuel_Z_0;

    // Info << "maxZ " << maxZ << " units" << endl;


    forAll(cellCenters, cellI) {
        double z = cellCenters[cellI].z();

        Ys_t ys = calc_Ys(z, maxZ);

        ft_field[cellI] = ys.Y_fuel_fz;
        fu_field[cellI] = ys.Y_fuel_fz;

    }

    // auto lambda = [&](auto &field) {
    forAll(mesh.boundary(), patchI) {
        // auto &patch_field = Y_fuel_field.boundaryFieldRef()[patchI];
        auto &patch = mesh.boundary()[patchI];
        const word &patchName = patch.name();

        if (patchName == "XL") {
            std::cout << "patchI: " << patchI << std::endl;

            fvPatchField<scalar> inlet_field_ft(patch, ft_field);
            fvPatchField<scalar> inlet_field_fu(patch, fu_field);

            auto &patch_cf = patch.Cf();
            forAll(patch, faceI) {
                double z = patch_cf[faceI].z();
                Ys_t ys = calc_Ys(z, maxZ);
                inlet_field_ft[faceI] = ys.Y_fuel_fz;
                inlet_field_fu[faceI] = ys.Y_fuel_fz;
            }
            {
                // Foam::dictionary myDict;

                // std::stringstream samp;
                // samp << "nonuniform List<scalar> " << inlet_field_fuel.size() << "(";
                // forAll(inlet_field_fuel, index)
                // {
                //     samp << std::to_string(inlet_field_fuel[index]) << " ";
                // }
                // samp << ")";

                // myDict.add("value", samp.str(), true);
                // myDict.add("inletValue", samp.str(), true);


                // auto iopf = new inletOutletFvPatchField<scalar>(patch, Y_fuel_field, myDict);
                auto iopf = new inletOutletFvPatchField<scalar>(patch, ft_field);
                iopf->refValue() = inlet_field_ft;
                (*iopf) = inlet_field_ft;
                // fvPatchField<scalar>& parentRef = *iopf; // Cast or access the parent reference
                // parentRef = inlet_field_fuel;
                ft_field.boundaryFieldRef().set(patchI, iopf);
            }
            {
                // Foam::dictionary myDict;

                // std::stringstream samp;
                // samp << "nonuniform List<scalar> " << inlet_field_fuel.size() << "(";
                // forAll(inlet_field_fuel, index)
                // {
                //     samp << std::to_string(inlet_field_fuel[index]) << " ";
                // }
                // samp << ")";

                // myDict.add("value", samp.str(), true); 
                // myDict.add("inletValue", samp.str(), true);


                // auto iopf = new inletOutletFvPatchFieldZ<scalar>(patch, Y_fuel_field, myDict);
                auto iopf = new inletOutletFvPatchField<scalar>(patch, fu_field);
                iopf->refValue() = inlet_field_fu;
                (*iopf) = inlet_field_fu;
                // fvPatchField<scalar>& parentRef = *iopf; // Cast or access the parent reference
                // parentRef = inlet_field_fuel;
                fu_field.boundaryFieldRef().set(patchI, iopf);
            }


        }
        if (patchName == "border_liquid") {
            std::cout << "border_liquid patchI: " << patchI << std::endl;

            {
                auto fuel_ = new fixedValueFvPatchField<scalar>  (patch, ft_field);
                forAll(patch, faceI) {
                    (*fuel_)[faceI] = Y_liquid_fuel;
                }
                ft_field.boundaryFieldRef().set(patchI, fuel_);
            }
            {
                auto fuel_ = new fixedValueFvPatchField<scalar>  (patch, fu_field);
                forAll(patch, faceI) {
                    (*fuel_)[faceI] = Y_liquid_fuel;
                }
                fu_field.boundaryFieldRef().set(patchI, fuel_);
            }
        }
    }

    // };

    ft_field.write();
    fu_field.write();
    Info << "Field initialization completed and written to time directory." << endl;

    return 0;
}
