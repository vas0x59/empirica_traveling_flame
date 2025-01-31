
python ~/Projects/DDOF/ddtransport/getThermoPoly.py ./constant/ethanol66.yaml ./constant/gen
python ~/Projects/DDOF/ddtransport/getDiffPoly.py ./constant/ethanol66.yaml ./constant/gen


canteraToFoam ./constant/ethanol66.yaml gas constant/etc/transportProperties0  constant/gen/reactions_cvt constant/gen/thermo_cvt

