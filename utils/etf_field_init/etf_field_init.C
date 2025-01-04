#include "fvCFD.H"
#include "inletOutletFvPatchField.H"
#include "fixedValueFvPatchField.H"

struct Ys_t {
    double Y_fuel_fz;
    // double Y_air_fz;
    double Y_N2_fz;
    double Y_O2_fz;
};


double Y_air_N2 = 0.767;
double Y_air_O2 = 0.233;
double Y_liquid_fuel = 0.09;

double fuel_Z_0 = 0.1;

Ys_t calc_Ys(double z, double maxZ) {
    double t = min(1, max(1 - (z / maxZ), 0));
    Ys_t ys;
    ys.Y_fuel_fz = t*Y_liquid_fuel;
    double Y_air_fz = 1 - ys.Y_fuel_fz;
    ys.Y_N2_fz = Y_air_N2 * Y_air_fz;
    ys.Y_O2_fz = Y_air_O2 * Y_air_fz;
    return ys;
}

int main(int argc, char *argv[])
{
    // Initialize OpenFOAM
    #include "setRootCase.H"
    #include "createTime.H"
    #include "createMesh.H"



    volScalarField Y_fuel_field
    (
        IOobject
        (
            "C2H5OH",
            runTime.timeName(),
            mesh,
            IOobject::MUST_READ,
            IOobject::NO_WRITE 
        ),
        mesh
    );
    volScalarField Y_N2_field
    (
        IOobject
        (
            "N2",
            runTime.timeName(),
            mesh,
            IOobject::MUST_READ,
            IOobject::NO_WRITE 
        ),
        mesh
    );
    volScalarField Y_O2_field
    (
        IOobject
        (
            "O2",
            runTime.timeName(),
            mesh,
            IOobject::MUST_READ,
            IOobject::NO_WRITE 
        ),
        mesh
    );


    const vectorField& cellCenters = mesh.C();


    scalar maxZ = 0;


    // forAll(cellCenters, cellI)
    // {
    //     scalar z = cellCenters[cellI].z(); 
        
    //     maxZ = max(maxZ, z);
    // }

    maxZ = fuel_Z_0;
    
    // Info << "maxZ " << maxZ << " units" << endl;


    forAll(cellCenters, cellI)
    {
        double z = cellCenters[cellI].z();
        
        Ys_t ys = calc_Ys(z, maxZ);
        
        Y_fuel_field[cellI] = ys.Y_fuel_fz;
        Y_N2_field[cellI] = ys.Y_N2_fz;
        Y_O2_field[cellI] = ys.Y_O2_fz;
    }

    // auto lambda = [&](auto &field) {
    forAll(mesh.boundary(), patchI)
    {
        // auto &patch_field = Y_fuel_field.boundaryFieldRef()[patchI];
        auto &patch = mesh.boundary()[patchI];
        const word& patchName =  patch.name();

        if (patchName == "XL")
        {
            std::cout << "patchI: " << patchI << std::endl;

            fvPatchField<scalar> inlet_field_fuel(patch, Y_fuel_field);
            fvPatchField<scalar> inlet_field_N2(patch, Y_N2_field);
            fvPatchField<scalar> inlet_field_O2(patch, Y_O2_field);
            auto &patch_cf = patch.Cf();
            forAll(patch, faceI) { 
                double z = patch_cf[faceI].z();
                Ys_t ys = calc_Ys(z, maxZ);
                inlet_field_fuel[faceI] = ys.Y_fuel_fz;
                inlet_field_N2[faceI] = ys.Y_N2_fz;
                inlet_field_O2[faceI] = ys.Y_O2_fz;
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
                auto iopf = new inletOutletFvPatchField<scalar>(patch, Y_fuel_field);
                iopf->refValue() = inlet_field_fuel;
                (*iopf) = inlet_field_fuel;
                // fvPatchField<scalar>& parentRef = *iopf; // Cast or access the parent reference
                // parentRef = inlet_field_fuel;
                Y_fuel_field.boundaryFieldRef().set(patchI, iopf);
            }
            {
                auto iopf = new inletOutletFvPatchField<scalar>(patch, Y_N2_field);
                iopf->refValue() = inlet_field_N2;
                (*iopf) = inlet_field_N2;
                // static_cast<fvPatchField<scalar>>(*iopf) = inlet_field_N2;
                Y_N2_field.boundaryFieldRef().set(patchI, iopf);
            }
            {
                auto iopf = new inletOutletFvPatchField<scalar>(patch, Y_O2_field);
                iopf->refValue() = inlet_field_O2;
                (*iopf) = inlet_field_O2;
                // static_cast<fvPatchField<scalar>>(*iopf) = inlet_field_O2;
                Y_O2_field.boundaryFieldRef().set(patchI, iopf);
            }
            
        }
        if (patchName == "border_liquid") {
            std::cout << "border_liquid patchI: " << patchI << std::endl;
            Foam::dictionary myDict;
            // Field<scalar> f(patch.size());
            // f = Y_liquid_fuel;
            
            myDict.add("value",Y_liquid_fuel); 
            auto fvpf = new fixedValueFvPatchField<scalar>(patch, Y_fuel_field, myDict);
            Y_fuel_field.boundaryFieldRef().set(patchI, fvpf);
        }
    }
    
    // };
    
    Y_fuel_field.write();
    Y_N2_field.write();
    Y_O2_field.write();

    Info << "Field initialization completed and written to time directory." << endl;

    return 0;
}
